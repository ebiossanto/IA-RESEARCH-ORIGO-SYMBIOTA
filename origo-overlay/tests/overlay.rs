use origo_overlay::{
    carrier, engine, parser,
    policy::{self, Policy},
    security,
};
use std::path::Path;
#[test]
fn parseia_sintaxe_minima() {
    let s = "overlay \"x\" {\nversion \"0.1\";\ncapability observe;\nobserve variable \"a\" -> trace \"origem\";\n}";
    let o = parser::parse_overlay(s).unwrap();
    assert_eq!(o.name, "x");
    assert_eq!(o.rules.len(), 1);
    policy::validate(&o, &Policy::default()).unwrap();
}
#[test]
fn extrai_de_comentario() {
    let s = "// @origo-begin\n// overlay \"x\" {\n// capability warn;\n// observe function \"f\" -> warn \"auditar\";\n// }\n// @origo-end";
    let o = carrier::extract_from_host(Path::new("x.rs"), s).unwrap();
    assert_eq!(o.len(), 1);
    assert_eq!(engine::plan(&o[0].overlay).len(), 1);
}
#[test]
fn bloqueia_unicode_invisivel() {
    let d = security::scan_unicode("let x=1;\u{202e}");
    assert_eq!(d[0].code, "OO-UNICODE-001");
}
#[test]
fn exige_capacidade() {
    let o =
        parser::parse_overlay("overlay \"x\" {\nobserve variable \"a\" -> emit \"e\";\n}").unwrap();
    assert!(policy::validate(&o, &Policy::default()).is_err());
}
