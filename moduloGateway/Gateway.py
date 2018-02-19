from gerenciador.Gerenciador import Gerenciador
    

class Gateway:

	def __init__(self):
		self.gerenciador = Gerenciador(self)
		self.gerenciador.start()

	def msg(self):
		print(" MSG ");	
		self.gerenciador.enviarMensagem('retorno de mensagem')