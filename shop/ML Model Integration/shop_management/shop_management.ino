#define ENTRY_TRIGGER_PIN 12
#define ENTRY_ECHO_PIN 13
#define EXIT_TRIGGER_PIN 10
#define EXIT_ECHO_PIN 11

#define BUTTON_A_PIN 2
#define BUTTON_B_PIN 3
#define BUTTON_C_PIN 4

long entryDuration, exitDuration;
int distanceEntry, distanceExit;
int peopleCount = 0;
unsigned long lastCountTime = 0;
const long debounceTime = 2000; // 2 seconds debounce time to prevent immediate re-triggering of entry/exit

void setup() {
  Serial.begin(9600);
  pinMode(ENTRY_TRIGGER_PIN, OUTPUT);
  pinMode(ENTRY_ECHO_PIN, INPUT);
  pinMode(EXIT_TRIGGER_PIN, OUTPUT);
  pinMode(EXIT_ECHO_PIN, INPUT);
  
  pinMode(BUTTON_A_PIN, INPUT_PULLUP);
  pinMode(BUTTON_B_PIN, INPUT_PULLUP);
  pinMode(BUTTON_C_PIN, INPUT_PULLUP);
}

void loop() {
  // Check for entry and exit with the ultrasonic sensors
  if (millis() - lastCountTime > debounceTime) {
    distanceEntry = calculateDistance(ENTRY_TRIGGER_PIN, ENTRY_ECHO_PIN);
    distanceExit = calculateDistance(EXIT_TRIGGER_PIN, EXIT_ECHO_PIN);

    if (distanceEntry < 5) { 
      peopleCount++;
      lastCountTime = millis();
      delay(1000); // Delay for the person to pass the sensor
    } 
    else if (distanceExit < 5) { 
      if (peopleCount > 0) {
        peopleCount--;
        lastCountTime = millis();
        delay(1000); // Delay for the person to pass the sensor
      }
    }
  }

  // Immediately handle button press for purchases
  checkButtonPress(BUTTON_A_PIN, 'A');
  checkButtonPress(BUTTON_B_PIN, 'B');
  checkButtonPress(BUTTON_C_PIN, 'C');
  
  delay(50); // Short delay to mitigate some bouncing effects
}

void checkButtonPress(int buttonPin, char article) {
  if (digitalRead(buttonPin) == LOW) {
    printPurchase(article);
    delay(200); // A short delay to help mitigate the immediate re-triggering
  }
}

void printPurchase(char article) {
  Serial.print(millis());
  Serial.print(",");
  Serial.print(peopleCount);
  Serial.print(",");
  Serial.println(article);
}

int calculateDistance(int triggerPin, int echoPin) {
  digitalWrite(triggerPin, LOW);
  delayMicroseconds(2);
  digitalWrite(triggerPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(triggerPin, LOW);

  long duration = pulseIn(echoPin, HIGH);
  int distance = duration * 0.034 / 2; // Calculate distance in cm
  return distance;
}
