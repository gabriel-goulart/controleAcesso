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
            print("##### Buscando informações da regra de acesso no banco de dados #####")            
            self.cursor.execute(query)
            result = self.cursor.fetchone()            
            if result == None :
                retorno = None
            else:
                retorno['id_papel_de_ambiente']     = result[0]
                retorno['nome_papel_de_ambiente']   = result[1]
                retorno['id_papel_de_usuario']      = result[2]
                retorno['nome_papel_de_usuario']    = result[3] 
                retorno['contexto']                 = result[4]
                retorno['usuario']                  = usuario
                retorno['ambiente']                 = ambiente   
        except:
            print("##### Buscando informações da regra de acesso no banco de dados - ERRO #####")
            retorno = None
        return retorno

    def temSessao(self, usuario, ambiente):
        retorno = None
        query = "SELECT * FROM Sessao WHERE tag_usuario = \""+usuario+"\" AND id_ambiente = "+ambiente

        try:
            print("##### Buscando informações da sessão no banco de dados #####")            
            self.cursor.execute(query)
            result = self.cursor.fetchone()

            if result == None :
                retorno = None
            else:
                retorno = {}
                retorno['usuario']                  = result[0]
                retorno['ambiente']                 = result[1]
                retorno['id_papel_de_ambiente']     = result[2]
                retorno['id_papel_de_usuario']      = result[3]
                               
             
        except:
            print("##### Buscando informações da sessão no banco de dados  - ERRO #####")
            
        return retorno

    def criarSessao(self, info):
        query = "INSERT INTO Sessao (tag_usuario, id_ambiente, id_papel_de_ambiente, id_papel_de_usuario, datetime)  VALUES ( \""+info['usuario']+"\", "+str(info['ambiente'])+", "+str(info['id_papel_de_ambiente'])+", "+str(info['id_papel_de_usuario'])+", NOW()) "

        try:
            print ("##### Registrando sessão para o usuário no ambiente #####")
            self.cursor.execute(query)
            self.bd.commit()
            return True
        except:
            print ("##### Registrando sessão para o usuário no ambiente - ERRO #####")
            self.bd.rollback()
            return False

    def deletarSessao(self, usuario, ambiente):
        query = "DELETE FROM Sessao WHERE tag_usuario = \""+usuario+"\" AND id_ambiente = "+str(ambiente)

        try:
            print ("##### Deletando sessão do usuário no ambiente #####")
            self.cursor.execute(query)
            self.bd.commit()
            return True
        except:
            print ("##### Deletando sessão do usuário no ambiente - ERRO #####")
            self.bd.rollback()
            return False
    
    def registrarEvento(self, *args):
        tag_usuario = args[0]
        id_ambiente = args[1]
        id_papel_de_ambiente = args[2]
        id_papel_de_usuario = args[3]
        contexto_regra = args[4]
        contexto_ambiente = args[5]
        acao = args[6]
        resultado = args[7]

        query = "INSERT INTO Evento (tag_usuario, id_ambiente, id_papel_de_ambiente, id_papel_de_usuario,contexto_regra,contexto_ambiente,acao,resultado, datetime)  VALUES ( \""+tag_usuario+"\", "+str(id_ambiente)+", "+str(id_papel_de_ambiente)+", "+str(id_papel_de_usuario)+",\""+contexto_regra+"\",\""+contexto_ambiente+"\",\""+str(acao)+"\",\""+str(resultado)+"\", NOW()) "
        
        try:
            print ("##### Registrando evento#####")
            self.cursor.execute(query)
            self.bd.commit()
            return True
        except:
            print ("##### Registrando evento - ERRO #####")
            self.bd.rollback()
            return False

            