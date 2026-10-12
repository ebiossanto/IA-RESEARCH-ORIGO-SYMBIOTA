use origo_overlay::{crypto, parser};

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let source = r#"// @origo-begin
// overlay "integridade" {
// version "0.1";
// integrity hash "sera-preenchido-pelo-exemplo";
// }
// @origo-end
fn main() {
    println!("processo industrial");
}
"#;

    let digest = crypto::source_hash(source)?;
    println!("hash calculado: {digest}");

    let overlay_source = format!(
        "overlay \"integridade\" {{\n\
         version \"0.1\";\n\
         integrity hash \"{digest}\";\n\
         }}"
    );

    let overlay = parser::parse_overlay(&overlay_source)?;
    crypto::verify_overlay_hash(source, &overlay)?;
    println!("integridade verificada");

    let modified = source.replace("processo industrial", "processo alterado");

    match crypto::verify_overlay_hash(&modified, &overlay) {
        Ok(()) => println!("alteracao nao detectada"),
        Err(error) => println!("alteracao detectada: {error}"),
    }

    Ok(())
}
