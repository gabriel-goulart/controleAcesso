#import Libs
import json

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

		# sub módulo de gerenciamento
		self.gerenciador = Gerenciador(self)
		self.gerenciador.start()

	def acessoSolicitado(self, info):
		infoDeserializada = json.loads(info)
		#contem todas as informações relacionadas ao acesso (usuario, ambiente, papel usuario, papel ambiente, regra de acesso)
		informacoesAcesso = self.persistencia.getInformacoesAcesso(infoDeserializada['usuario'], infoDeserializada['ambiente'])

	def msg(self):
		print(" MSG ");	
		self.gerenciador.enviarMensagem('retorno de mensagem')