use std::path::PathBuf;

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Overlay {
    pub name: String,
    pub version: String,
    pub target: Option<PathBuf>,
    pub capabilities: Vec<Capability>,
    pub rules: Vec<Rule>,
    pub integrity: Option<Integrity>,
}

#[derive(Debug, Clone, PartialEq, Eq, Hash)]
pub enum Capability {
    Observe,
    Emit,
    Export,
    Warn,
    Reject,
}

impl Capability {
    pub fn parse(s: &str) -> Option<Self> {
        match s {
            "observe" => Some(Self::Observe),
            "emit" => Some(Self::Emit),
            "export" => Some(Self::Export),
            "warn" => Some(Self::Warn),
            "reject" => Some(Self::Reject),
            _ => None,
        }
    }
    pub fn as_str(&self) -> &'static str {
        match self {
            Self::Observe => "observe",
            Self::Emit => "emit",
            Self::Export => "export",
            Self::Warn => "warn",
            Self::Reject => "reject",
        }
    }
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum Selector {
    Variable(String),
    Function(String),
    Return(String),
    Parameter { function: String, name: String },
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum Action {
    Trace { label: String },
    Record { label: String },
    Warn { message: String },
    Reject { message: String },
    Emit { event: String },
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Rule {
    pub selector: Selector,
    pub action: Action,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Integrity {
    pub source_hash: String,
    pub signer: Option<String>,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct LocatedOverlay {
    pub overlay: Overlay,
    pub source: PathBuf,
    pub start_line: usize,
    pub end_line: usize,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum Severity {
    Info,
    Warning,
    Error,
}
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Diagnostic {
    pub code: &'static str,
    pub severity: Severity,
    pub line: usize,
    pub column: usize,
    pub message: String,
}
