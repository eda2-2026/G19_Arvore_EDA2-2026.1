class No:
    def __init__(self, nome, especialidade, data_consulta, cpf):

        self.nome = nome.lower().strip() 
        self.nome_original = nome.strip() 
        self.especialidade = especialidade
        self.data_consulta = data_consulta
        self.cpf = cpf 
        self.cor = "VERMELHO"
        self.pai = None
        self.esq = None
        self.dir = None

class ArvoreVermelhoPreto:
    def __init__(self):

        self.NIL = No("", "", "", 0)
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

    def inserir(self, nome, especialidade, data_consulta, cpf):
        novo_no = No(nome, especialidade, data_consulta, cpf)
        novo_no.pai = None
        novo_no.esq = self.NIL
        novo_no.dir = self.NIL

        y = self.NIL
        x = self.raiz

        while x != self.NIL:
            y = x
            if novo_no.nome < x.nome:
                x = x.esq
            else:
                x = x.dir

        novo_no.pai = y
        if y == self.NIL:
            self.raiz = novo_no
        elif novo_no.nome < y.nome:
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

    def buscar(self, nome):

        nome_formatado = nome.lower().strip()
        return self._buscar_recursivo(self.raiz, nome_formatado)

    def _buscar_recursivo(self, no, nome):
        if no == self.NIL or nome == no.nome:
            return no

        if nome < no.nome:
            return self._buscar_recursivo(no.esq, nome)
        return self._buscar_recursivo(no.dir, nome)

    def remover(self, nome):
        z = self.buscar(nome)
        if z == self.NIL:
            return False

        y = z
        y_cor_original = y.cor
        if z.esq == self.NIL:
            x = z.dir
            self._transplantar(z, z.dir)
        elif z.dir == self.NIL:
            x = z.esq
            self._transplantar(z, z.esq)
        else:
            y = self._minimo(z.dir)
            y_cor_original = y.cor
            x = y.dir
            if y.pai == z:
                x.pai = y
            else:
                self._transplantar(y, y.dir)
                y.dir = z.dir
                y.dir.pai = y
            self._transplantar(z, y)
            y.esq = z.esq
            y.esq.pai = y
            y.cor = z.cor

        if y_cor_original == "PRETO":
            self._consertar_remocao(x)
        return True

    def _transplantar(self, u, v):
        if u.pai == self.NIL:
            self.raiz = v
        elif u == u.pai.esq:
            u.pai.esq = v
        else:
            u.pai.dir = v
        v.pai = u.pai

    def _minimo(self, no):
        while no.esq != self.NIL:
            no = no.esq
        return no

    def _consertar_remocao(self, x):
        while x != self.raiz and x.cor == "PRETO":
            if x == x.pai.esq:
                w = x.pai.dir
                if w.cor == "VERMELHO":
                    w.cor = "PRETO"
                    x.pai.cor = "VERMELHO"
                    self._rotacao_esquerda(x.pai)
                    w = x.pai.dir
                if w.esq.cor == "PRETO" and w.dir.cor == "PRETO":
                    w.cor = "VERMELHO"
                    x = x.pai
                else:
                    if w.dir.cor == "PRETO":
                        w.esq.cor = "PRETO"
                        w.cor = "VERMELHO"
                        self._rotacao_direita(w)
                        w = x.pai.dir
                    w.cor = x.pai.cor
                    x.pai.cor = "PRETO"
                    w.dir.cor = "PRETO"
                    self._rotacao_esquerda(x.pai)
                    x = self.raiz
            else:
                w = x.pai.esq
                if w.cor == "VERMELHO":
                    w.cor = "PRETO"
                    x.pai.cor = "VERMELHO"
                    self._rotacao_direita(x.pai)
                    w = x.pai.esq
                if w.dir.cor == "PRETO" and w.esq.cor == "PRETO":
                    w.cor = "VERMELHO"
                    x = x.pai
                else:
                    if w.esq.cor == "PRETO":
                        w.dir.cor = "PRETO"
                        w.cor = "VERMELHO"
                        self._rotacao_esquerda(w)
                        w = x.pai.esq
                    w.cor = x.pai.cor
                    x.pai.cor = "PRETO"
                    w.esq.cor = "PRETO"
                    self._rotacao_direita(x.pai)
                    x = self.raiz
        x.cor = "PRETO"