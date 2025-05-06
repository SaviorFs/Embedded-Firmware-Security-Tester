// Intial Serial Command Handler Firmware (more complex to come)
String inputString = "";
int temperature = 22; // just a random default value

void setup() {
  Serial.begin(9600);
  Serial.setTimeout(500);
  Serial.println("READY");
}

void loop() {
  if (Serial.available()) {
    inputString = Serial.readStringUntil('\n');
    inputString.trim();
    if (inputString.length() == 0 || inputString.length() > 100) {
      Serial.println("ERROR: Input too long or empty");
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
    Serial.println("ERROR: Input too long");
    return;
  }

  if (cmd.startsWith("SET TEMP ")) {
    String tempVal = cmd.substring(9);
    if (tempVal.length() == 0 || (tempVal.toInt() == 0 && tempVal != "0")) {
      Serial.println("ERROR: Invalid number format");
      return;
    }
    int temp = tempVal.toInt();
    if (temp >= 0 && temp <= 100) {
      temperature = temp;
      Serial.println("OK");
    } else {
      Serial.println("ERROR: Out of range");
    }
  } else if (cmd == "READ TEMP") {
    Serial.print("TEMP=");
    Serial.println(temperature);
  } else {
    Serial.println("ERROR: Unknown command");
  }
}
