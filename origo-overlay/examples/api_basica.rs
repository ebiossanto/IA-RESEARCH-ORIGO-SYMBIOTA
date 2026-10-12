use std::path::Path;

use origo_overlay::{
    carrier, engine, output,
    policy::{self, Policy},
};

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let source = r#"
// @origo-begin
// overlay "exemplo-api" {
// version "0.1";
// capability observe;
// capability emit;
// observe variable "temperatura" -> trace "sensor_T3";
// observe return "calcular" -> emit "calculo.finalizado";
// }
// @origo-end

fn calcular(temperatura: f64) -> f64 {
    temperatura * 2.0
}

fn main() {
    let temperatura = 188.7;
    println!("{}", calcular(temperatura));
}
"#;

    let overlays = carrier::extract_from_host(Path::new("exemplo.rs"), source)?;

    for located in &overlays {
        policy::validate(&located.overlay, &Policy::default())?;

        println!(
            "overlay={} linhas={}-{}",
            located.overlay.name, located.start_line, located.end_line,
        );

        let events = engine::plan(&located.overlay);
        print!("{}", output::events_json(&events));
    }

    Ok(())
}
