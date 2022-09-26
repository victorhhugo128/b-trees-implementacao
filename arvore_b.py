class NoB:
    raiz = None

    def __init__(self, chave, t):
        if NoB.raiz is None: NoB.raiz = self
        self.chaves = [chave]
        self.ptr_baixo = [None, None]
        self.ptr_cima = None
        self.n_chaves = 1
        self.folha = True
        self.nivel = 1
        self.altura = 1
        self.t = t

    @staticmethod
    def retornar_raiz(cls):
        return NoB.raiz

    @staticmethod
    def definir_raiz(cls, raiz):
        NoB.raiz = raiz

    def mostrar_arvore(self):
        print(self.chaves)
        for i in self.ptr_baixo:
            if i is not None:
                i.mostrar_arvore()


    # def apagar_chave(self):
    #     # del self.chaves[-1], self.ptr_baixo[-1]
    #     # self.n_chaves -= 1
    #     for i in range(self.t, )

    def novo_no_raiz(self):
        n = NoB(None, self.t)
        n.chaves = []
        n.ptr_baixo = [None]
        n.ptr_cima = None
        n.n_chaves = 0
        n.nivel = -1
        n.altura = -1

        return n

    def novo_no(self):
        n = NoB(None, self.t)
        n.chaves = []
        for i in range(0, self.t - 1):
            n.chaves.append(None)
        n.ptr_baixo = []
        for i in range(0, self.t):
            n.ptr_baixo.append(None)
        n.ptr_cima = None
        n.n_chaves = 0
        n.nivel = -1
        n.altura = -1

        return n

    def nova_chave(self):
        self.chaves.append(None)
        self.n_chaves += 1
        self.ptr_baixo.append(None)

    def busca(self, k): # list index out of range
        i = 0
        while i < self.n_chaves and k > self.chaves[i]:
            i += 1
        if k == self.chaves[i]:
            return self, i
        elif self.folha:
            return self

        if self.chaves[i - 1] > k:
            return self.ptr_baixo[i - 1].busca
        else:
            return self.ptr_baixo[i].busca

    def busca_inserir(self, k):
        i = 0
        while i < self.n_chaves and k > self.chaves[i]: i += 1
        if i < self.n_chaves and k == self.chaves[i]:
            return print("Chave já existente.")
        elif self.folha:
            self.inserir_chave(k)

        return self.busca_inserir(k)

    def repartir_no_filho(self, i):
        """
        Reparte o filho no indíce i especificado.
        :param i: índice do ponteiro que aponta para o filho para dividir o nó.
        :return: None
        """

        #   cria um novo nó que será irmão do nó que será repartido.
        z = self.novo_no()
        y = self.ptr_baixo[i]
        z.folha = y.folha
        z.nivel = y.nivel
        z.altura = y.altura

        #   cuida para que as devidas chaves e ponteiros sejam transferidos de um nó para o outro.
        for j in range(0, self.t - 1):
            z.chaves[j] = y.chaves[j + self.t]
        if not y.folha:
            for j in range(0, self.t):
                z.ptr_baixo[j] = y.ptr_baixo[j + self.t]
        self.nova_chave()
        #   cuida para que os ponteiros do nó pai sejam rearranjados de maneira a incorporar o novo nó.
        for j in range(self.n_chaves, i + 1, -1):
            self.ptr_baixo[j] = self.ptr_baixo[j - 1]
        self.ptr_baixo[i + 1] = z
        #   rearranja as chaves do nó pai para receber a chave que vai subir.
        for j in range(self.n_chaves, i, -1):
            self.chaves[j - 1] = self.chaves[j - 2]
        #   o nó pai recebe a chave que subiu do nó que foi repartido.
        self.chaves[i] = y.chaves[self.t - 1]
        self.n_chaves = len(self.chaves)
        #   redefine o tamanho do nó que foi repartido.
        while len(y.chaves) != self.t - 1:
            y.chaves.pop(-1)
        y.n_chaves = len(y.chaves)
        z.n_chaves = len(z.chaves)

    def inserir_chave(self, k):
        """
        Insere uma chave k na árvore B.
        :param k: valor a ser inserido na árvore
        :return: None.
        """
        if self.busca(k) is tuple:
            print("Nó já existente.")
        r = self
        if r.n_chaves == 2 * self.t - 1:    # caso a raiz esteja cheia, divide e cria uma nova raiz.
            s = self.novo_no_raiz()
            NoB.raiz = s    # redefine a raiz para o novo nó.
            s.folha = False
            s.n = 0
            s.ptr_baixo[0] = r
            s.repartir_no_filho(0)
            s.inserir_chave_nao_cheia(k)
        else:   # caso a raiz não esteja cheia, prossegue normalmente com a operação.
            self.inserir_chave_nao_cheia(k)

    def inserir_chave_nao_cheia(self, k):
        """
        Percorre a árvore até a folha para inserir o valor solicitado.
        :param k: valor a ser adicionado na árvore.
        :return: None.
        """
        i = self.n_chaves
        if self.folha:  # faz a inserção do elemento caso esteja numa folha.
            self.nova_chave()
            while i > 0 and k < self.chaves[i - 1]:
                self.chaves[i + 1 - 1] = self.chaves[i - 1]
                i -= 1
            self.chaves[i + 1 - 1] = k
        else:   # caso o nó presente não seja folha, procura o índice correto e desce a árvore mais um nível.
            while i >= 0 and k < self.chaves[i - 1]:
                i -= 1
            if self.ptr_baixo[i].n_chaves == 2 * self.t - 1:    # separa o nó seguinte caso ele esteja cheio.
                self.repartir_no_filho(i)
                if k > self.chaves[i - 1]:
                    i += 1
            self.ptr_baixo[i].inserir_chave_nao_cheia(k)


if __name__ == "__main__":
    b_tree = NoB(1, 3)
    # NoB.raiz.inserir_chave(2)
    # NoB.raiz.inserir_chave(3)
    # NoB.raiz.inserir_chave(4)
    # NoB.raiz.inserir_chave(5)
    # NoB.raiz.inserir_chave(6)
    # NoB.raiz.inserir_chave(7)
    # NoB.raiz.inserir_chave(8)
    # NoB.raiz.inserir_chave(9)
    # NoB.raiz.inserir_chave(10)
    for i in range(2, 25):
        NoB.raiz.inserir_chave(i)

    NoB.raiz.inserir_chave(2)

    NoB.raiz.mostrar_arvore()
