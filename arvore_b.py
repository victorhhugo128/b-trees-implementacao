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
        self.t = t

    @staticmethod
    def definir_raiz(cls, raiz):
        """
        Designa um determinado nó como nova raiz.
        :param cls: método que atua na própria classe.
        :param raiz: nó a ser designado como raiz.
        :return: None.
        """
        NoB.raiz = raiz

    def redefinir_niveis(self, t):
        """
        Ajusta o nível de todos os nós.
        :param t: t = 0.
        :return: None.
        """
        self.nivel = t
        if self.folha:
            return

        for i in self.ptr_baixo:
            i.redefinir_niveis(t + 1)

    def redefinir_ptr_cima(self, no_pai):
        """
        Redefine os ponteiros apontando para o pai de todos os nós.
        :param no_pai: o próprio nó que vai varrer os filhos redefinindo.
        :return: None.
        """
        for i in self.ptr_baixo:
            self.ptr_cima = no_pai
            if i is not None:
                i.redefinir_ptr_cima(self)

    # def balancear_nos_t(self, no_pai):
    #     j = 0
    #     for i in self.ptr_baixo:
    #         if i.n_chaves < self.t - 1:
    #             print(no_pai.chaves)
    #             no_pai.juntar_filhos(j)
    #         j += 1
    #         if i is not None:
    #             i.balancear_nos_t(self)

    def mostrar_arvore(self):
        """
        Mostra as informações da árvore criada.
        :return: None.
        """
        print(f"chaves = {self.chaves}, n_chaves = {self.n_chaves}, n_ptr_baixo = {len(self.ptr_baixo)}, nivel = {self.nivel}, folha = {self.folha}, t = {self.t}")
        if NoB.raiz != self:
            print(f"ptr_cima = {self.ptr_cima.chaves}")
        for i in self.ptr_baixo:
            if i is not None:
                i.mostrar_arvore()

    def apagar_chave(self, t=-1):
        """
        Apaga um espaço de chave, com um ponteiro correspondente.
        :return: None.
        """
        self.chaves.pop(t)
        self.ptr_baixo.pop(t)
        self.n_chaves = len(self.chaves)

    def retornar_no_antecessor(self, no_k, k, primeiro):
        """
        Retorna o antecessor de um determinado nó.
        :param no_k: o nó em que k se encontra.
        :param k: a própria chave k.
        :param primeiro: deve sempre ser passado como True como forma de controlar a recursão.
        :return: None.
        """
        if primeiro is True:
            i = 0
            if no_k.ptr_baixo[0].folha:
                return no_k
            else:
                while no_k.chaves[i] != k:
                    i += 1
                return no_k.ptr_baixo[i].retornar_no_antecessor(no_k.ptr_baixo[i], k, False)
        else:
            if self.ptr_baixo[0].folha:
                return self
            else:
                return self.ptr_baixo[self.n_chaves].retornar_no_antecessor(self.ptr_baixo, k, False)

    def retornar_no_sucessor(self, no_k, k, primeiro):
        """
        Retorna o sucessor de um determinado nó.
        :param no_k: nó em que a chave k se encontra.
        :param k: a própria chave k.
        :param primeiro: deve sempre ser passado como True como forma de controlar a recursão.
        :return: sucessor de k.
        """
        if primeiro is True:
            i = 0
            if no_k.ptr_baixo[0].folha:
                return no_k
            else:
                while no_k.chaves[i] != k:
                    i += 1
                return no_k.ptr_baixo[i + 1].retornar_no_sucessor(no_k.ptr_baixo[i], k, False)
        else:
            if self.ptr_baixo[0].folha:
                return self
            else:
                return self.ptr_baixo[0].retornar_no_sucessor(self.ptr_baixo, k, False)

    def juntar_filhos(self, indice):
        """
        Junta dois filhos de uma chave pai no indice especifico.
        :param indice: indice da chave que irá juntar os nós filhos.
        :return: None.
        """
        filho1 = self.ptr_baixo[indice]
        filho2 = self.ptr_baixo[indice + 1]

        for i in range(0, filho2.n_chaves):
            if i < 0:
                filho1.nova_chave()
                indice_1 = filho1.n_chaves - 1
                filho1.chaves[indice_1] = self.chaves[indice]
                filho1.ptr_baixo[indice_1 + 1] = None
            filho1.nova_chave()
            indice_1 = filho1.n_chaves - 1
            filho1.chaves[indice_1] = filho2.chaves[i]
            filho1.ptr_baixo[indice_1 + 1] = None
        del filho2
        self.apagar_chave(indice)
        self.ptr_baixo[indice] = filho1

    def emprestar_chave_irma(self, indice):
        if self.ptr_baixo[indice - 1].n_chaves >= self.t:    #   pegar emprestado do irmão à esquerda.
            filho1 = self.ptr_baixo[indice - 1]
            filho2 = self.ptr_baixo[indice]
            filho2.nova_chave()
            for i in range(filho2.n_chaves - 1, 0):
                filho2[i - 1] = filho2[i]
            filho2.chaves[0] = self.chaves[indice]
            self.chaves[indice] = filho1.chaves[-1]
            filho1.apagar_chave()
        elif self.ptr_baixo[indice].n_chaves >= self.t:   #   pegar emprestado do irmão à direita.
            filho1 = self.ptr_baixo[indice]
            filho2 = self.ptr_baixo[indice + 1]
            filho1.nova_chave()
            filho1.chaves[-1] = self.chaves[indice]
            self.chaves[indice] = filho1.chaves[-1]
            filho2.apagar_chave(0)
        else:
            self.juntar_filhos(indice)

    def novo_no_raiz(self):
        """
        Define um novo nó que será a nova raiz.
        :return: novo nó raiz.
        """
        n = NoB(None, self.t)
        n.chaves = []
        n.ptr_baixo = [None]
        n.ptr_cima = None
        n.n_chaves = 0
        n.nivel = -1
        n.altura = -1

        return n

    def novo_no(self):
        """
        Define um novo nó com número de chaves t - 1 e número de ponteiros t.
        :return: novo nó criado.
        """
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
        """
        Cria um novo espaço de chaves no nó especificado.
        :return: None.
        """
        self.chaves.append(None)
        self.n_chaves += 1
        self.ptr_baixo.append(None)

    def busca(self, k):
        """
        Busca um determinado índice na árvore. Caso ele seja achado, retorna a posição e o nó em que o índice já se
        encontra, caso não, retorna apenas o nó em que o índice estaria.
        :param k: índice a ser procurado.
        :return: posição do nó, caso ele exista, e nó em que o índice está ou estaria.
        """
        i = 0
        while i < self.n_chaves - 1 and k > self.chaves[i]:
            i += 1
        if k == self.chaves[i]:
            return self, i
        elif self.folha:
            return self

        if self.chaves[i] > k:
            return self.ptr_baixo[i].busca(k)
        else:
            return self.ptr_baixo[i + 1].busca(k)

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
            y.ptr_baixo.pop(-1)
        y.n_chaves = len(y.chaves)
        z.n_chaves = len(z.chaves)
        y.ptr_cima = self
        z.ptr_cima = self

    def remover_chave_folha(self, k):
        """
        Caso mais simples de remoção na árvore b, que ocorre quando a chave se encontra em uma folha e continuará com
        t - 1 após a remoção.
        :param k: a chave a ser removida da árvore.
        :return: None.
        """
        if type(self.busca(k)) is NoB:
            print("Chave não existe, impossível remover.")
            return
        no, indice = self.busca(k)
        no.apagar_chave(indice)

    def remover_chave_emprestar_folha(self, k):
        if type(self.busca(k)) is NoB:
            print("Chave não existe, impossível remover.")
            return
        no, indice = self.busca()
        pai = no.ptr_cima

        for i in range(0, pai.n_chaves - 1):
            if pai.chaves[i] > k:
                indice_pai = i

        pai.emprestar_chave_irma(indice_pai)

        self.remover_chave_folha(k)

    def remover_chave_no_interno(self, k):
        """
        Caso que ocorre quando a chave a ser retirada se encontra em um nó interno, em que é necessário fazer uma
        leitura sobre os sucessores e antecessores da chave em questão.
        :param k: chave a ser removida.
        :return: None.
        """
        self.mostrar_arvore()
        if type(self.busca(k)) is NoB:
            print("Chave não existe, impossível remover.")
            return
        no, indice = self.busca(k)
        no_pai_antecessor = no.retornar_no_antecessor(no, k, True)
        indice_a = no_pai_antecessor.n_chaves - 1
        no_pai_sucessor = no.retornar_no_sucessor(no, k, True)
        if no_pai_antecessor.ptr_baixo[indice_a + 1].n_chaves >= self.t:
            filho = no_pai_antecessor.ptr_baixo[indice_a]
            aux = filho.chaves[filho.n_chaves - 1]
            filho.apagar_chave()
            no.chaves[indice] = aux
        elif no_pai_sucessor.ptr_baixo[0].n_chaves >= self.t:
            filho = no_pai_sucessor.ptr_baixo[0]
            aux = filho.chaves[0]
            filho.apagar_chave(0)
            no.chaves[indice] = aux
        else:
            no_pai_antecessor.emprestar_chave_irma(indice_a)

    def remover_chave(self, k):
        """
        Verifica em que caso a remoção se aplica e faz a devida operação.
        :param k: chave a ser removida.
        :return:
        """
        no, indice = self.busca(k)

        if no.folha and no.n_chaves > self.t - 1:
            self.remover_chave_folha(k)
        elif no.folha:
            self.remover_chave_emprestar_folha(k)
        else:
            self.remover_chave_no_interno(k)
            self.balancear_nos_t(None)

    def inserir_chave(self, k):
        """
        Insere uma chave k na árvore B.
        :param k: valor a ser inserido na árvore
        :return: None.
        """
        #   testa o valor para saber se ele existe na árvore, caso sim, ele não completará a operação de busca.
        if type(self.busca(k)) is tuple:
            print("Nó já existente.")
            return
        r = self
        if r.n_chaves == 2 * self.t - 1:    # caso a raiz esteja cheia, divide e cria uma nova raiz.
            s = self.novo_no_raiz()
            NoB.raiz = s    # redefine a raiz para o novo nó.
            s.folha = False
            s.n = 0
            s.nivel = 0
            s.ptr_baixo[0] = r
            s.repartir_no_filho(0)
            s.inserir_chave_nao_cheia(k)
        else:   # caso a raiz não esteja cheia, prossegue normalmente com a operação.
            self.inserir_chave_nao_cheia(k)
        self.redefinir_niveis(0)
        self.redefinir_ptr_cima(None)

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
    for i in range(2, 30):
        NoB.raiz.inserir_chave(i)

    NoB.raiz.mostrar_arvore()
    print("\n\n")
    NoB.raiz.remover_chave(6)

    NoB.raiz.mostrar_arvore()
