// Intial Serial Command Handler Firmware (more complex to come)
String inputString = "";
int temperature = 22; // just a random default value

String wrapWithChecksum(String msg) {
  int checksum = 0;
  for (int i = 0; i < msg.length(); i++) {
    checksum += msg[i];
  }
  checksum %= 256;
  return msg + "|" + String(checksum);
}

void setup() {
  Serial.begin(9600);
  Serial.setTimeout(500);
  Serial.println(wrapWithChecksum("READY"));
}

void loop() {
  if (Serial.available()) {
    inputString = Serial.readStringUntil('\n');
    inputString.trim();

    // checksum validation start
    int pipeIndex = inputString.indexOf('|');
    if (pipeIndex == -1) {
      Serial.println(wrapWithChecksum("ERROR: No Checksum"));
      return;
    }

    String rawCommand = inputString.substring(0, pipeIndex);
    String checksumStr = inputString.substring(pipeIndex + 1);
    int providedChecksum = checksumStr.toInt();

    int computedChecksum = 0;
    for (int i = 0; i < rawCommand.length(); i++) {
      computedChecksum += rawCommand[i];
    }
    computedChecksum %= 256;

    if (providedChecksum != computedChecksum) {
      Serial.println(wrapWithChecksum("ERROR: Invalid Checksum"));
      return;
    }

    inputString = rawCommand; // replace inputString with verified command
    // checksum validation end

    if (inputString.length() == 0 || inputString.length() > 100) {
      Serial.println(wrapWithChecksum("ERROR: Input too long or empty"));
    } else {
      handleCommand(inputString);
    }
    inputString = "";
  }
}

void handleCommand(String cmd) {
  Serial.print("Received: ");
  Serial.println(cmd);

  if (cmd.length() > 100) {
    Serial.println(wrapWithChecksum("ERROR: Input too long"));
    return;
  }

  if (cmd.startsWith("SET TEMP ")) {
    String tempVal = cmd.substring(9);
    if (tempVal.length() == 0 || (tempVal.toInt() == 0 && tempVal != "0")) {
      Serial.println(wrapWithChecksum("ERROR: Invalid number format"));
      return;
    }
    int temp = tempVal.toInt();
    if (temp >= 0 && temp <= 100) {
      temperature = temp;
      Serial.println(wrapWithChecksum("OK"));
    } else {
      Serial.println(wrapWithChecksum("ERROR: Out of range"));
    }
  } else if (cmd == "READ TEMP") {
    Serial.println(wrapWithChecksum("TEMP=" + String(temperature)));
  } else {
    Serial.println(wrapWithChecksum("ERROR: Unknown command"));
  }
}
