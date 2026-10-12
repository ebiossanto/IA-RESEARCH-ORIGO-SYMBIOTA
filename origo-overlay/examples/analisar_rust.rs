use std::path::Path;

use origo_overlay::{
    carrier,
    policy::{self, Policy},
    rust_adapter,
};

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let source = r#"
// @origo-begin
// overlay "analise-rust" {
// version "0.1";
// capability observe;
// capability emit;
// observe parameter "calcular::forca" -> trace "sensor_forca";
// observe variable "indice" -> trace "indice_processo";
// observe return "calcular" -> emit "indice.calculado";
// }
// @origo-end

fn calcular<T>(
    forca: f64,
    temperatura: f64,
    metadados: Option<Result<T, String>>,
) -> f64
where
    T: Clone,
{
    let indice = forca / temperatura;
    let _ = metadados;
    indice
}
"#;

    let overlays = carrier::extract_from_host(Path::new("analise.rs"), source)?;

    for located in &overlays {
        policy::validate(&located.overlay, &Policy::default())?;
    }

    let analysis = rust_adapter::analyze(source, &overlays);
    rust_adapter::validate(&analysis)?;

    println!("simbolos indexados: {}", analysis.symbols.len());
    println!("seletores resolvidos: {}", analysis.resolved.len());
    print!("{}", rust_adapter::analysis_json(&analysis));

    let instrumented = rust_adapter::instrument(source, &analysis);

    println!("\n--- Rust instrumentado ---\n{instrumented}");
    Ok(())
}
