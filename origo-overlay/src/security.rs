use crate::model::{Diagnostic, Severity};

pub fn scan_unicode(source: &str) -> Vec<Diagnostic> {
    let mut out = Vec::new();
    for (li, line) in source.lines().enumerate() {
        for (ci, ch) in line.chars().enumerate() {
            let cp = ch as u32;
            let (code, msg) = if matches!(cp,0x202A..=0x202E|0x2066..=0x2069) {
                (
                    "OO-UNICODE-001",
                    Some(format!("controle bidirecional U+{cp:04X}")),
                )
            } else if matches!(cp, 0x200B | 0x200C | 0x200D | 0x2060 | 0xFEFF) {
                (
                    "OO-UNICODE-002",
                    Some(format!("caractere invisivel U+{cp:04X}")),
                )
            } else if matches!(cp,0xFE00..=0xFE0F|0xE0100..=0xE01EF) {
                (
                    "OO-UNICODE-003",
                    Some(format!("seletor de variacao U+{cp:04X}")),
                )
            } else {
                ("", None)
            };
            if let Some(message) = msg {
                out.push(Diagnostic {
                    code,
                    severity: Severity::Error,
                    line: li + 1,
                    column: ci + 1,
                    message,
                });
            }
        }
    }
    out
}
