# import classes
import json
# import Gateway
import Gateway
# import classe de tipo
from avaliador.Tipo import Tipo
# import classe de operação
from avaliador.Operacao import Operacao

class Avaliador:
    

    def __init__(self, gateway):
        self.gateway = gateway
        self.tipo = Tipo()
        self.operacao = Operacao()
       
    def avaliar(self, contextoAtual, contextoRegra):
        print("##### Avaliando contexto #####")
        print("Contexto Atual : %s" % str(contextoAtual))
        print("Contexto da Regra : %s" % str(contextoRegra))

        # verifica se o usuario tem acesso garantido independente de contexto
        if contextoRegra == None:
            return True
        else:
            avaliacao = False
            contextoRegra = json.loads(contextoRegra)           
            for c in contextoRegra:
                
                # convertendo os valores de acordo com o seu tipo
                valorConvertidoRegra,valorConvertidoAtual = getattr(self.tipo,c['Tipo'])(c['Valor'], contextoAtual[c['Tipo']], c['Recurso'])
                
                # avaliando os valores de acordo com a operacao
                avaliacao = getattr(self.operacao,c['Operacao'])(valorConvertidoRegra,valorConvertidoAtual)                
                print("Avaliação : " + str(avaliacao))
                if avaliacao == False:
                    break

            return avaliacao
