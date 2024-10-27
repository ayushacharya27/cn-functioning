#include <DHT.h>        // Library for DHT sensor
#include <Wire.h>       // Library for I2C communication
#include <MPU6050.h>    // Library for MPU6050 sensor

// Pin Definitions
#define DHTPIN 2      // DHT sensor pin
#define DHTTYPE DHT11 // DHT sensor type
#define FIRE_PIN 3    // Fire sensor pin
#define SOUND_PIN A0  // Sound sensor analog pin
#define DISTANCE_TRIG 4 // Ultrasonic sensor trigger pin
#define DISTANCE_ECHO 5 // Ultrasonic sensor echo pin
#define LIGHT_PIN 2  // Light sensor analog pin

DHT dht(DHTPIN, DHTTYPE);
MPU6050 mpu;

void setup() {
  Serial.begin(9600); // Start serial communication
  dht.begin();        // Start DHT sensor
  Wire.begin();       // Start I2C
  mpu.initialize();   // Initialize MPU6050 sensor

  // Check if MPU6050 connection is successful
   

  pinMode(FIRE_PIN, INPUT);
  pinMode(SOUND_PIN, INPUT);
  pinMode(DISTANCE_TRIG, OUTPUT);
  pinMode(DISTANCE_ECHO, INPUT);
  pinMode(LIGHT_PIN, INPUT);
}

void loop() {
  // Read Humidity and Temperature from DHT sensor
  float humidity = dht.readHumidity();
  float temperature = dht.readTemperature();

  if (isnan(humidity)) humidity = 0;
  if (isnan(temperature)) temperature = 0;

  // Read Fire sensor (digital)
  int fire = digitalRead(FIRE_PIN);

  // Read Sound sensor (analog)
  int soundLevel = analogRead(SOUND_PIN);

  // Calculate Distance from ultrasonic sensor
  long duration, distance;
  digitalWrite(DISTANCE_TRIG, LOW);
  delayMicroseconds(2);
  digitalWrite(DISTANCE_TRIG, HIGH);
  delayMicroseconds(10);
  digitalWrite(DISTANCE_TRIG, LOW);
  duration = pulseIn(DISTANCE_ECHO, HIGH);
  distance = duration * 0.034 / 2;

  // Read Light sensor (analog)
  int light = digitalRead(LIGHT_PIN);

  // Read Accelerometer and Gyroscope values from MPU6050
  int16_t accelX, accelY, accelZ;
  int16_t gyroX, gyroY, gyroZ;

  mpu.getAcceleration(&accelX, &accelY, &accelZ);
  mpu.getRotation(&gyroX, &gyroY, &gyroZ);
  int Accelartion = sqrt(accelX*accelX+ accelY*accelY + accelZ*accelZ);

  // Send sensor data as a JSON-like string over serial
  Serial.print("{");
  Serial.print("\"humidity\":"); Serial.print(humidity);
  Serial.print(", \"temperature\":"); Serial.print(temperature);
  Serial.print(", \"fire\":"); Serial.print(fire);
  Serial.print(", \"sound\":"); Serial.print(soundLevel);
  Serial.print(", \"distance\":"); Serial.print(distance);
  Serial.print(", \"light\":"); Serial.print(light);
  Serial.print(", \"Acceleration\":"); Serial.print(Accelartion);
   
  Serial.print(", \"gyroX\":"); Serial.print(gyroX);
  Serial.print(", \"gyroY\":"); Serial.print(gyroY);
  
  Serial.println("}");

  delay(5000); // Wait before sending the next reading
}
