use pyo3::{
    prelude::*,
    types::{PyDict, PyList},
};
use serde_json::Value;

/// Converts rust json to json for pyo3 (python bindings)
pub fn to_py(py: Python<'_>, value: Value) -> PyResult<Option<PyObject>> {
    match value {
        Value::Null => Ok(None),
        Value::Bool(r) => Ok(Some(r.to_object(py))),
        Value::Number(n) => {
            if n.is_f64() {
                Ok(Some(n.as_f64().to_object(py)))
            } else {
                Ok(Some(n.as_i64().unwrap().to_object(py)))
            }
        }
        Value::String(s) => Ok(Some(s.to_object(py))),
        Value::Array(a) => {
            let list = PyList::empty_bound(py);
            for v in a {
                list.append(to_py(py, v)?)?;
            }
            Ok(Some(list.into()))
        }
        Value::Object(map) => {
            let dict = PyDict::new_bound(py);
            for (k, v) in map.iter() {
                dict.set_item(k, to_py(py, v.to_owned())?)?;
            }
            Ok(Some(dict.into()))
        }
    }
}
