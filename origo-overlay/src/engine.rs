use crate::{
    error::{OverlayError, Result},
    model::*,
};

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Event {
    pub overlay: String,
    pub action: String,
    pub selector: String,
    pub payload: String,
}
pub fn plan(o: &Overlay) -> Vec<Event> {
    o.rules
        .iter()
        .map(|r| Event {
            overlay: o.name.clone(),
            action: action_name(&r.action).into(),
            selector: selector_name(&r.selector),
            payload: payload(&r.action),
        })
        .collect()
}
pub fn enforce(events: &[Event]) -> Result<()> {
    for e in events {
        if e.action == "reject" {
            return Err(OverlayError::Policy(format!(
                "rejeitado por {}: {}",
                e.overlay, e.payload
            )));
        }
    }
    Ok(())
}
fn action_name(a: &Action) -> &'static str {
    match a {
        Action::Trace { .. } => "trace",
        Action::Record { .. } => "record",
        Action::Warn { .. } => "warn",
        Action::Reject { .. } => "reject",
        Action::Emit { .. } => "emit",
    }
}
fn payload(a: &Action) -> String {
    match a {
        Action::Trace { label } | Action::Record { label } => label.clone(),
        Action::Warn { message } | Action::Reject { message } => message.clone(),
        Action::Emit { event } => event.clone(),
    }
}
fn selector_name(s: &Selector) -> String {
    match s {
        Selector::Variable(v) => format!("variable:{v}"),
        Selector::Function(v) => format!("function:{v}"),
        Selector::Return(v) => format!("return:{v}"),
        Selector::Parameter { function, name } => format!("parameter:{function}::{name}"),
    }
}
