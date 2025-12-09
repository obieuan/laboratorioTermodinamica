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

// Velocidades (0-255)
#define SPEED1 200
#define SPEED2 180

// ========== SENSORES DE TEMPERATURA DS18B20 ==========
OneWire oneWire1(11);   // Sensor 1 en pin 11
OneWire oneWire2(12);   // Sensor 2 en pin 12
OneWire oneWire3(4);    // Sensor 3 en pin 4

DallasTemperature sensor1(&oneWire1);
DallasTemperature sensor2(&oneWire2);
DallasTemperature sensor3(&oneWire3);

// ========== CAUDALÍMETROS YF-S201 ==========
// Caudalímetro 1 en pin 2
volatile long NumPulsos1 = 0;
const int PinSensor1 = 2;
float factor_conversion = 7.11;  // K (pulsos a L/min)
float volumen1 = 0.0;
float caudal1_L_m = 0.0;

// Caudalímetro 2 en pin 3
volatile long NumPulsos2 = 0;
const int PinSensor2 = 3;
float volumen2 = 0.0;
float caudal2_L_m = 0.0;

// Control de tiempo para cálculos continuos
unsigned long tiempoAnterior = 0;
const unsigned long intervaloMuestreo = 100; // 100ms = 0.1 segundos

// ========== ISR (Interrupciones) ==========
void ContarPulsos1() {
  NumPulsos1++;
}

void ContarPulsos2() {
  NumPulsos2++;
}

// ========== FUNCIONES AUXILIARES ==========
void CalcularCaudalesYVolumenes(float dt_s) {
  // Leer pulsos de forma segura
  noInterrupts();
  long pulsos1 = NumPulsos1;
  long pulsos2 = NumPulsos2;
  NumPulsos1 = 0;
  NumPulsos2 = 0;
  interrupts();
  
  // Calcular frecuencia en Hz (pulsos / tiempo en segundos)
  float frecuencia1 = pulsos1 / dt_s;
  float frecuencia2 = pulsos2 / dt_s;
  
  // Calcular caudales en L/min
  caudal1_L_m = frecuencia1 / factor_conversion;
  caudal2_L_m = frecuencia2 / factor_conversion;
  
  // Actualizar volúmenes (caudal L/min * tiempo en minutos)
  volumen1 += caudal1_L_m * (dt_s / 60.0);
  volumen2 += caudal2_L_m * (dt_s / 60.0);
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
  
  // Estado de las bombas
  Serial.println("\n--- BOMBAS ---");
  Serial.println("Bomba 1: ENCENDIDA");
  Serial.println("Bomba 2: ENCENDIDA");
  Serial.println("========================================\n");
}

void setup() {
  Serial.begin(115200); // Baudrate más alto para comunicación más rápida
  Serial.println("Sistema de monitoreo continuo iniciado");
  Serial.println("Comandos: 'r' = reset volumenes\n");

  // ---- Configuración Bombas ----
  pinMode(R_EN1, OUTPUT);
  pinMode(L_EN1, OUTPUT);
  pinMode(RPWM1, OUTPUT);
  pinMode(R_EN2, OUTPUT);
  pinMode(L_EN2, OUTPUT);
  pinMode(RPWM2, OUTPUT);

  // Habilitar módulos
  digitalWrite(R_EN1, HIGH);
  digitalWrite(L_EN1, HIGH);
  digitalWrite(R_EN2, HIGH);
  digitalWrite(L_EN2, HIGH);

  // Iniciar bombas apagadas
  analogWrite(RPWM1, 0);
  analogWrite(RPWM2, 0);

  // ---- Configuración Sensores de Temperatura ----
  sensor1.begin();
  sensor2.begin();
  sensor3.begin();
  
  // Configurar resolución más baja para lecturas más rápidas
  sensor1.setResolution(9); // 9 bits = 93.75 ms por lectura
  sensor2.setResolution(9);
  sensor3.setResolution(9);

  // ---- Configuración Caudalímetros ----
  pinMode(PinSensor1, INPUT);
  pinMode(PinSensor2, INPUT);
  attachInterrupt(digitalPinToInterrupt(PinSensor1), ContarPulsos1, RISING);
  attachInterrupt(digitalPinToInterrupt(PinSensor2), ContarPulsos2, RISING);

  tiempoAnterior = millis();
}

void loop() {
  unsigned long tiempoActual = millis();
  
  // Reset de volúmenes por comando serial
  if (Serial.available()) {
    char c = Serial.read();
    if (c == 'r' || c == 'R') {
      volumen1 = 0.0;
      volumen2 = 0.0;
      Serial.println("Volumenes reiniciados a 0 L.\n");
    }
  }

  // ---- Encender ambas bombas ----
  analogWrite(RPWM1, SPEED1);
  analogWrite(RPWM2, SPEED2);

  // Actualizar cada intervaloMuestreo (100ms)
  if (tiempoActual - tiempoAnterior >= intervaloMuestreo) {
    // Calcular dt en segundos
    float dt_s = (tiempoActual - tiempoAnterior) / 1000.0;
    tiempoAnterior = tiempoActual;
    
    // ---- Calcular caudales y volúmenes ----
    CalcularCaudalesYVolumenes(dt_s);
    
    // ---- Leer temperaturas ----
    sensor1.requestTemperatures();
    sensor2.requestTemperatures();
    sensor3.requestTemperatures();

    float t1 = sensor1.getTempCByIndex(0);
    float t2 = sensor2.getTempCByIndex(0);
    float t3 = sensor3.getTempCByIndex(0);

    // ---- Mostrar datos ----
    MostrarDatos(t1, t2, t3);
  }
}