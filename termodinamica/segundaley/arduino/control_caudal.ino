#include <OneWire.h>
#include <DallasTemperature.h>

// ========== BOMBAS BTS7960 ==========
// --- Bomba 1 (Módulo 1) ---
#define R_EN1 7
#define L_EN1 8
#define RPWM1 5

// --- Bomba 2 (Módulo 2) ---
#define R_EN2 9
#define L_EN2 10
#define RPWM2 6

// Velocidades iniciales (0-255)
int pwm1 = 200;
int pwm2 = 180;

// ========== SENSORES DE TEMPERATURA DS18B20 ==========
OneWire oneWire1(11);
OneWire oneWire2(12);
OneWire oneWire3(4);

DallasTemperature sensor1(&oneWire1);
DallasTemperature sensor2(&oneWire2);
DallasTemperature sensor3(&oneWire3);

// ========== CAUDALÍMETROS YF-S201 ==========
volatile long NumPulsos1 = 0;
const int PinSensor1 = 2;
float factor_conversion = 7.11;
float volumen1 = 0.0;
float caudal1_L_m = 0.0;

volatile long NumPulsos2 = 0;
const int PinSensor2 = 3;
float volumen2 = 0.0;
float caudal2_L_m = 0.0;

// ========== CONTROL DE CAUDAL ==========
// Setpoints de caudal (L/min)
float caudal_setpoint1 = 0.0;  // Caudal deseado bomba 1
float caudal_setpoint2 = 0.0;  // Caudal deseado bomba 2

// Variables PID para Bomba 1
float error1 = 0, error_anterior1 = 0, integral1 = 0;
float Kp1 = 20.0;   // Ganancia proporcional
float Ki1 = 5.0;    // Ganancia integral
float Kd1 = 2.0;    // Ganancia derivativa

// Variables PID para Bomba 2
float error2 = 0, error_anterior2 = 0, integral2 = 0;
float Kp2 = 20.0;
float Ki2 = 5.0;
float Kd2 = 2.0;

// Control automático habilitado
bool auto_control1 = false;
bool auto_control2 = false;

// Control de tiempo
unsigned long tiempoAnterior = 0;
const unsigned long intervaloMuestreo = 100; // 100ms

// ========== ISR (Interrupciones) ==========
void ContarPulsos1() {
  NumPulsos1++;
}

void ContarPulsos2() {
  NumPulsos2++;
}

// ========== FUNCIONES AUXILIARES ==========
void CalcularCaudalesYVolumenes(float dt_s) {
  noInterrupts();
  long pulsos1 = NumPulsos1;
  long pulsos2 = NumPulsos2;
  NumPulsos1 = 0;
  NumPulsos2 = 0;
  interrupts();
  
  float frecuencia1 = pulsos1 / dt_s;
  float frecuencia2 = pulsos2 / dt_s;
  
  caudal1_L_m = frecuencia1 / factor_conversion;
  caudal2_L_m = frecuencia2 / factor_conversion;
  
  volumen1 += caudal1_L_m * (dt_s / 60.0);
  volumen2 += caudal2_L_m * (dt_s / 60.0);
}

void ControlPID_Bomba1(float dt_s) {
  if (!auto_control1 || caudal_setpoint1 == 0) {
    return;
  }
  
  // Calcular error
  error1 = caudal_setpoint1 - caudal1_L_m;
  
  // Término proporcional
  float P = Kp1 * error1;
  
  // Término integral (con anti-windup)
  integral1 += error1 * dt_s;
  if (integral1 > 50) integral1 = 50;
  if (integral1 < -50) integral1 = -50;
  float I = Ki1 * integral1;
  
  // Término derivativo
  float D = Kd1 * (error1 - error_anterior1) / dt_s;
  
  // Calcular PWM
  float pwm_ajuste = P + I + D;
  pwm1 += (int)pwm_ajuste;
  
  // Limitar PWM
  if (pwm1 < 0) pwm1 = 0;
  if (pwm1 > 255) pwm1 = 255;
  
  error_anterior1 = error1;
}

