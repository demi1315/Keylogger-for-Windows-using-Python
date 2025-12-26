# 🛡️ Encrypted Endpoint Activity Logger (Windows)
Ethical Keylogger Research & Defensive Security Study

---

## Abstract

This project presents the design and implementation of a **secure, encrypted endpoint activity logger** developed **strictly for ethical research and defensive security education**.

The goal of this work is to **understand how keyloggers operate at the operating system level**, how such tools are abused by attackers, and—most importantly—**how endpoint defenses detect and mitigate them**.

Unlike malicious implementations, this system enforces:
- **full AES encryption of all captured data**
- **controlled forensic reconstruction**
- **clear ethical boundaries**
- **defensive awareness as the primary outcome**

---

## Why This Project Matters

Keyloggers are often discussed only as *malware*, yet they are also:
- powerful **learning tools** for understanding endpoint monitoring
- essential for **blue-team threat modeling**
- critical for designing **EDR and anti-keylogging defenses**

Understanding how keyloggers work **does not make an attacker** —  
it makes a **better defender**.

This project exists to bridge that gap.

---

## Scope & Ethical Boundaries

This project was developed under the following **non-negotiable constraints**:

- ✔ Educational and research purposes only  
- ✔ Controlled lab environment  
- ✔ No persistence mechanisms  
- ✔ No data exfiltration  
- ✔ No stealth or evasion techniques  
- ✔ No deployment on real user systems  

The implementation intentionally avoids malware-style behaviors.

---

## High-Level Architecture

The system follows a **modular, secure data-capture pipeline**:

User Input Events → Event Listener Modules → Immediate AES Encryption → Encrypted Log Storage → Authorized Forensic Decryptor


At **no point** is plaintext activity written to disk.

---

## Technical Implementation Overview

### 1. Secure Initialization & Key Handling

- Generates or loads an **AES-128 Fernet key** (`audit.key`)
- Ensures encryption is active before any capture begins
- Creates an isolated log directory

This guarantees **zero plaintext exposure**.

---

### 2. System Context Collection

Captures initial system metadata to provide **audit context**, including:
- Hostname
- Local IP address
- Operating system details
- Processor architecture

This information is logged once as an **encrypted session header**.

---

### 3. Active Window Tracking

- Uses Windows API (`user32.dll`)
- Detects foreground window changes
- Associates keystroke activity with application context

This enables accurate session reconstruction without behavioral profiling.

---

### 4. Global Keystroke Monitoring

- Implemented using `pynput`
- Captures:
  - printable characters
  - special keys (ENTER, BACKSPACE, SHIFT)
- Events are timestamped and grouped by active window

Every keystroke is **encrypted immediately**.

---

### 5. Clipboard Activity Monitoring

- Runs in a background daemon thread
- Detects clipboard changes
- Logs events as encrypted entries

This demonstrates how sensitive data often leaks **outside traditional keystrokes**.

---

### 6. AES-Encrypted Log Storage

- All data is written only as ciphertext
- Stored in `system_audit.enc`
- Logs are unusable without the correct key

Even if the file is accessed, it is **cryptographically protected**.

---

## Forensic Decryptor & Evidence Reconstruction

To support **authorized auditing**, a separate decryptor was built.

### Capabilities

- Loads AES key securely
- Decrypts encrypted log entries
- Reconstructs user activity accurately by handling:
  - backspaces
  - ENTER key events
  - window switches
  - clipboard captures
  - timestamps

### Output

- Generates a clean, human-readable transcript
- Saved as `final_evidence.txt`
- Preserves event order exactly as recorded

This models a **forensically sound audit workflow**.

---

## Screenshots & Evidence

The `screenshots/` directory contains:

- Project folder structure
- Logger startup output
- Encrypted log file (`system_audit.enc`)
- AES key file (`audit.key`)
- Decryptor execution
- Final reconstructed output

All screenshots are captured from a **controlled lab system** and contain **no real user data**.

---

## Detection & Defense Analysis

### How Modern Security Tools Detect Keyloggers

Endpoint security solutions rely on **behavioral detection**, including:
- Keyboard API interception attempts
- Suspicious background listeners
- Abnormal file-write frequency
- Memory and thread inspection

Even simple scripts can be detected if they resemble malicious behavior.

---

## Defensive Best Practices

### Organizational Controls
- Deploy Endpoint Detection & Response (EDR)
- Enforce application whitelisting
- Monitor unusual input-capture behavior
- Restrict administrator privileges

### User-Level Protections
- Use Multi-Factor Authentication (MFA)
- Prefer password managers (auto-fill reduces keystrokes)
- Avoid running unknown executables
- Keep OS and security tools updated

**MFA remains the strongest mitigation**, even if keystrokes are captured.

---

## Limitations

- No persistence mechanisms implemented
- No stealth or obfuscation
- No real-world deployment
- Exploit development intentionally excluded

These constraints are deliberate and ethical.

---

## Final Reflection

This project demonstrates:
- how keyloggers operate internally
- how captured data can be protected with encryption
- how forensic reconstruction works
- why endpoint defenses must focus on **behavior**, not signatures

By understanding offensive tooling **responsibly**, we design **stronger defenses**.

---

## Disclaimer

This project is intended **strictly for educational and defensive research**.  
Unauthorized use of keylogging software is illegal and unethical.

---

*This repository represents my final internship project and reflects a deep focus on ethical security research, endpoint defense, and responsible tooling design.*
