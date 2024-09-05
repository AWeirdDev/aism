use pyo3::prelude::*;

mod core;
mod provider_base;
mod provider_groq;
mod utils;

use crate::core::{RustAism, RustInstance};

#[pymodule]
fn aism(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_class::<RustAism>()?;
    m.add_class::<RustInstance>()?;
    Ok(())
}