void ControlPID_Bomba2(float dt_s) {
  if (!auto_control2 || caudal_setpoint2 == 0) {
    return;
  }
  
  error2 = caudal_setpoint2 - caudal2_L_m;
  
  float P = Kp2 * error2;
  
  integral2 += error2 * dt_s;
  if (integral2 > 50) integral2 = 50;
  if (integral2 < -50) integral2 = -50;
  float I = Ki2 * integral2;
  
  float D = Kd2 * (error2 - error_anterior2) / dt_s;
  
  float pwm_ajuste = P + I + D;
  pwm2 += (int)pwm_ajuste;
  
  if (pwm2 < 0) pwm2 = 0;
  if (pwm2 > 255) pwm2 = 255;
  
  error_anterior2 = error2;
}

void ProcesarComandoSerial() {
  if (Serial.available()) {
    String comando = Serial.readStringUntil('\n');
    comando.trim();
    
    // Comando: r = reset volúmenes
    if (comando == "r" || comando == "R") {
      volumen1 = 0.0;
      volumen2 = 0.0;
      Serial.println("Volumenes reiniciados");
    }
    
    // Comando: S1:valor = setpoint caudal bomba 1
    else if (comando.startsWith("S1:")) {
      float valor = comando.substring(3).toFloat();
      caudal_setpoint1 = valor;
      auto_control1 = (valor > 0);
      Serial.print("Setpoint Bomba 1: ");
      Serial.println(valor);
    }
    
    // Comando: S2:valor = setpoint caudal bomba 2
    else if (comando.startsWith("S2:")) {
      float valor = comando.substring(3).toFloat();
      caudal_setpoint2 = valor;
      auto_control2 = (valor > 0);
      Serial.print("Setpoint Bomba 2: ");
      Serial.println(valor);
    }
    
    // Comando: M1:valor = PWM manual bomba 1
    else if (comando.startsWith("M1:")) {
      int valor = comando.substring(3).toInt();
      pwm1 = constrain(valor, 0, 255);
      auto_control1 = false;
      Serial.print("PWM Manual Bomba 1: ");
      Serial.println(pwm1);
    }
    
    // Comando: M2:valor = PWM manual bomba 2
    else if (comando.startsWith("M2:")) {
      int valor = comando.substring(3).toInt();
      pwm2 = constrain(valor, 0, 255);
      auto_control2 = false;
      Serial.print("PWM Manual Bomba 2: ");
      Serial.println(pwm2);
    }
    
    // Comando: OFF = apagar ambas bombas
    else if (comando == "OFF") {
      pwm1 = 0;
      pwm2 = 0;
      auto_control1 = false;
      auto_control2 = false;
      Serial.println("Bombas apagadas");
    }
  }
}

void MostrarDatos(float t1, float t2, float t3) {
  Serial.println("========================================");
  
  // Temperaturas
  Serial.println("--- TEMPERATURAS ---");
  Serial.print("Sensor 1 (pin11): ");
  Serial.print(t1, 2);
  Serial.println(" °C");
  
  Serial.print("Sensor 2 (pin12): ");
  Serial.print(t2, 2);
  Serial.println(" °C");
  
  Serial.print("Sensor 3 (pin4): ");
  Serial.print(t3, 2);
  Serial.println(" °C");
  
  // Caudalímetros
  Serial.println("\n--- CAUDALIMETROS ---");
  Serial.print("Caudal 1 (pin2): ");
  Serial.print(caudal1_L_m, 3);
  Serial.print(" L/min  |  Vol: ");
  Serial.print(volumen1, 3);
  Serial.println(" L");
  
  Serial.print("Caudal 2 (pin3): ");
  Serial.print(caudal2_L_m, 3);
  Serial.print(" L/min  |  Vol: ");
  Serial.print(volumen2, 3);
  Serial.println(" L");
  
  // Estado de las bombas y PWM
  Serial.println("\n--- BOMBAS ---");
  Serial.print("Bomba 1: ");
  Serial.print(pwm1 > 0 ? "ENCENDIDA" : "APAGADA");
  Serial.print(" | PWM: ");
  Serial.print(pwm1);
  Serial.print(" (");
  Serial.print((pwm1 * 100.0) / 255.0, 1);
  Serial.print("%) | Modo: ");
  Serial.println(auto_control1 ? "AUTO" : "MANUAL");
  
  Serial.print("Bomba 2: ");
  Serial.print(pwm2 > 0 ? "ENCENDIDA" : "APAGADA");
  Serial.print(" | PWM: ");
  Serial.print(pwm2);
  Serial.print(" (");
  Serial.print((pwm2 * 100.0) / 255.0, 1);
  Serial.print("%) | Modo: ");
  Serial.println(auto_control2 ? "AUTO" : "MANUAL");
  
  // Setpoints (solo si modo automático)
  if (auto_control1) {
    Serial.print("Setpoint 1: ");
    Serial.print(caudal_setpoint1, 2);
    Serial.print(" L/min | Error: ");
    Serial.println(error1, 3);
  }
  
  if (auto_control2) {
    Serial.print("Setpoint 2: ");
    Serial.print(caudal_setpoint2, 2);
    Serial.print(" L/min | Error: ");
    Serial.println(error2, 3);
  }
  
  Serial.println("========================================\n");
}

