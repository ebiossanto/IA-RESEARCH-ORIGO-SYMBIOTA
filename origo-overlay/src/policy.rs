use crate::{
    error::{OverlayError, Result},
    model::*,
};
use std::collections::HashSet;

#[derive(Debug, Clone)]
pub struct Policy {
    pub allow: HashSet<Capability>,
    pub max_rules: usize,
    pub require_integrity: bool,
}
impl Default for Policy {
    fn default() -> Self {
        Self {
            allow: [
                Capability::Observe,
                Capability::Emit,
                Capability::Export,
                Capability::Warn,
                Capability::Reject,
            ]
            .into_iter()
            .collect(),
            max_rules: 100,
            require_integrity: false,
        }
    }
}
pub fn validate(o: &Overlay, p: &Policy) -> Result<()> {
    if o.version != "0.1" {
        return Err(OverlayError::Validation(format!(
            "versao overlay nao suportada: {}",
            o.version
        )));
    }
    if o.rules.len() > p.max_rules {
        return Err(OverlayError::Policy(format!(
            "{} regras excedem limite {}",
            o.rules.len(),
            p.max_rules
        )));
    }
    for c in &o.capabilities {
        if !p.allow.contains(c) {
            return Err(OverlayError::Policy(format!(
                "capacidade negada: {}",
                c.as_str()
            )));
        }
    }
    if p.require_integrity && o.integrity.is_none() {
        return Err(OverlayError::Policy("integridade obrigatoria".into()));
    }
    for r in &o.rules {
        let needed = match &r.action {
            Action::Trace { .. } | Action::Record { .. } => Capability::Observe,
            Action::Emit { .. } => Capability::Emit,
            Action::Warn { .. } => Capability::Warn,
            Action::Reject { .. } => Capability::Reject,
        };
        if !o.capabilities.contains(&needed) {
            return Err(OverlayError::Validation(format!(
                "acao requer capability {}",
                needed.as_str()
            )));
        }
    }
    Ok(())
}
