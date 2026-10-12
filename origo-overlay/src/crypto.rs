use sha2::{Digest, Sha256};

use crate::{
    error::{OverlayError, Result},
    model::Overlay,
};

pub const SHA256_PREFIX: &str = "sha256:";

pub fn sha256_bytes(input: &[u8]) -> String {
    let digest = Sha256::digest(input);
    let mut hex = String::with_capacity(64);
    for byte in digest {
        use std::fmt::Write;
        write!(&mut hex, "{byte:02x}").expect("writing to String cannot fail");
    }
    format!("{SHA256_PREFIX}{hex}")
}

/// Hashes the semantic host after removing complete Overlay carrier blocks.
/// This avoids a self-referential digest when the hash is declared inside the block.
pub fn canonical_host(source: &str) -> Result<String> {
    let mut output = String::new();
    let mut inside = false;
    let mut start_line = 0usize;

    for (index, line) in source.lines().enumerate() {
        let line_number = index + 1;
        if line.contains("@origo-begin") {
            if inside {
                return Err(OverlayError::Validation(format!(
                    "bloco Overlay aninhado na linha {line_number}"
                )));
            }
            inside = true;
            start_line = line_number;
            continue;
        }
        if line.contains("@origo-end") {
            if !inside {
                return Err(OverlayError::Validation(format!(
                    "fim Overlay sem inicio na linha {line_number}"
                )));
            }
            inside = false;
            continue;
        }
        if !inside {
            output.push_str(line.trim_end());
            output.push('\n');
        }
    }

    if inside {
        return Err(OverlayError::Validation(format!(
            "bloco Overlay iniciado na linha {start_line} nao foi encerrado"
        )));
    }
    Ok(output)
}

pub fn source_hash(source: &str) -> Result<String> {
    Ok(sha256_bytes(canonical_host(source)?.as_bytes()))
}

pub fn verify_overlay_hash(source: &str, overlay: &Overlay) -> Result<()> {
    let integrity = overlay.integrity.as_ref().ok_or_else(|| {
        OverlayError::Validation(format!(
            "overlay '{}' nao declara integrity hash",
            overlay.name
        ))
    })?;
    validate_sha256_literal(&integrity.source_hash)?;
    let actual = source_hash(source)?;
    if constant_time_eq(actual.as_bytes(), integrity.source_hash.as_bytes()) {
        Ok(())
    } else {
        Err(OverlayError::Validation(format!(
            "hash divergente para '{}': esperado {}, calculado {}",
            overlay.name, integrity.source_hash, actual
        )))
    }
}

pub fn validate_sha256_literal(value: &str) -> Result<()> {
    let hex = value
        .strip_prefix(SHA256_PREFIX)
        .ok_or_else(|| OverlayError::Validation("hash deve usar o prefixo sha256:".into()))?;
    if hex.len() != 64 || !hex.bytes().all(|b| b.is_ascii_hexdigit()) {
        return Err(OverlayError::Validation(
            "SHA-256 deve conter exatamente 64 digitos hexadecimais".into(),
        ));
    }
    Ok(())
}

fn constant_time_eq(left: &[u8], right: &[u8]) -> bool {
    if left.len() != right.len() {
        return false;
    }
    let mut difference = 0u8;
    for (&a, &b) in left.iter().zip(right) {
        difference |= a ^ b;
    }
    difference == 0
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::parser::parse_overlay;

    #[test]
    fn sha256_usa_vetor_conhecido() {
        assert_eq!(
            sha256_bytes(b"hello world"),
            "sha256:b94d27b9934d3e08a52e52d7da7dabfac484efe37a5380ee9088f7ace2efcde9"
        );
    }

    #[test]
    fn hash_ignora_o_bloco_overlay() {
        let a = "// @origo-begin\n// overlay \"a\" { }\n// @origo-end\nfn main() {}\n";
        let b = "// @origo-begin\n// overlay \"b\" { capability observe; }\n// @origo-end\nfn main() {}\n";
        assert_eq!(source_hash(a).unwrap(), source_hash(b).unwrap());
    }

    #[test]
    fn verifica_hash_real() {
        let source = "// @origo-begin\n// overlay metadata\n// @origo-end\nfn main() {}\n";
        let hash = source_hash(source).unwrap();
        let overlay =
            parse_overlay(&format!("overlay \"x\" {{\nintegrity hash \"{hash}\";\n}}")).unwrap();
        verify_overlay_hash(source, &overlay).unwrap();
    }
}