void setup() {
  Serial.begin(115200);
  Serial.println("Sistema de control de caudal iniciado");
  Serial.println("Comandos:");
  Serial.println("  r = reset volumenes");
  Serial.println("  S1:X = setpoint bomba 1 (L/min)");
  Serial.println("  S2:X = setpoint bomba 2 (L/min)");
  Serial.println("  M1:X = PWM manual bomba 1 (0-255)");
  Serial.println("  M2:X = PWM manual bomba 2 (0-255)");
  Serial.println("  OFF = apagar bombas\n");

  // Configuración Bombas
  pinMode(R_EN1, OUTPUT);
  pinMode(L_EN1, OUTPUT);
  pinMode(RPWM1, OUTPUT);
  pinMode(R_EN2, OUTPUT);
  pinMode(L_EN2, OUTPUT);
  pinMode(RPWM2, OUTPUT);

  digitalWrite(R_EN1, HIGH);
  digitalWrite(L_EN1, HIGH);
  digitalWrite(R_EN2, HIGH);
  digitalWrite(L_EN2, HIGH);

  analogWrite(RPWM1, 0);
  analogWrite(RPWM2, 0);

  // Configuración Sensores de Temperatura
  sensor1.begin();
  sensor2.begin();
  sensor3.begin();
  
  sensor1.setResolution(9);
  sensor2.setResolution(9);
  sensor3.setResolution(9);

  // Configuración Caudalímetros
  pinMode(PinSensor1, INPUT);
  pinMode(PinSensor2, INPUT);
  attachInterrupt(digitalPinToInterrupt(PinSensor1), ContarPulsos1, RISING);
  attachInterrupt(digitalPinToInterrupt(PinSensor2), ContarPulsos2, RISING);

  tiempoAnterior = millis();
}

void loop() {
  unsigned long tiempoActual = millis();
  
  // Procesar comandos seriales
  ProcesarComandoSerial();

  // Actualizar cada intervaloMuestreo
  if (tiempoActual - tiempoAnterior >= intervaloMuestreo) {
    float dt_s = (tiempoActual - tiempoAnterior) / 1000.0;
    tiempoAnterior = tiempoActual;
    
    // Calcular caudales y volúmenes
    CalcularCaudalesYVolumenes(dt_s);
    
    // Control PID de caudal
    ControlPID_Bomba1(dt_s);
    ControlPID_Bomba2(dt_s);
    
    // Aplicar PWM
    analogWrite(RPWM1, pwm1);
    analogWrite(RPWM2, pwm2);
    
    // Leer temperaturas
    sensor1.requestTemperatures();
    sensor2.requestTemperatures();
    sensor3.requestTemperatures();

    float t1 = sensor1.getTempCByIndex(0);
    float t2 = sensor2.getTempCByIndex(0);
    float t3 = sensor3.getTempCByIndex(0);

    // Mostrar datos
    MostrarDatos(t1, t2, t3);
  }
}