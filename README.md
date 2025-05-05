# Embedded Firmware Security Tester

This project provides a test framework for evaluating embedded firmware resilience against malformed input, command injection, and other UART-based protocol violations. It combines Arduino firmware with a Python fuzz tester.

## Features
- Injects structured and random serial data to test microcontroller robustness
- Detects crashes, resets, and malformed response handling
- Documents expected vs. actual firmware behavior
- Provides formal evaluation criteria and logs

## Folder Overview
- `firmware/`: Arduino sketch for command-based serial interface
- `tester/`: Python fuzzing scripts using `pyserial`
- `docs/`: LaTeX + PDF documentation
- `logs/`: Runtime log outputs for test case analysis

## Getting Started
1. Flash `firmware/ArduinoSecurityTest.ino` to an Arduino Uno R4.
2. Run `tester/fuzzer.py` with the Arduino connected via USB.
3. Review logs in `logs/` and compare to `docs/EmbeddedSecurityTester.pdf`.

## Requirements
- Python 3.x
- `pyserial` library
- Arduino Uno R4 or compatible board
