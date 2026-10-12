use crate::{
    error::{OverlayError, Result},
    model::LocatedOverlay,
    parser::parse_overlay,
};
use std::path::Path;

pub fn extract_from_host(path: &Path, source: &str) -> Result<Vec<LocatedOverlay>> {
    let mut out = Vec::new();
    let mut buffer = String::new();
    let mut start = 0usize;
    let mut active = false;
    for (i, line) in source.lines().enumerate() {
        let n = i + 1;
        if line.contains("@origo-begin") {
            if active {
                return Err(OverlayError::Validation(format!(
                    "bloco aninhado na linha {n}"
                )));
            }
            active = true;
            start = n;
            continue;
        }
        if line.contains("@origo-end") {
            if !active {
                return Err(OverlayError::Validation(format!(
                    "fim sem inicio na linha {n}"
                )));
            }
            let overlay = parse_overlay(&buffer)?;
            out.push(LocatedOverlay {
                overlay,
                source: path.into(),
                start_line: start,
                end_line: n,
            });
            buffer.clear();
            active = false;
            continue;
        }
        if active {
            buffer.push_str(&strip_comment(line));
            buffer.push('\n');
        }
    }
    if active {
        return Err(OverlayError::Validation(format!(
            "bloco iniciado na linha {start} nao foi encerrado"
        )));
    }
    Ok(out)
}
fn strip_comment(line: &str) -> String {
    let t = line.trim_start();
    for p in ["//", "#", "*", "/*"] {
        if let Some(r) = t.strip_prefix(p) {
            return r.trim_start().trim_end_matches("*/").trim_end().to_string();
        }
    }
    t.to_string()
}
