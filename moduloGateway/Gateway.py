#import classes
import json
import time
# import classe Grenciador
from gerenciador.Gerenciador import Gerenciador
# import classe Avaliador
from avaliador.Avaliador import Avaliador
# import classe Persistencia
from persistencia.Persistencia import Persistencia    

class Gateway:

	def __init__(self):

		# sub módulo de avaliação da politica de acesso
		self.avaliador = Avaliador(self)
		
		# sub módulo de persistência
		self.persistencia = Persistencia(self)
		#infoAcesso = self.persistencia.getInformacoesAcesso("e1be95a5", "2")
		#print(infoAcesso)
		# sub módulo de gerenciamento
		self.gerenciador = Gerenciador(self)
		self.gerenciador.start()

	def tagIdentificada(self, info):
		infoDeserializada = json.loads(info)
		#contem todas as informações relacionadas ao acesso (usuario, ambiente, papel usuario, papel ambiente, regra de acesso)
		informacoesAcesso = self.persistencia.getInformacoesAcesso(infoDeserializada['usuario'], infoDeserializada['ambiente'])
		
		# montando o contexto atual
		contextoAtual = {}
		contextoAtual['Data'] = time.strftime('%d/%m/%Y')
		contextoAtual['Tempo'] = time.strftime('%H:%M')
		contextoAtual['Recurso'] = infoDeserializada['contexto']
		#print(infoDeserializada['contexto']['3'])
		resultadoAvaliacao = self.avaliador.avaliar(contextoAtual,informacoesAcesso['contexto'])
		print("RESULTADO : " + str(resultadoAvaliacao))

	def msg(self):
		print(" MSG ");	
		self.gerenciador.enviarMensagem('retorno de mensagem')