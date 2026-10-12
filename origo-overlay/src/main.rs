use origo_overlay::{
    crypto, engine, load, output,
    policy::{self, Policy},
    rust_adapter, security,
};
use std::{
    env, fs,
    path::{Path, PathBuf},
    process,
};

fn main() {
    if let Err((code, message)) = run() {
        eprintln!("{message}");
        process::exit(code)
    }
}

fn run() -> Result<(), (i32, String)> {
    let args: Vec<String> = env::args().collect();
    if args.len() < 3 {
        return Err((64, help()));
    }
    let command = &args[1];
    let path = Path::new(&args[2]);
    let source = fs::read_to_string(path)
        .map_err(|e| (66, format!("nao foi possivel ler {}: {e}", path.display())))?;

    if command == "scan" {
        let diagnostics = security::scan_unicode(&source);
        return if diagnostics.is_empty() {
            println!("OK: nenhum Unicode perigoso detectado");
            Ok(())
        } else {
            println!("{}", output::diagnostics_text(&diagnostics));
            Err((
                2,
                format!("{} diagnostico(s) de seguranca", diagnostics.len()),
            ))
        };
    }
    if command == "hash" {
        println!(
            "{}",
            crypto::source_hash(&source).map_err(|e| (1, e.to_string()))?
        );
        return Ok(());
    }

    let overlays = load(path).map_err(|e| (1, e.to_string()))?;
    if overlays.is_empty() {
        return Err((1, "nenhum bloco Origo Overlay encontrado".into()));
    }
    for located in &overlays {
        policy::validate(&located.overlay, &Policy::default()).map_err(|e| (3, e.to_string()))?;
    }

    match command.as_str() {
        "inspect" => {
            for located in overlays {
                println!(
                    "overlay={} linhas={}-{} regras={}",
                    located.overlay.name,
                    located.start_line,
                    located.end_line,
                    located.overlay.rules.len()
                );
            }
            Ok(())
        }
        "verify" | "plan" | "integrity-check" => {
            if command == "integrity-check" {
                for located in &overlays {
                    crypto::verify_overlay_hash(&source, &located.overlay)
                        .map_err(|e| (5, e.to_string()))?;
                }
                println!(
                    "OK: integridade SHA-256 verificada para {} overlay(s)",
                    overlays.len()
                );
                return Ok(());
            }
            let events: Vec<_> = overlays
                .iter()
                .flat_map(|o| engine::plan(&o.overlay))
                .collect();
            if command == "plan" {
                print!("{}", output::events_json(&events));
            } else {
                engine::enforce(&events).map_err(|e| (3, e.to_string()))?;
                println!("OK: overlay validado");
            }
            Ok(())
        }
        "rust-check" | "rust-plan" | "rust-instrument" => {
            let analysis = rust_adapter::analyze(&source, &overlays);
            rust_adapter::validate(&analysis).map_err(|e| (4, e.to_string()))?;
            match command.as_str() {
                "rust-check" => println!(
                    "OK: {} seletor(es) resolvido(s), {} simbolo(s) indexado(s)",
                    analysis.resolved.len(),
                    analysis.symbols.len()
                ),
                "rust-plan" => print!("{}", rust_adapter::analysis_json(&analysis)),
                _ => {
                    let output_path = args
                        .get(3)
                        .map(PathBuf::from)
                        .unwrap_or_else(|| default_output(path));
                    fs::write(&output_path, rust_adapter::instrument(&source, &analysis)).map_err(
                        |e| {
                            (
                                1,
                                format!("nao foi possivel gravar {}: {e}", output_path.display()),
                            )
                        },
                    )?;
                    println!(
                        "instrumentacao declarativa gravada em {}",
                        output_path.display()
                    );
                }
            }
            Ok(())
        }
        _ => Err((64, help())),
    }
}

fn default_output(path: &Path) -> PathBuf {
    let stem = path
        .file_stem()
        .and_then(|s| s.to_str())
        .unwrap_or("output");
    path.with_file_name(format!("{stem}.origo.rs"))
}

fn help() -> String {
    "Uso:\n  origo-overlay scan <arquivo>\n  origo-overlay inspect <arquivo>\n  origo-overlay verify <arquivo>\n  origo-overlay plan <arquivo>\n  origo-overlay rust-check <arquivo.rs>\n  origo-overlay rust-plan <arquivo.rs>\n  origo-overlay rust-instrument <arquivo.rs> [saida.rs]\nNenhum comando executa processos, rede ou codigo arbitrario.".into()
}
