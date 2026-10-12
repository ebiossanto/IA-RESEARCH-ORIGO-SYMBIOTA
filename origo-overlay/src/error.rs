use std::{fmt, io};

#[derive(Debug)]
pub enum OverlayError {
    Io(io::Error),
    Parse { line: usize, message: String },
    Validation(String),
    Policy(String),
    Security(String),
    Usage(String),
}

impl fmt::Display for OverlayError {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            Self::Io(e) => write!(f, "erro de E/S: {e}"),
            Self::Parse { line, message } => write!(f, "linha {line}: {message}"),
            Self::Validation(m) => write!(f, "validacao: {m}"),
            Self::Policy(m) => write!(f, "politica: {m}"),
            Self::Security(m) => write!(f, "seguranca: {m}"),
            Self::Usage(m) => write!(f, "uso: {m}"),
        }
    }
}
impl std::error::Error for OverlayError {}
impl From<io::Error> for OverlayError {
    fn from(value: io::Error) -> Self {
        Self::Io(value)
    }
}
pub type Result<T> = std::result::Result<T, OverlayError>;
