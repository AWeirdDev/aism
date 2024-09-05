use std::{collections::HashMap, env, sync::LazyLock};

use anyhow::Error;
use colored::Colorize;
use pyo3::{exceptions::PyRuntimeError, prelude::*, types::PyDict};
use serde_json::Value;
use tokio::runtime::{self, Runtime};
use dotenv::dotenv;

static RUNTIME: LazyLock<Runtime> = LazyLock::new(|| {
    runtime::Builder::new_current_thread()
        .enable_all()
        .build()
        .unwrap()
});

use crate::{
    provider_base::{Message, Provider, Role},
    provider_groq::Groq, utils,
};

#[pyclass]
pub struct RustAism {
    provider: Groq,
    debug: bool
}

#[pymethods]
impl RustAism {
    #[new]
    #[pyo3(signature = (*, api_key = None, debug = false))]
    fn new(api_key: Option<String>, debug: bool) -> Self {
        dotenv().ok();
        RustAism {
            provider: Groq::new(
                api_key
                    .unwrap_or(
                        env::var("GROQ_API_KEY").unwrap_or("".to_string())
                    )
            ),
            debug
        }
    }

    /// Creates a new instance.
    fn give(&self, value: String) -> RustInstance {
        RustInstance::new(vec![value], self.provider.to_owned(), self.debug)
    }

    /// Creates a new instance from a list of values.
    fn feed(&self, values: Vec<String>) -> RustInstance {
        RustInstance::new(values, self.provider.to_owned(), self.debug)
    }
}

#[pyclass]
#[derive(Clone)]
pub struct RustInstance {
    #[pyo3(get)]
    values: Vec<String>,
    provider: Groq,
    debug: bool
}

impl RustInstance {
    pub fn new(values: Vec<String>, provider: Groq, debug: bool) -> Self {
        RustInstance { values, provider, debug }
    }
}

#[pymethods]
impl RustInstance {
    fn give(&mut self, value: String) -> RustInstance {
        self.values.push(value);
        self.to_owned()
    }
    fn instruct(&self, py: Python, q: String) -> PyResult<String> {
        let f = async move {
            if self.debug {
                println!(
                    "→ {} instruct (q): {}",
                    "aism".bright_blue(),
                    format!("{:?}", q).dimmed()
                );
            }

            let res = self
                .provider
                .inquire(vec![
                    Message {
                        role: Role::User,
                        content: format!(
                            "Given data rows:\n{}", 
                            self.values
                                .iter()
                                .enumerate()
                                .map(|(i, v)| format!("{}. {}", i, v))
                                .collect::<Vec<String>>()
                                .join("\n")
                        ),
                    },
                    Message {
                        role: Role::User,
                        content: format!(
                            "Given the above data, follow the below instructions:\n{}\n{}", 
                            q,
                            "Follow the instructions and NEVER write anything else (e.g., descriptions, ...)\nONLY PROVIDE THE OUTPUT."
                        ),
                    },
                ])
                .await?;

            if self.debug {
                println!(
                    "{} {} instruct: {}",
                    "✓".green(),
                    "aism".bright_blue(),
                    format!("{:?}", res.content).dimmed()
                );
            }

            Ok(res)
        };

        let binding: Result<Message, Error> = py.allow_threads(|| RUNTIME.block_on(f));
        match binding {
            Ok(res) => Ok(res.content),
            Err(e) => Err(PyRuntimeError::new_err(format!(
                "error while instructing: {}",
                e
            ))),
        }
    }

    fn translate(&self, py: Python, language: String) -> PyResult<String> {
        self.instruct(py, format!("Translate it into the language {:?}", language))
    }

    fn summarize(&self, py: Python) -> PyResult<String> {
        self.instruct(py, "Summarize it into one sentence".to_string())
    }

    fn is_sensitive(&self, py: Python) -> PyResult<bool> {
        let res = self.instruct(
            py, 
            "Is it sensitive? Perform a profanity check and write the reasons. At the end of the line, write Yes or No"
                .to_string()
        )?;
        Ok(res.trim().to_lowercase().ends_with("yes"))
    }

    fn mentioned(&self, py: Python, keyword: String) -> PyResult<bool> {
        let res = self.instruct(
            py, 
            format!("Is the information {:?} mentioned in the above text? Write your reasons, and at the end of the line, write 'therefore,' Yes or No.", keyword)
        )?;

        Ok(res.trim().to_lowercase().trim_end_matches(".").ends_with("yes"))
    }

    fn matches(&self, py: Python, keyword: String) -> PyResult<bool> {
        let res = self.instruct(
            py, 
            format!("Does the information {:?} match the above text? Write your reasons, and at the end of the line, write 'therefore,' Yes or No.", keyword)
        )?;

        Ok(res.trim().to_lowercase().trim_end_matches(".").ends_with("yes"))
    }

    fn fill_dict(&self, py: Python, d: HashMap<String, String>) -> PyResult<PyObject> {
        let res = self.instruct(
            py,
            format!(
                "Given the below dictionary, you MUST fill it with the above data: {:?}\nYOU MUST provide valid JSON, NOT RUST CODE. If unknown, use null.", 
                d
            )
        )?;
        let filled = serde_json::from_str::<Value>(res.as_str());
        if let Ok(r) = filled {
            Ok(utils::to_py(py, r)?.unwrap_or(PyDict::new_bound(py).into()))
        } else {
            Err(PyRuntimeError::new_err(format!("failed to fill dictionary, original text:\n{}", res)))
        }
    }
}
