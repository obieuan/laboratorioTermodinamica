// Librerías
#include <max6675.h>

// Sensor de presión MPX5700AP
const int pressurePin = A0;
const float Vout_min = 0.2;
const float Vout_max = 4.7;
const float P_min = 0.0;
const float P_max = 700.0;

// Pines MAX6675 (Termopar Tipo K)
const int thermoCLK = 52;  // SCK
const int thermoCS = 53;   // CS
const int thermoDO = 50;   // MISO (SO)

// Crear objeto MAX6675
MAX6675 thermocouple(thermoCLK, thermoCS, thermoDO);

// Pines BTS7960
const int RPWM = 5;
const int LPWM = 6;
const int R_EN = 7;
const int L_EN = 8;

// Variables de control automático
unsigned long startTime = 0;
bool extending = false;
bool retracting = false;
unsigned long motorDuration = 10000; // Duración configurable (default 10 segundos)

// Variables de control manual
bool manualMode = false;
int manualPWM = 128; // PWM configurable (0-255)

// Buffer para comandos seriales
String inputString = "";
bool stringComplete = false;

void setup() {
  // Configurar pines del motor
  pinMode(RPWM, OUTPUT);
  pinMode(LPWM, OUTPUT);
  pinMode(R_EN, OUTPUT);
  pinMode(L_EN, OUTPUT);
  
  // Habilitar ambos lados del puente H
  digitalWrite(R_EN, HIGH);
  digitalWrite(L_EN, HIGH);
  
  // Inicializar comunicación serial
  Serial.begin(9600);
  
  // Esperar estabilización del MAX6675
  delay(500);
  
  Serial.println("Sistema listo.");
  Serial.println("Comandos: E=extender | R=retraer | T:ms=tiempo | P:pwm=PWM | F=forward | B=backward | S=stop");
  Serial.print("Tiempo actual: ");
  Serial.print(motorDuration);
  Serial.println(" ms");
  Serial.print("PWM manual: ");
  Serial.println(manualPWM);
  
  // Reservar espacio para el string de entrada
  inputString.reserve(50);
}

void loop() {
  // Leer datos seriales
  while (Serial.available()) {
    char inChar = (char)Serial.read();
    
    // Comandos simples de un solo carácter
    if (inChar == 'E' || inChar == 'e') {
      stopManual();
      startExtension();
    }
    else if (inChar == 'R' || inChar == 'r') {
      stopManual();
      startRetraction();
    }
    else if (inChar == 'F' || inChar == 'f') {
      // Forward manual (extender)
      stopAuto();
      moveForward();
    }
    else if (inChar == 'B' || inChar == 'b') {
      // Backward manual (retraer)
      stopAuto();
      moveBackward();
    }
    else if (inChar == 'S' || inChar == 's') {
      // Stop todo
      stopAll();
    }
    else if (inChar == '\n') {
      stringComplete = true;
    }
    else {
      inputString += inChar;
    }
  }
  
  // Procesar comando compuesto si está completo
  if (stringComplete) {
    processCommand(inputString);
    inputString = "";
    stringComplete = false;
  }
  
  // ===== LECTURA CONTINUA DE SENSORES (SIEMPRE ACTIVA) =====
  static unsigned long lastSensorRead = 0;
  if (millis() - lastSensorRead >= 500) {
    // Leer presión
    int sensorValue = analogRead(pressurePin);
    float voltage = sensorValue * (5.0 / 1023.0);
    float pressure = ((voltage - Vout_min) * (P_max - P_min) /
                     (Vout_max - Vout_min)) + P_min;
    
    // Leer temperatura
    float temperature = thermocouple.readCelsius();
    
    // Verificar si hay error en la lectura del termopar
    if (isnan(temperature)) {
      Serial.print("Pressure: ");
      Serial.print(pressure);
      Serial.print(" kPa | Temperature: ERROR");
      Serial.println();
    } else {
      Serial.print("Pressure: ");
      Serial.print(pressure);
      Serial.print(" kPa | Temperature: ");
      Serial.print(temperature);
      Serial.println(" C");
    }
    
    lastSensorRead = millis();
  }
  // =========================================================
  
  // Control del tiempo de operación AUTOMÁTICA
  if (extending || retracting) {
    unsigned long elapsedTime = millis() - startTime;
    
    // Verificar si ha transcurrido el tiempo configurado
    if (elapsedTime >= motorDuration) {
      // Detener el motor
      analogWrite(RPWM, 0);
      analogWrite(LPWM, 0);
      
      if (extending) {
        Serial.println("Extension completada.");
        extending = false;
      }
      else if (retracting) {
        Serial.println("Retraccion completada.");
        retracting = false;
      }
    }
  }
}

void startExtension() {
  extending = true;
  retracting = false;
  manualMode = false;
  startTime = millis();
  Serial.println("Extendiendo motor...");
  analogWrite(RPWM, 255);
  analogWrite(LPWM, 0);
}

void startRetraction() {
  retracting = true;
  extending = false;
  manualMode = false;
  startTime = millis();
  Serial.println("Retrayendo motor...");
  analogWrite(RPWM, 0);
  analogWrite(LPWM, 255);
}

void moveForward() {
  manualMode = true;
  analogWrite(RPWM, manualPWM);
  analogWrite(LPWM, 0);
  Serial.print("Manual Forward - PWM: ");
  Serial.println(manualPWM);
}

void moveBackward() {
  manualMode = true;
  analogWrite(RPWM, 0);
  analogWrite(LPWM, manualPWM);
  Serial.print("Manual Backward - PWM: ");
  Serial.println(manualPWM);
}

void stopAll() {
  extending = false;
  retracting = false;
  manualMode = false;
  analogWrite(RPWM, 0);
  analogWrite(LPWM, 0);
  Serial.println("Motor detenido.");
}

void stopAuto() {
  extending = false;
  retracting = false;
}

void stopManual() {
  if (manualMode) {
    analogWrite(RPWM, 0);
    analogWrite(LPWM, 0);
    manualMode = false;
  }
}

void processCommand(String command) {
  command.trim();
  
  // Comando para cambiar el tiempo: T:valor
  if (command.startsWith("T:") || command.startsWith("t:")) {
    int colonIndex = command.indexOf(':');
    if (colonIndex != -1) {
      String timeStr = command.substring(colonIndex + 1);
      long newTime = timeStr.toInt();
      
      if (newTime >= 1000 && newTime <= 60000) {
        motorDuration = newTime;
        Serial.print("Tiempo actualizado a: ");
        Serial.print(motorDuration);
        Serial.println(" ms");
      } else {
        Serial.println("Error: Tiempo debe estar entre 1000 y 60000 ms");
      }
    }
  }
  
  // Comando para cambiar PWM manual: P:valor
  else if (command.startsWith("P:") || command.startsWith("p:")) {
    int colonIndex = command.indexOf(':');
    if (colonIndex != -1) {
      String pwmStr = command.substring(colonIndex + 1);
      int newPWM = pwmStr.toInt();
      
      if (newPWM >= 0 && newPWM <= 255) {
        manualPWM = newPWM;
        Serial.print("PWM manual actualizado a: ");
        Serial.println(manualPWM);
      } else {
        Serial.println("Error: PWM debe estar entre 0 y 255");
      }
    }
  }
}