#include <WiFi.h>
#include <PubSubClient.h>
#include <DHT.h>
#include <OneWire.h>
#include <DallasTemperature.h>

#define DHT22_PIN  15 // ESP32 pin GPIO21 connected to DHT22 sensor
#define temp_ds18b20  13
#define ledPin 2
#define TIME_TO_SLEEP  900
#define uS_TO_S_FACTOR 1000000


// Replace the SSID/Password details as per your wifi router
const char* ssid = "Vodafone-9BBF01";
const char* password = "Q6Fdc7eGN5";

// Replace your MQTT Broker IP address here:
const char* mqtt_server = "192.168.1.130";

WiFiClient espClient;
PubSubClient client(espClient);

DHT dht22(DHT22_PIN, DHT22);

OneWire oneWire(temp_ds18b20);
DallasTemperature DS18B20(&oneWire);

long lastMsg = 0;
float temp_tomatos;
int hum_tomatos;


void blink_led(unsigned int times, unsigned int duration){
  for (int i = 0; i < times; i++) {
    digitalWrite(ledPin, HIGH);
    delay(duration);
    digitalWrite(ledPin, LOW); 
    delay(200);
  }
}

void setup_wifi() {
  delay(50);
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);

  WiFi.begin(ssid, password);

  int c=0;
  while (WiFi.status() != WL_CONNECTED) {
    blink_led(2,200); //blink LED twice (for 200ms ON time) to indicate that wifi not connected
    delay(1000); //
    Serial.print(".");
    c=c+1;
    if(c>10){
        ESP.restart(); //restart ESP after 10 seconds
    }
  }

  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
  
}

void connect_mqttServer() {
  // Loop until we're reconnected
  while (!client.connected()) {

        //first check if connected to wifi
        if(WiFi.status() != WL_CONNECTED){
          //if not connected, then first connect to wifi
          setup_wifi();
        }

        //now attemt to connect to MQTT server
        Serial.print("Attempting MQTT connection...");
        // Attempt to connect
        if (client.connect("ESP32_client1")) { // Change the name of client here if multiple ESP32 are connected
          //attempt successful
          Serial.println("connected");
          // Subscribe to topics here
          client.subscribe("rpi/broadcast");
          //client.subscribe("rpi/xyz"); //subscribe more topics here
          
        } 
        else {
          //attempt not successful
          Serial.print("failed, rc=");
          Serial.print(client.state());
          Serial.println(" trying again in 2 seconds");
    
          blink_led(3,200); //blink LED three times (200ms on duration) to show that MQTT server connection attempt failed
          // Wait 2 seconds before retrying
          delay(2000);
        }
  }
  
}

//this function will be executed whenever there is data available on subscribed topics
void callback(char* topic, byte* message, unsigned int length) {
  Serial.print("Message arrived on topic: ");
  Serial.print(topic);
  Serial.print(". Message: ");
  String messageTemp;
  
  for (int i = 0; i < length; i++) {
    Serial.print((char)message[i]);
    messageTemp += (char)message[i];
  }
  Serial.println();

  // Check if a message is received on the topic "rpi/broadcast"
  if (String(topic) == "rpi/broadcast") {
      if(messageTemp == "10"){
        Serial.println("Action: blink LED");
        blink_led(1,1250); //blink LED once (for 1250ms ON time)
      }
  }

  //Similarly add more if statements to check for other subscribed topics 
}

void setup() {
  pinMode(ledPin, OUTPUT);
  Serial.begin(115200);

  setup_wifi();
  client.setServer(mqtt_server,1883);//1883 is the default port for MQTT server
  client.setCallback(callback);
  dht22.begin(); // initialize the DHT22 sensor
  DS18B20.begin();
}

void loop() {
  
  if (!client.connected()) {
    connect_mqttServer();
  }
  client.loop();

  hum_tomatos = analogRead(4);

  DS18B20.requestTemperatures();       // send the command to get temperatures

  // read humidity
  float humi_dht  = dht22.readHumidity();
  // read temperature in Celsius
  float temp_dht = dht22.readTemperature();
  // Tomatos's sensors
  temp_tomatos = DS18B20.getTempCByIndex(0); 
  
  Serial.println(temp_tomatos);
  Serial.println(hum_tomatos);
  Serial.println("");

  hum_tomatos = map(hum_tomatos, 1020, 500, 0, 100);//4100, 1500, 0, 100);

  Serial.println(hum_tomatos);
  Serial.println("");

  char humi_dht_str[8];
  dtostrf(humi_dht, 1, 2, humi_dht_str);
  char temp_dht_str[8];
  dtostrf(temp_dht, 1, 2, temp_dht_str);
  char temp_tomatos_str[8];
  dtostrf(temp_tomatos, 1, 2, temp_tomatos_str);
  char hum_tomatos_str[8];
  dtostrf(hum_tomatos, 1, 2, hum_tomatos_str);

  client.publish("esp32/temperature/external", temp_dht_str); //topic name (to which this ESP32 publishes its data). 88 is the dummy value.
  client.publish("esp32/humidity/external", humi_dht_str);
  client.publish("esp32/temperature/tomatos", temp_tomatos_str);
  client.publish("esp32/humidity/tomatos", hum_tomatos_str);

  delay(500);

  esp_sleep_enable_timer_wakeup(TIME_TO_SLEEP * uS_TO_S_FACTOR);
  esp_deep_sleep_start();

  delay(500);
    
}
