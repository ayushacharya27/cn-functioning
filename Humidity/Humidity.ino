#include <DHT.h>

#define DHTPIN 2       // Pin connected to the DHT sensor
#define DHTTYPE DHT11  // DHT11 or DHT22

DHT dht(DHTPIN, DHTTYPE);

void setup() {
  Serial.begin(9600);
  dht.begin();
}

void loop() {
  float temperature = dht.readTemperature();
  float humidity = dht.readHumidity();

  if (isnan(temperature) || isnan(humidity)) {
    Serial.println("Failed to read from DHT sensor!");
  } else {
    Serial.print("Temperature: ");
    Serial.print(temperature);
    Serial.print("°C ");
    Serial.print("Humidity: ");
    Serial.print(humidity);
    Serial.println("%");
  }

  delay(2000);  // Wait a few seconds between measurements
}
