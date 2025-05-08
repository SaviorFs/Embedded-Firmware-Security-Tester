// Initial Serial Command Handler Firmware (more complex to come)
#include <Arduino.h>

#define BUFFER_SIZE 128
char inputBuffer[BUFFER_SIZE];
int bufferIndex = 0;
bool commandReady = false;

int temperature = 22; // default value

// ARM-compatible estimate of free memory
int freeMemory() {
  char stackDummy;
  return &stackDummy - (char*)malloc(4);
}

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
  while (Serial.available() > 0 && !commandReady) {
    char incoming = Serial.read();
    if (incoming == '\n') {
      inputBuffer[bufferIndex] = '\0';  
      commandReady = true;
    } else if (bufferIndex < BUFFER_SIZE - 1) {
      inputBuffer[bufferIndex++] = incoming;
    }
  }

  if (commandReady) {
    String inputString = String(inputBuffer);
    inputString.trim();

    handleParsedString(inputString);

    bufferIndex = 0;
    commandReady = false;
  }
}

void handleParsedString(String inputString) {
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

  if (rawCommand.length() == 0 || rawCommand.length() > 100) {
    Serial.println(wrapWithChecksum("ERROR: Input too long or empty"));
  } else {
    handleCommand(rawCommand);
  }
}

void handleCommand(String cmd) {
  cmd.trim();  // this will normalize for reliable matching
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
  } else if (cmd == "FREE MEM") {
    int mem = freeMemory();
    Serial.println(wrapWithChecksum("FREE_MEM=" + String(mem)));
  } else {
    Serial.println(wrapWithChecksum("ERROR: Unknown command"));
  }
}
