#import classes
import time

class Tipo:

   # convertendo as datas
    def Data(self, *args):
        print("#### Tipo: DATA ######")
        dataRegra = args[0]
        dataAtual = args [1]       
        if ',' in dataRegra:           
            dataRegra1, dataRegra2 = dataRegra.split(",")
            dataRegra1 = time.strptime(dataRegra1,'%d/%m/%Y')
            dataRegra2 = time.strptime(dataRegra2,'%d/%m/%Y')

            dataRegra = [dataRegra1,dataRegra2]
            dataAtual = time.strptime(dataAtual,'%d/%m/%Y')
            return dataRegra,dataAtual            
        else:            
            dataRegra = time.strptime(dataRegra,'%d/%m/%Y')
            dataAtual = time.strptime(dataAtual,'%d/%m/%Y')
            return dataRegra,dataAtual
    
    # convertendo os tempos
    def Horario(self, *args):
        print("#### Tipo: Horario ######")
        tempoRegra = args[0]
        tempoAtual = args[1]
        if ',' in tempoRegra:            
            tempoRegra1, tempoRegra2 = tempoRegra.split(",")
            tempoRegra1 = time.strptime(tempoRegra1,'%H:%M')
            tempoRegra2 = time.strptime(tempoRegra2,'%H:%M')

            tempoRegra = [tempoRegra1,tempoRegra2]
            tempoAtual = time.strptime(tempoAtual,'%H:%M')
            return tempoRegra,tempoAtual            
        else:           
            tempoRegra = time.strptime(tempoRegra,'%H:%M')
            tempoAtual = time.strptime(tempoAtual,'%H:%M')
            return tempoRegra,tempoAtual

    def Recurso(self, *args):
        print("#### Tipo: RECURSO ######")
        recursoRegra = args[0]
        recursoAtual = args[1]
        idRecurso = args[2]
        
       
        if type(recursoRegra) == str:

            recursoAtual = recursoAtual[idRecurso]
            if ',' in recursoRegra:
                recursoRegra1, recursoRegra2 = recursoRegra.split(",")
                recursoRegra = [float(recursoRegra1),float(recursoRegra2)]
                recursoAtual = float(recursoAtual)

            return recursoRegra, recursoAtual
        else:            
            recursoAtual = recursoAtual[idRecurso]           
            return float(recursoRegra), float(recursoAtual)       