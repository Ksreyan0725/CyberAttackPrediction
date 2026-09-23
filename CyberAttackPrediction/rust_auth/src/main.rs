use rand::Rng;
use serde::Serialize;
use serde_json;

#[derive(Serialize)]
struct TempAccount {
    username: String,
    password: String,
    auth_token: String,
}

fn generate_random_string(length: usize) -> String {
    let charset: &[u8] = b"ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";
    let mut rng = rand::thread_rng();
    (0..length)
        .map(|_| {
            let idx = rng.gen_range(0..charset.len());
            charset[idx] as char
        })
        .collect()
}

fn main() {
    // Generate a secure temporary guest account
    let username = format!("Guest_{}", generate_random_string(8));
    let password = generate_random_string(16);
    let auth_token = generate_random_string(32);

    let account = TempAccount {
        username,
        password,
        auth_token,
    };

    // Output strictly JSON so the Python Wall can parse it securely
    if let Ok(json_out) = serde_json::to_string(&account) {
        println!("{}", json_out);
    } else {
        eprintln!("Failed to generate secure credentials.");
        std::process::exit(1);
    }
}
