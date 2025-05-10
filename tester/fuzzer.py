import serial
import time
import os
import random
from datetime import datetime

PORT = 'COM5'  # you have to change serial port according to your device
BAUD = 9600
LOG_DIR = '../logs'

VALID_COMMANDS = [
    "READ TEMP",
    "SET TEMP 25",
    "SET TEMP 50",
    "FREE MEM",         # memory usage test
    "SET TEMP 33"       # EEPROM test: persistent temperature
]

STATIC_FUZZ_CASES = [
    "SET TEMP 999",
    "SET TEMP -100",
    "SET TEMP twenty",
    "SET TEMP",
    "SET TEMP 25;DROP TABLE",
    "!!!!@@@@####",
    "A" * 120,
    "READ TEMP|0",              # invalid checksum
    "SET TEMP 25|999"           # invalid checksum
]

def add_checksum(command):
    checksum = sum(ord(c) for c in command) % 256
    return f"{command}|{checksum}\n"

def verify_output_checksum(response):
    if "|" not in response:
        return False
    try:
        msg, chk = response.rsplit("|", 1)
        expected = sum(ord(c) for c in msg) % 256
        return expected == int(chk)
    except:
        return False

def generate_random_fuzz_case():
    junk = ''.join(random.choices('!@#$%^&*()_+-=ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789', k=random.randint(10, 100)))
    return junk + "\n"

def send_and_receive(ser, msg, logfile):
    ser.write(msg.encode())
    ser.flush()
    time.sleep(0.25)

    result_lines = []

    while ser.in_waiting:
        response = ser.readline().decode(errors='replace').strip()
        if "READY" in response or "BOOT OK" in response:
            logfile.write("[RESET DETECTED]\n")
            print("[RESET DETECTED]")
        result_lines.append(response)

    output = result_lines[-1] if result_lines else "NO RESPONSE"

    if not verify_output_checksum(output):
        verdict = "FAIL (bad checksum)"
    elif any(kw in output for kw in ["ERROR", "TEMP=", "FREE_MEM=", "OK"]):
        verdict = "PASS"
    else:
        verdict = "FAIL"

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

        # EEPROM persistence test is the SET then prompt reboot, then check logs
        logfile.write("=== EEPROM PERSISTENCE TEST (MANUAL) ===\n")
        send_and_receive(ser, add_checksum("SET TEMP 33"), logfile)
        print("\n Now reboot your Arduino by pressing the reset button once and press ENTER to continue...")
        input()  # this will be a manual pause for board reboot
        send_and_receive(ser, add_checksum("READ TEMP"), logfile)

        logfile.write("\n=== VALID COMMAND TESTS ===\n")
        for cmd in VALID_COMMANDS:
            send_and_receive(ser, add_checksum(cmd), logfile)

        logfile.write("\n=== STATIC FUZZ TESTS ===\n")
        for cmd in STATIC_FUZZ_CASES:
            if "|" in cmd:
                send_and_receive(ser, cmd + "\n", logfile)
            else:
                send_and_receive(ser, add_checksum(cmd), logfile)

        logfile.write("\n=== RANDOM FUZZ TESTS ===\n")
        for _ in range(5):
            cmd = generate_random_fuzz_case()
            send_and_receive(ser, cmd, logfile)

    print("Fuzzing complete. Review log file for results.")

if __name__ == "__main__":
    main()
