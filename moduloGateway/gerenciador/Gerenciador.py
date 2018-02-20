import paho.mqtt.client as mqtt

import Gateway

class Gerenciador:

    

    def __init__(self, gateway):
        self.gateway = gateway
        self.MQTT_ADDRESS = '192.168.1.100'
        self.MQTT_PORT = 1883
        self.MQTT_TIMEOUT = 60

    def start(self):
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_subscribe = self.on_subscribe
        self.client.on_message = self.on_message
        self.client.connect(self.MQTT_ADDRESS, self.MQTT_PORT,self. MQTT_TIMEOUT)
        self.client.subscribe('conect')
        self.client.loop_forever()

    def enviarMensagem(self,msg):
        result, mid = self.client.publish('access', msg)
        print('Mensagem enviada ao canal: %d' % mid)
        
    # MQTT METODOS   
    def on_connect(self,client, userdata, flags, rc):
        print('Conectado. Resultado: %s' % str(rc))


    def on_subscribe(self,client, userdata, mid, granted_qos):
        print('Inscrito no tópico: %d' % mid)


    def on_message(self,client, userdata, msg):
        print('Mensagem recebida no tópico: %s' % msg.topic)

        if msg.topic == 'conect':
            info = msg.payload.decode('utf-8')
            print("Mensagem: %s" % info)
            self.gateway.acessoSolicitado(info)
        else:
            print('Tópico desconhecido.')



