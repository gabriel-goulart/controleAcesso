#include <MFRC522.h>

#include <SPI.h>
#include <Ethernet.h>
#include <PubSubClient.h>
#include <Ultrasonic.h>


// configurações de rede
byte mac[]    = {  0xDE, 0xED, 0xBA, 0xFE, 0xFE, 0xED }; // endereço MAC
IPAddress ip(192, 168, 1, 120); // ip da interface de rede


// configurações MQTT
#define MQTT_BROKER  "192.168.1.100"  //URL do broker MQTT 
#define MQTT_PORT  1883  // Porta do Broker MQTT
#define MQTT_ID  "ambiente_1"
#define MQTT_TOPICO_SUBSCRIBE_ACESSO "1-Ambiente-Acessando"     //escuta o que é publicado para o topica
#define MQTT_TOPICO_SUBSCRIBE_SAIDA "1-Ambiente-Saindo"     //escuta o que é publicado para o topica
#define MQTT_TOPICO_PUBLISH   "TagIdentificada"      //publica no topico
char message_buff[100];

// configurações RFID
constexpr uint8_t RST_PIN = 9;     
constexpr uint8_t SS_PIN = 8;     
MFRC522 mfrc522(SS_PIN, RST_PIN);  // instancia  MFRC522

// configurações SENSORES
int portaLDR = A5;

// configuração LEDS
int portaLEDVerde = 7;
int portaLEDVermelho = 5;

// configuração do sensor ultrasônico 
#define pino_trigger 2
#define pino_echo 3
Ultrasonic ultrasonic(pino_trigger, pino_echo); //Inicializa o sensor nos pinos definidos acima


EthernetClient ethClient;
PubSubClient mqttClient(ethClient);

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600); // Inicia a serial
  SPI.begin();// Inicia  SPI bus
  pinMode(portaLEDVerde, OUTPUT);
  pinMode(portaLEDVermelho, OUTPUT);
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
            mqttClient.subscribe(MQTT_TOPICO_SUBSCRIBE_ACESSO);
            mqttClient.subscribe(MQTT_TOPICO_SUBSCRIBE_SAIDA);  
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
  String resposta = "";
  for (int i=0;i<length;i++) {
    resposta += (char)payload[i];
  }

  if (resposta == "True"){
    Serial.println("True");
    acendeLedVerde();
  }else{
    Serial.println("False");
    acendeLedVermelho();
  }
}

// envia as informações para o broker
void enviaInformacoes(String msg){
  Serial.println("MENSAGEM ENVIADA");
  msg.toCharArray(message_buff, msg.length()+1);
  mqttClient.publish(MQTT_TOPICO_PUBLISH,message_buff);

}

// retorna o valor do sensor de luminosidade (quanto maior o valor menos luminosidade tem no ambiente)
float getValorLuminosidade(){
  int valor = analogRead(portaLDR);
  return map(valor,0,1023,0,255);
}

// pega o valor do sensor ultrasônico em centímetros 
float getValorSensorUltrasonico(){
    long microsec = ultrasonic.timing();
    return ultrasonic.convert(microsec, Ultrasonic::CM);
}

// acende o led verde por 3 segundos
void acendeLedVerde(){
  digitalWrite(portaLEDVerde, HIGH);

  delay(3000);

  digitalWrite(portaLEDVerde, LOW);
}

// acende o led vermelho por 3 segundos
void acendeLedVermelho(){
  digitalWrite(portaLEDVermelho, HIGH);

  delay(3000);

  digitalWrite(portaLEDVermelho, LOW);
}

// acende todos os leds
void acendeAllLeds(){
  digitalWrite(portaLEDVermelho, HIGH);
  digitalWrite(portaLEDVerde, HIGH);
  delay(1000);
  digitalWrite(portaLEDVermelho, LOW);
  digitalWrite(portaLEDVerde, LOW);

}
void loop() {
  // verificando a conexao com o mqtt
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
       conteudo.concat(String(mfrc522.uid.uidByte[i] < 0x10 ? "0" : ""));
       conteudo.concat(String(mfrc522.uid.uidByte[i], HEX));
    }
    acendeAllLeds();
    float valorSensorUltrasonico = getValorSensorUltrasonico(); 
    Serial.println(valorSensorUltrasonico);
    float valorSensorLuminosidade = getValorLuminosidade();
    Serial.println(valorSensorLuminosidade);
    String pubInfo = "{\"ambiente\": \"1\",\"usuario\": \""+conteudo+"\" , \"contexto\" : {\"1\":"+valorSensorLuminosidade+",\"2\":"+valorSensorUltrasonico+"}}";
    enviaInformacoes(pubInfo);
    delay(5000);
  }

  mqttClient.loop();
  
}
