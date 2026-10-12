pub mod carrier;
pub mod crypto;
pub mod engine;
pub mod error;
pub mod model;
pub mod output;
pub mod parser;
pub mod policy;
pub mod rust_adapter;
pub mod security;
use error::Result;
use model::LocatedOverlay;
use std::{fs, path::Path};
pub fn load(path: &Path) -> Result<Vec<LocatedOverlay>> {
    let source = fs::read_to_string(path)?;
    carrier::extract_from_host(path, &source)
}
