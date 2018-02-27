import paho.mqtt.client as mqtt
#import configs
from Config import MQTT_INFO,MQTT_TOPICOS_GERAIS
#import classes
import Gateway

class Gerenciador:

    

    def __init__(self, gateway):
        self.gateway = gateway
        self.MQTT_ADDRESS = MQTT_INFO['host']
        self.MQTT_PORT =  MQTT_INFO['porta']
        self.MQTT_TIMEOUT =  MQTT_INFO['timeout']

    def start(self):
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_subscribe = self.on_subscribe
        self.client.on_message = self.on_message
        self.client.connect(self.MQTT_ADDRESS, self.MQTT_PORT,self. MQTT_TIMEOUT)
        self.client.subscribe('TagIdentificada')
        self.client.loop_forever()

    def enviarMensagem(self,info):
        print('##### Enviando Mensagem para o ambiente #####')
        print ('Informação: %s' % str(info))

        result, mid = self.client.publish(info['ambiente']+"-"+ MQTT_TOPICOS_GERAIS[info['acao']], info['resultado'])
        print('Mensagem enviada ao canal: %d' % mid)
        
    # MQTT METODOS   
    def on_connect(self,client, userdata, flags, rc):
        print('Conectado. Resultado: %s' % str(rc))


    def on_subscribe(self,client, userdata, mid, granted_qos):
        print('Inscrito no tópico: %d' % mid)


    def on_message(self,client, userdata, msg):
        print('##### MENSAGEM RECEBIDA #####') 
        print('Tópico: %s' % msg.topic)

        if msg.topic == 'TagIdentificada':
            info = msg.payload.decode('utf-8')
            print("Mensagem recebida do módulo de ambiente: %s" % info)
            self.gateway.tagIdentificada(info)
        else:
            print('Tópico desconhecido.')



