use crate::{
    engine::Event,
    model::{Diagnostic, Severity},
};
pub fn events_json(events: &[Event]) -> String {
    let body=events.iter().map(|e|format!("    {{\"overlay\":\"{}\",\"action\":\"{}\",\"selector\":\"{}\",\"payload\":\"{}\"}}",esc(&e.overlay),esc(&e.action),esc(&e.selector),esc(&e.payload))).collect::<Vec<_>>().join(",\n");
    format!("{{\n  \"schema\":\"origo-overlay-events/v1\",\n  \"events\":[\n{body}\n  ]\n}}\n")
}
pub fn diagnostics_text(items: &[Diagnostic]) -> String {
    items
        .iter()
        .map(|d| {
            format!(
                "{} {:?} {}:{} {}",
                d.code, d.severity, d.line, d.column, d.message
            )
        })
        .collect::<Vec<_>>()
        .join("\n")
}
fn esc(s: &str) -> String {
    s.replace('\\', "\\\\")
        .replace('"', "\\\"")
        .replace('\n', "\\n")
}
#[allow(dead_code)]
fn _severity(s: &Severity) -> &'static str {
    match s {
        Severity::Info => "info",
        Severity::Warning => "warning",
        Severity::Error => "error",
    }
}
