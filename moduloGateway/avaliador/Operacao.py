
class Operacao:

    def igual(self, valorRegra, valorAtual):
        print("IGUAL")
        if valorRegra == valorAtual:
            return True
        else:
            return False

    def diferente(self, valorRegra, valorAtual):
        print("DIFERENTE")
        if valorRegra != valorAtual:
            return True
        else:
            return False        

    def maior (self, valorRegra, valorAtual):
        print("MAIOR")
        if valorRegra > valorAtual:
            return True 
        else:
            return False

    def menor (self, valorRegra, valorAtual):
        print("MENOR")
        if valorRegra < valorAtual:
            return True 
        else:
            return False      

    def between(self, valorRegra, valorAtual):
        print("BETWEEN")
        if valorAtual >= valorRegra[0] and valorAtual <= valorRegra[1]:
            return True
        else:
            return False