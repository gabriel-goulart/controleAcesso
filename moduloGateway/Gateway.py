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
		resultadoAvaliacao = False
		retorno = {}
		acao = None
		# deserializando o json que vem do ambiente
		infoDeserializada = json.loads(info)

		# verificando se o usuario tem uma sessao para o ambiente que esta tentando acessar
		if self.persistencia.temSessao(infoDeserializada['usuario'], infoDeserializada['ambiente']) == False :
			print("##### Usuário entrando no ambiente #####")
			acao = "acessando"
			# contem todas as informações relacionadas ao acesso (usuario, ambiente, papel usuario, papel ambiente, regra de acesso)
			informacoesAcesso = self.persistencia.getInformacoesAcesso(infoDeserializada['usuario'], infoDeserializada['ambiente'])
			
			# verificando se retornou informacoes do banco de dados		
			if informacoesAcesso != None: 
				# montando o contexto atual
				contextoAtual = {}
				contextoAtual['Data'] = time.strftime('%d/%m/%Y')
				contextoAtual['Tempo'] = time.strftime('%H:%M')
				contextoAtual['Recurso'] = infoDeserializada['contexto']
				#print(infoDeserializada['contexto']['3'])
				resultadoAvaliacao = self.avaliador.avaliar(contextoAtual,informacoesAcesso['contexto'])

				if resultadoAvaliacao == True:
					# registrando a sessao para o usuario no ambiente
					if self.persistencia.criarSessao(informacoesAcesso) == False:
						resultadoAvaliacao = False
			else:
				resultadoAvaliacao = False
					
			print("RESULTADO : " + str(resultadoAvaliacao))

			# registrando evento
			
		else:
			print("##### Usuário saindo no ambiente #####")
			acao = "saindo"
			# deletando sessao
			if self.persistencia.deletarSessao(infoDeserializada['usuario'], infoDeserializada['ambiente']) == False:
				resultadoAvaliacao = False
			else:
				resultadoAvaliacao = True

			# registrando evento
		
		# enviando o resultado de volta para o ambiente
		retorno['ambiente'] = infoDeserializada['ambiente']
		retorno['acao'] = acao
		retorno['resultado'] = resultadoAvaliacao
		self.retornoAcesso(retorno)	 	

	def retornoAcesso(self, info):		
		self.gerenciador.enviarMensagem(info)