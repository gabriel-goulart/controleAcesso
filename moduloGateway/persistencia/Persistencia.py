import pymysql

#import configs
from Config import BD_INFO
#import classes
import Gateway

class Persistencia:

    def __init__(self, gateway):
        self.gateway = gateway
        # conexao com o banco de dados
        self.bd = pymysql.connect(BD_INFO['host'],BD_INFO['usuario'],BD_INFO['senha'],BD_INFO['database'])
        self.cursor = self.bd.cursor()

    # obtem as informacoes associadas ao usuario e ao ambiente
    def getInformacoesAcesso(self, usuario, ambiente):
        retorno = {}
        retorno['ambiente'] = ambiente
        retorno['usuario'] = usuario

        query = "SELECT pa.id_papel_de_ambiente, pa.nome_papel_de_ambiente, up.id_papel_de_usuario, pu.nome_papel_de_usuario, ra.contexto FROM Regra_De_Acesso ra INNER JOIN Ambiente a ON a.id_ambiente = "+ambiente+" INNER JOIN Papel_De_Ambiente pa ON pa.id_papel_de_ambiente = a.id_papel_de_ambiente INNER JOIN Usuario_Papel up ON up.tag_usuario = \""+usuario+"\" AND up.id_papel_de_ambiente = pa.id_papel_de_ambiente INNER JOIN Papel_De_Usuario pu ON pu.id_papel_de_usuario = up.id_papel_de_usuario WHERE ra.id_papel_de_ambiente = pa.id_papel_de_ambiente AND ra.id_papel_de_usuario = pu.id_papel_de_usuario;"        
        try:
            print("##### Buscando informações no banco de dados #####")            
            self.cursor.execute(query)
            result = self.cursor.fetchone()            
            if result == None :
                retorno = {}
            else:
                retorno['id_papel_de_ambiente']     = result[0]
                retorno['nome_papel_de_ambiente']   = result[1]
                retorno['id_papel_de_usuario']      = result[2]
                retorno['nome_papel_de_usuario']    = result[3] 
                retorno['contexto']                 = result[4]   
        except:
            retorno = {}
        return retorno    