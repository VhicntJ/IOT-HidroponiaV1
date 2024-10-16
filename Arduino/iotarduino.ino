// Incluye las bibliotecas necesarias
#include <DHT.h>

// Definición de pines
#define DHTPIN 5          // Pin donde está conectado el DHT11
#define DHTTYPE DHT11     // Define el tipo de sensor DHT

#define TRIGGER_PIN 3     // Pin Trigger del HC-SR04
#define ECHO_PIN 4        // Pin Echo del HC-SR04

#define EC_SENSOR_PIN A0  // Pin analógico para el sensor EC
#define PH_SENSOR_PIN A1  // Pin analógico para el sensor de pH

// Inicializa el sensor DHT11
DHT dht(DHTPIN, DHTTYPE);

// Variables para el sensor HC-SR04
long duration;
float distance_cm;

// Variables para el sensor EC
int ecRawValue;
float ecVoltage;
float ecConductivity; // En µS/cm, por ejemplo

// Variables para el sensor de pH
int phRawValue;
float phVoltage;
float phValue; // Valor de pH calculado

void setup() {
  // Inicia la comunicación serial
  Serial.begin(9600);
  Serial.println("Iniciando lectura de sensores...");

  // Inicia el sensor DHT11
  dht.begin();

  // Configura los pines del HC-SR04
  pinMode(TRIGGER_PIN, OUTPUT);
  pinMode(ECHO_PIN, INPUT);

  // Configura los pines de los sensores analógicos
  pinMode(EC_SENSOR_PIN, INPUT);
  pinMode(PH_SENSOR_PIN, INPUT);

  // Nota: Asegúrate de conectar correctamente los sensores antes de leerlos
}

// Función para validar el rango de las lecturas
bool isValidReading(float value, float min, float max) {
  return (value >= min && value <= max);
}

void loop() {
  // --- Lectura del sensor HC-SR04 ---
  // Limpia el pin Trigger
  digitalWrite(TRIGGER_PIN, LOW);
  delayMicroseconds(2);
  
  // Genera un pulso de 10µs en Trigger
  digitalWrite(TRIGGER_PIN, HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIGGER_PIN, LOW);
  
  // Lee el tiempo que tarda el pulso en regresar
  duration = pulseIn(ECHO_PIN, HIGH);
  
  // Calcula la distancia en centímetros
  distance_cm = duration * 0.034 / 2;

  // --- Lectura del sensor DHT11 ---
  float humidity = dht.readHumidity();
  float temperatureDHT = dht.readTemperature();

  // Verifica si la lectura del DHT11 falló
  if (isnan(humidity) || isnan(temperatureDHT)) {
    Serial.println("¡Error al leer el DHT11!");
  }

  // --- Lectura del sensor EC ---
  ecRawValue = analogRead(EC_SENSOR_PIN);
  ecVoltage = (ecRawValue / 1024.0) * 5.0; // Convierte a voltaje (asumiendo Vcc = 5V)
  
  // Calcular la conductividad eléctrica
  // Este cálculo depende de la calibración del sensor y puede requerir ajuste
  // Aquí se asume una calibración lineal simple
  ecConductivity = ecVoltage * 200.0; // Ajusta el factor según tu calibración

  // --- Lectura del sensor de pH ---
  phRawValue = analogRead(PH_SENSOR_PIN);
  phVoltage = (phRawValue / 1024.0) * 5.0; // Convierte a voltaje (asumiendo Vcc = 5V)
  
  // Calcular el valor de pH
  // Ajusta los coeficientes según la calibración de tu sensor
  float slope = 3.0;      // Ejemplo de pendiente (determinado por calibración)
  float intercept = -2.5; // Ejemplo de intercepto (determinado por calibración)
  
  phValue = slope * phVoltage + intercept;
  
  // Validar Lectura de pH
  if (!isValidReading(phValue, 0.0, 14.0)) {
    Serial.println("¡Lectura de pH fuera de rango!");
  }

  // Validar Lectura de EC
  if (!isValidReading(ecConductivity, 0.0, 2000.0)) { // Ajusta según tu sensor
    Serial.println("¡Lectura de EC fuera de rango!");
  }

  // Validar Lectura de Temperatura
  if (!isValidReading(temperatureDHT, -10.0, 60.0)) { // Ajusta según tu entorno
    Serial.println("¡Lectura de temperatura fuera de rango!");
  }

  // Validar Lectura de Humedad
  if (!isValidReading(humidity, 0.0, 100.0)) {
    Serial.println("¡Lectura de humedad fuera de rango!");
  }

  // Validar Lectura de Distancia
  if (!isValidReading(distance_cm, 0.0, 400.0)) { // HC-SR04 rango típico 2cm - 400cm
    Serial.println("¡Lectura de distancia fuera de rango!");
  }

  // --- Mostrar todos los valores en el Serial Monitor ---
  Serial.println("========================================");
  
  Serial.print("Distancia (HC-SR04): ");
  Serial.print(distance_cm);
  Serial.println(" cm");

  Serial.print("Humedad (DHT11): ");
  Serial.print(humidity);
  Serial.println(" %");

  Serial.print("Temperatura DHT11: ");
  Serial.print(temperatureDHT);
  Serial.println(" *C");

  Serial.print("Conductividad Eléctrica (EC): ");
  Serial.print(ecConductivity);
  Serial.println(" µS/cm"); // Asegúrate de que la unidad sea correcta según tu sensor

  Serial.print("pH: ");
  Serial.print(phValue);
  Serial.println(" pH");

  Serial.println("========================================\n");

  // --- Mostrar todos los valores para recoleccion de datos para graficos ---
  Serial.print(distance_cm);
  Serial.print(",");        // Separador para Serial Plotter
  Serial.print(humidity);
  Serial.print(",");
  Serial.print(temperatureDHT);
  Serial.print(",");
  Serial.print(ecConductivity);
  Serial.print(",");
  Serial.println(phValue);  // Fin de línea

  // Espera 2 segundos antes de la siguiente lectura
  delay(2000);
}
