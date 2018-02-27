
class Operacao:

    def igual(self, valorRegra, valorAtual):
        print("Operação: IGUAL")
        if valorRegra == valorAtual:
            return True
        else:
            return False

    def diferente(self, valorRegra, valorAtual):
        print("Operação: DIFERENTE")
        if valorRegra != valorAtual:
            return True
        else:
            return False        

    def maior (self, valorRegra, valorAtual):
        print("Operação: MAIOR")
        if valorRegra > valorAtual:
            return True 
        else:
            return False

    def menor (self, valorRegra, valorAtual):
        print("Operação: MENOR")
        if valorRegra < valorAtual:
            return True 
        else:
            return False      

    def between(self, valorRegra, valorAtual):
        print("Operação: BETWEEN")
        if valorAtual >= valorRegra[0] and valorAtual <= valorRegra[1]:
            return True
        else:
            return False