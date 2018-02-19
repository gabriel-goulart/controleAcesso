#include <MFRC522.h>

#include <SPI.h>
#include <Ethernet.h>
#include <PubSubClient.h>


// configurações de rede
byte mac[]    = {  0xDE, 0xED, 0xBA, 0xFE, 0xFE, 0xED }; // endereço MAC
IPAddress ip(192, 168, 1, 120); // ip da interface de rede
//IPAddress gateway(192,168,0,1);      //Define o gateway
//IPAddress subnet(255, 255, 255, 0); //Define a máscara de rede

// configurações MQTT
#define MQTT_BROKER  "192.168.1.100"  //URL do broker MQTT 
#define MQTT_PORT  1883  // Porta do Broker MQTT
#define MQTT_ID  "ambiente_1"
#define MQTT_TOPICO_SUBSCRIBE "access"     //escuta o que é publicado para o topica
#define MQTT_TOPICO_PUBLISH   "conect"      //publica no topico
char message_buff[100];

// configurações RFID
constexpr uint8_t RST_PIN = 9;     // Configurable, see typical pin layout above
constexpr uint8_t SS_PIN = 8;     // Configurable, see typical pin layout above
MFRC522 mfrc522(SS_PIN, RST_PIN);  // Create MFRC522 instance.


EthernetClient ethClient;
PubSubClient mqttClient(ethClient);

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600); // Inicia a serial
  SPI.begin();// Inicia  SPI bus
  
  setupRfid();
  setupMqtt();
  setupEthernet();
  Serial.println("* Aproxime o cartão *");
}

// inicia o RFID
void setupRfid(){
  mfrc522.PCD_Init(); // Inicia MFRC522
 // mfrc522.PCD_DumpVersionToSerial();
}
// inicia o MQTT
void setupMqtt(){
  Serial.println("* MQTT");
  mqttClient.setServer(MQTT_BROKER, MQTT_PORT);
  mqttClient.setCallback(callbackMqtt);
}

// inicia a rede
void setupEthernet(){
  Serial.println("* ETHERNET ");
  Ethernet.begin(mac, ip);
  Serial.println(Ethernet.localIP());

}

// refaz a conexao com o broker
void reconectMqtt(){
  while (!mqttClient.connected()) 
    {
        Serial.println("* Tentando se conectar ao Broker MQTT: ");
        Serial.println(MQTT_BROKER);
        if (mqttClient.connect("1")) 
        {
            Serial.println("Conectado com sucesso ao broker MQTT!");
            mqttClient.subscribe(MQTT_TOPICO_SUBSCRIBE); 
        } 
        else 
        {
            Serial.println("Falha ao reconectar no broker.");
            Serial.println("Havera nova tentatica de conexao em 2s");
            delay(2000);
        }
    }
}

// recebe os dados do broker
void callbackMqtt(char* topic, byte* payload, unsigned int length) {
  Serial.println("MENSAGEM RECEBIDA");
}

// envia as informações para o broker
void enviaInformacoes(String msg){
  Serial.println("MENSAGEM ENVIADA");
  msg.toCharArray(message_buff, msg.length()+1);
  mqttClient.publish(MQTT_TOPICO_PUBLISH,message_buff);

}

void loop() {
  //Serial.println("* INICIO *");
  // verificando a coneccao com o mqtt
  if (!mqttClient.connected()) {
    reconectMqtt(); // reconeccao do mqtt
  }

  // Look for new cards
  if (mfrc522.PICC_IsNewCardPresent() and mfrc522.PICC_ReadCardSerial()) 
  {
    String conteudo= "";
    byte letra;
    for (byte i = 0; i < mfrc522.uid.size; i++) 
    {
       //Serial.print(mfrc522.uid.uidByte[i] < 0x10 ? " 0" : "");
       //Serial.print(mfrc522.uid.uidByte[i], HEX);
       conteudo.concat(String(mfrc522.uid.uidByte[i] < 0x10 ? " 0" : ""));
       conteudo.concat(String(mfrc522.uid.uidByte[i], HEX));
    }
    String pubInfo = "{\"ambiente\": 1,\"usuario\": \" "+conteudo+"\" , \"contexto\" : [{\"recurso\": 1, \"valor\" : true}]}";
    enviaInformacoes(pubInfo);
    delay(3000);
  }

  mqttClient.loop();
  
}
