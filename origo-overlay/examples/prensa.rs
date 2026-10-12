// @origo-begin
// overlay "prensa-quality" {
// version "0.1";
// target "examples/prensa.rs";
// capability observe;
// capability emit;
// integrity hash "sha256:7c61dab41f1837deecd14c4017c9057861295851997c1461d172c4498cde8e83";
// observe variable "temperatura" -> trace "sensor_temperatura";
// observe return "calcular_indice" -> emit "quality.calculated";
// }
// @origo-end
fn calcular_indice(forca: f64, temperatura: f64) -> f64 {
    forca / temperatura
}
fn main() {
    let temperatura = 188.7;
    println!("{}", calcular_indice(410.2, temperatura));
}
