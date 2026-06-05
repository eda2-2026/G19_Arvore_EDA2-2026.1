class No:
    def __init__(self, matricula, nome, especialidade, data_consulta):
        self.matricula = matricula 
        self.nome = nome
        self.especialidade = especialidade
        self.data_consulta = data_consulta
        self.cor = "VERMELHO"
        self.pai = None
        self.esq = None
        self.dir = None

class ArvoreVermelhoPreto:
    def __init__(self):

        self.NIL = No(0, "", "", "")
        self.NIL.cor = "PRETO"
        self.NIL.esq = None
        self.NIL.dir = None
        self.raiz = self.NIL

    def _rotacao_esquerda(self, x):
        y = x.dir
        x.dir = y.esq
        if y.esq != self.NIL:
            y.esq.pai = x
        y.pai = x.pai
        if x.pai == self.NIL:
            self.raiz = y
        elif x == x.pai.esq:
            x.pai.esq = y
        else:
            x.pai.dir = y
        y.esq = x
        x.pai = y

    def _rotacao_direita(self, x):
        y = x.esq
        x.esq = y.dir
        if y.dir != self.NIL:
            y.dir.pai = x
        y.pai = x.pai
        if x.pai == self.NIL:
            self.raiz = y
        elif x == x.pai.dir:
            x.pai.dir = y
        else:
            x.pai.esq = y
        y.dir = x
        x.pai = y

    def inserir(self, matricula, nome, especialidade, data_consulta):
        novo_no = No(matricula, nome, especialidade, data_consulta)
        novo_no.pai = None
        novo_no.esq = self.NIL
        novo_no.dir = self.NIL

        y = self.NIL
        x = self.raiz

        while x != self.NIL:
            y = x
            if novo_no.matricula < x.matricula:
                x = x.esq
            else:
                x = x.dir

        novo_no.pai = y
        if y == self.NIL:
            self.raiz = novo_no
        elif novo_no.matricula < y.matricula:
            y.esq = novo_no
        else:
            y.dir = novo_no

        if novo_no.pai == self.NIL:
            novo_no.cor = "PRETO"
            return

        if novo_no.pai.pai == self.NIL:
            return

        self._consertar_insercao(novo_no)

    def _consertar_insercao(self, k):
        while k.pai.cor == "VERMELHO":
            if k.pai == k.pai.pai.esq:
                tio = k.pai.pai.dir

                if tio.cor == "VERMELHO":
                    tio.cor = "PRETO"
                    k.pai.cor = "PRETO"
                    k.pai.pai.cor = "VERMELHO"
                    k = k.pai.pai
                else:

                    if k == k.pai.dir:
                        k = k.pai
                        self._rotacao_esquerda(k)

                    k.pai.cor = "PRETO"
                    k.pai.pai.cor = "VERMELHO"
                    self._rotacao_direita(k.pai.pai)
            else:
                tio = k.pai.pai.esq

                if tio.cor == "VERMELHO":
                    tio.cor = "PRETO"
                    k.pai.cor = "PRETO"
                    k.pai.pai.cor = "VERMELHO"
                    k = k.pai.pai
                else:

                    if k == k.pai.esq:
                        k = k.pai
                        self._rotacao_direita(k)

                    k.pai.cor = "PRETO"
                    k.pai.pai.cor = "VERMELHO"
                    self._rotacao_esquerda(k.pai.pai)
            
            if k == self.raiz:
                break
        
        self.raiz.cor = "PRETO"

    def buscar(self, matricula):
        return self._buscar_recursivo(self.raiz, matricula)

    def _buscar_recursivo(self, no, matricula):
        if no == self.NIL or matricula == no.matricula:
            return no
        
        if matricula < no.matricula:
            return self._buscar_recursivo(no.esq, matricula)
        return self._buscar_recursivo(no.dir, matricula)