# Embedded Firmware Security Tester

This project provides a testing framework for evaluating embedded firmware resilience against malformed input, command injection, and UART-based protocol violations. It includes Arduino-based firmware and a Python fuzzing tool to automate quality assurance (QA) and basic security audits for serial-connected microcontrollers.

## Key Features
- Injects structured, malformed, and randomized serial data via UART
- Enforces checksum validation on **both incoming and outgoing messages**
- Detects crashes, invalid parsing, and inconsistent firmware behavior
- Automatically verifies response integrity using checksums
- Logs pass/fail outcomes for each fuzz test with detailed output
- Provides a LaTeX-based formal test plan and evaluation rubric

## Folder Overview
- `firmware/`: Arduino sketch (`ArduinoSecurityTest.ino`) for serial command parsing with checksum verification
- `tester/`: Python fuzzing and response validation tool (`fuzzer.py`) using `pyserial`
- `logs/`: Timestamped test run outputs, including valid and malformed cases
- `docs/`: LaTeX documentation, test plan, architecture diagrams, and compiled PDF

## Getting Started
1. Flash `firmware/ArduinoSecurityTest.ino` to your Arduino Uno R4 using the Arduino IDE.
2. Connect the Arduino via USB and note the serial port (e.g., `COM5` or `/dev/ttyACM0`).
3. Run the fuzzing tool:
   ```bash
   python tester/fuzzer.py

## Requirements
- Python 3.x  
- [`pyserial`](https://pypi.org/project/pyserial/) (`pip install pyserial`)  
- Arduino Uno R4 or compatible microcontroller  
- Arduino IDE or PlatformIO  

## Example Command Format
- **Input:** `SET TEMP 25|201`  
- **Output:**  
  - `OK|139`  
  - `TEMP=25|157`  
  - `ERROR: Invalid Checksum|...`  

**Checksum Algorithm:** Sum of ASCII values of the message (before `|`) modulo 256.
