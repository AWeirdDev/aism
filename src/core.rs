use std::{collections::HashMap, env, sync::LazyLock};

use anyhow::Error;
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
    provider_groq::Groq,
};

#[pyclass]
pub struct RustAism {
    provider: Groq,
}

#[pymethods]
impl RustAism {
    #[new]
    #[pyo3(signature = (*, api_key = None))]
    fn new(api_key: Option<String>) -> Self {
        dotenv().ok();
        RustAism {
            provider: Groq::new(
                api_key
                    .unwrap_or(
                        env::var("GROQ_API_KEY").unwrap_or("".to_string())
                    )
            ),
        }
    }

    fn give(&self, value: String) -> RustInstance {
        RustInstance::new(value, self.provider.to_owned())
    }
}

#[pyclass]
pub struct RustInstance {
    #[pyo3(get)]
    value: String,
    provider: Groq,
}

impl RustInstance {
    pub fn new(value: String, provider: Groq) -> Self {
        RustInstance { value, provider }
    }
}

#[pymethods]
impl RustInstance {
    fn instruct(&self, py: Python, q: String) -> PyResult<String> {
        let f = async move {
            let res = self
                .provider
                .inquire(vec![
                    Message {
                        role: Role::User,
                        content: format!("Given data:\n{}", self.value),
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
            format!("Is the information {:?} mentioned in the above text? Write your reasons, and at the end of the line, write Yes or No.", keyword)
        )?;

        Ok(res.trim().to_lowercase().ends_with("yes"))
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
            let dict = PyDict::new_bound(py);
            for (key, value) in r.as_object().unwrap().iter() {
                dict.set_item(
                    key,
                    match value {
                        Value::String(s) => Some(s.to_string().to_object(py)),
                        Value::Number(n) => Some(n.to_string().to_object(py)),
                        Value::Null => None,
                        _ => Some("".to_string().to_object(py)),
                    }
                )?;
            }

            Ok(dict.into())
        } else {
            Err(PyRuntimeError::new_err(format!("failed to fill dictionary, original text:\n{}", res)))
        }
    }
}
