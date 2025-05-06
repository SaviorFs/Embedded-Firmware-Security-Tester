import serial
import time
import os
import random
from datetime import datetime

PORT = 'COM5'  # you have to change serial port according to your device
BAUD = 9600
LOG_DIR = '../logs'

VALID_COMMANDS = [
    "READ TEMP\n",
    "SET TEMP 25\n",
    "SET TEMP 50\n"
]

STATIC_FUZZ_CASES = [
    "SET TEMP 999\n",
    "SET TEMP -100\n",
    "SET TEMP twenty\n",
    "SET TEMP\n",
    "SET TEMP 25;DROP TABLE\n",
    "!!!!@@@@####\n",
    "A" * 120 + "\n"
]

def generate_random_fuzz_case():
    junk = ''.join(random.choices('!@#$%^&*()_+-=ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789', k=random.randint(10, 100)))
    return junk + "\n"

def send_and_receive(ser, msg, logfile):
    ser.write(msg.encode())
    ser.flush()
    time.sleep(0.25)  # note: needs Arduino more time depending on amount of work tests may fail if not enough time is allotted

    result_lines = []

    while ser.in_waiting:
        response = ser.readline().decode(errors='replace').strip()
        result_lines.append(response)

    output = result_lines[-1] if result_lines else "NO RESPONSE"
    verdict = "PASS" if "ERROR" in output or "TEMP=" in output or output == "OK" else "FAIL"

    log_entry = f"Command: {msg.strip()}\nResponse: {output}\nResult: {verdict}\n---\n"
    print(log_entry)
    logfile.write(log_entry)

def main():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_filename = os.path.join(LOG_DIR, f"fuzz_log_{timestamp}.txt")

    with serial.Serial(PORT, BAUD, timeout=2) as ser, open(log_filename, 'w') as logfile:
        print(f"[+] Logging to {log_filename}")
        time.sleep(2)

        ser.reset_input_buffer()
        logfile.write("=== VALID COMMAND TESTS ===\n")
        for cmd in VALID_COMMANDS:
            send_and_receive(ser, cmd, logfile)

        logfile.write("\n=== STATIC FUZZ TESTS ===\n")
        for cmd in STATIC_FUZZ_CASES:
            send_and_receive(ser, cmd, logfile)

        logfile.write("\n=== RANDOM FUZZ TESTS ===\n")
        for _ in range(5):
            cmd = generate_random_fuzz_case()
            send_and_receive(ser, cmd, logfile)

    print("Fuzzing complete. Review log file for results.")

if __name__ == "__main__":
    main()
