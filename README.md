# Embedded Firmware Security Tester

This project simulates security attacks and malformed input on a simple embedded firmware running on a microcontroller (e.g., Arduino). It tests the system's resilience using automated fuzzing over UART.

## Structure
- `ArduinoFirmware/`: Command-based firmware to respond to input
- `SecurityTester/`: Python-based fuzzer to send malformed/valid commands
- `Logs/`: Execution logs of fuzzing sessions
- `Documentation/`: Test plans and vulnerability reports

## Getting Started
1. Upload firmware from `ArduinoFirmware/device_firmware.ino` to your Arduino
2. Run `serial_fuzzer.py` from the `SecurityTester` folder
3. Check `Logs/run_log.txt` for results

## Future Work
- I2C/SPI spoofing
- Buffer overflow detection
- Watchdog reset logging
