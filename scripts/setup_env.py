import os
import json
import subprocess
from werkzeug.security import generate_password_hash

def run_setup():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    target_dir = os.path.join(base_dir, "CyberAttackPrediction")
    users_file = os.path.join(target_dir, "users.json")
    rust_exe = os.path.join(target_dir, "rust_auth", "target", "release", "rust_auth.exe")
    
    if os.path.exists(users_file):
        # Already set up
        return
        
    print("\n=======================================================")
    print("[First-Time Setup] Initializing Secure Local Environment")
    print("=======================================================")
    
    if not os.path.exists(rust_exe):
        print("[-] Error: Rust authentication engine not found.")
        print(f"[-] Expected at: {rust_exe}")
        print("[-] Please compile the rust_auth project first.")
        input("Press Enter to continue...")
        return
        
    print("[*] Calling Rust Engine for cryptographic key generation...")
    result = subprocess.run([rust_exe], capture_output=True, text=True)
    if result.returncode != 0:
        print("[-] Error: Rust engine failed to generate credentials.")
        input("Press Enter to continue...")
        return
        
    try:
        guest_creds = json.loads(result.stdout)
    except Exception as e:
        print(f"[-] Error parsing Rust output: {e}")
        input("Press Enter to continue...")
        return
        
    raw_username = guest_creds['username']
    raw_password = guest_creds['password']
    
    print("[*] Generating secure Werkzeug hashes...")
    hashed_password = generate_password_hash(raw_password)
    
    users = {
        raw_username: {
            "username": raw_username,
            "password": hashed_password,
            "role": "admin"
        }
    }
    
    with open(users_file, 'w') as f:
        json.dump(users, f, indent=4)
        
    print("\n[SUCCESS] Environment securely initialized!")
    print("-------------------------------------------------------")
    print(f"  Your Local Admin Username: {raw_username}")
    print(f"  Your Local Admin Password: {raw_password}")
    print("-------------------------------------------------------")
    print("[!] Please save these credentials. They will not be shown again.")
    print("=======================================================\n")
    input("Press Enter to enter the Launcher Menu...")

if __name__ == "__main__":
    run_setup()
