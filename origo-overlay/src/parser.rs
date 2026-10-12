use crate::{
    error::{OverlayError, Result},
    model::*,
};

pub fn parse_overlay(source: &str) -> Result<Overlay> {
    let mut name = None;
    let mut version = "0.1".to_string();
    let mut target = None;
    let mut capabilities = Vec::new();
    let mut rules = Vec::new();
    let mut integrity = None;
    for (i, raw) in source.lines().enumerate() {
        let line_no = i + 1;
        let line = raw.trim();
        if line.is_empty()
            || line.starts_with("//")
            || line.starts_with('#')
            || line == "{"
            || line == "}"
        {
            continue;
        }
        let line = line.trim_end_matches(';').trim();
        if let Some(rest) = line.strip_prefix("overlay ") {
            name = Some(unquote(rest.trim_end_matches('{').trim(), line_no)?);
            continue;
        }
        if let Some(rest) = line.strip_prefix("version ") {
            version = unquote(rest, line_no)?;
            continue;
        }
        if let Some(rest) = line.strip_prefix("target ") {
            target = Some(unquote(rest, line_no)?.into());
            continue;
        }
        if let Some(rest) = line.strip_prefix("capability ") {
            let c = Capability::parse(rest)
                .ok_or_else(|| perr(line_no, format!("capacidade desconhecida: {rest}")))?;
            if !capabilities.contains(&c) {
                capabilities.push(c);
            }
            continue;
        }
        if let Some(rest) = line.strip_prefix("integrity hash ") {
            integrity = Some(Integrity {
                source_hash: unquote(rest, line_no)?,
                signer: None,
            });
            continue;
        }
        if let Some(rest) = line.strip_prefix("observe ") {
            rules.push(parse_rule(rest, line_no)?);
            continue;
        }
        return Err(perr(line_no, format!("declaracao desconhecida: {line}")));
    }
    Ok(Overlay {
        name: name.ok_or_else(|| perr(1, "declaracao overlay ausente"))?,
        version,
        target,
        capabilities,
        rules,
        integrity,
    })
}

fn parse_rule(s: &str, line: usize) -> Result<Rule> {
    let (selector_text, action_text) = s
        .split_once(" -> ")
        .ok_or_else(|| perr(line, "regra observe exige '->'"))?;
    let selector = parse_selector(selector_text, line)?;
    let (kind, arg) = action_text.split_once(' ').unwrap_or((action_text, ""));
    let value = unquote(arg, line)?;
    let action = match kind {
        "trace" => Action::Trace { label: value },
        "record" => Action::Record { label: value },
        "warn" => Action::Warn { message: value },
        "reject" => Action::Reject { message: value },
        "emit" => Action::Emit { event: value },
        _ => return Err(perr(line, format!("acao desconhecida: {kind}"))),
    };
    Ok(Rule { selector, action })
}
fn parse_selector(s: &str, line: usize) -> Result<Selector> {
    let (kind, arg) = s
        .trim()
        .split_once(' ')
        .ok_or_else(|| perr(line, "seletor incompleto"))?;
    let value = unquote(arg, line)?;
    match kind {
        "variable" => Ok(Selector::Variable(value)),
        "function" => Ok(Selector::Function(value)),
        "return" => Ok(Selector::Return(value)),
        "parameter" => {
            let (f, n) = value
                .split_once("::")
                .ok_or_else(|| perr(line, "parameter usa funcao::nome"))?;
            Ok(Selector::Parameter {
                function: f.into(),
                name: n.into(),
            })
        }
        _ => Err(perr(line, format!("seletor desconhecido: {kind}"))),
    }
}
fn unquote(s: &str, line: usize) -> Result<String> {
    let s = s.trim();
    match s {
        "" => Ok(String::new()),
        value if value.starts_with('"') && value.ends_with('"') && value.len() >= 2 => {
            Ok(value[1..value.len() - 1].replace("\\\"", "\""))
        }
        _ => Err(perr(line, "valor deve estar entre aspas")),
    }
}
fn perr(line: usize, message: impl Into<String>) -> OverlayError {
    OverlayError::Parse {
        line,
        message: message.into(),
    }
}
