class _No:
    def __init__(self, valor):
        self.valor = valor
        self.proximo = None

    def __str__(self):
        proximo = f', {self.proximo}'
        if self.proximo is None:
            proximo = ''
        return f'{self.valor}{proximo}'


class ListEncadSimples:
    def __init__(self, tipo=None):

        self.inicio = None
        self.final = None
        self.tamanho = 0
        self.tipo = tipo

    def __str__(self):
        return f'[{self.inicio}]'

    def __len__(self):
        return self.tamanho

    def __getitem__(self, item):
        return self.get_valor(item)

    def adicionaritens(self, valor):
        if self.tipo and type(valor) != self.tipo:
            raise TypeError(f'Tipo inválido, a função só aceita tipo: {self.tipo}')
        no = _No(valor)
        if not self.final:
            self.final = no
            self.inicio = no
        else:
            self.final.proximo = no
            self.final = no
        self.tamanho += 1

    def inseriritem(self, index, valor):
        if self.tipo and type(valor) != self.tipo:
            raise TypeError(f'Tipo inválido, a função só aceita tipo: {self.tipo}')
        if index >= self.tamanho:  # pro final
            self.adicionaritens(valor)
            return
        no = _No(valor)  # adiciona o parâmetro valor ao nó
        if index == 0:  # pro inicial
            no.proximo = self.inicio
            # o no.proximo vai apontar para o self.inicio,
            # que é a caixinha inicial
            self.inicio = no
            # logo após irá depositar o valor nó com self.inicio = no
        else:
            perc = self.inicio
            for i in range(index - 1):
                perc = perc.proximo
            no.proximo = perc.proximo
            perc.proximo = no
        self.tamanho += 1

    def remover_index(self, index):
        if self.tamanho == 0:
            raise Exception('Lista Vazia!!!')
        if index >= self.tamanho or self.tamanho + index < 0:
            raise Exception('Não há um item na lista com esse index')
        elif index < 0:
            index += self.tamanho
        elif index == 0:
            self.inicio = self.inicio.proximo
            self.tamanho -= 1
        else:
            perc = self.inicio
            for i in range(index - 1):
                perc = perc.proximo
            perc.proximo = perc.proximo.proximo
            self.tamanho -= 1

    def remover_item(self, valor):
        if self.tamanho == 0:
            raise ValueError('LISTA ZERADA')
        perc = self.inicio
        if perc.valor == valor:
            self.inicio = self.inicio.proximo
            self.tamanho -= 1
            return
        while perc.proximo:
            if perc.proximo.valor == valor:
                perc.proximo = perc.proximo.proximo
                self.tamanho -= 1
                return
            perc = perc.proximo

    def get_valor(self, index):
        if self.tamanho == 0:
            raise IndexError('NÃO EXISTE ELEMENTOS NA LISTA')
        if index == 0:
            return self.inicio.valor
        elif index == self.tamanho:
            return self.final.valor
        else:
            perc = self.inicio
            for i in range(index-1):
                if not perc.proximo:
                    return
                else:
                    perc = perc.proximo
            return perc.valor

    def get_index(self, valor):
        if self.tamanho == 0:
            raise IndexError('NÃO EXISTE ELEMENTOS NA LISTA')
        cont = 0
        perc = self.inicio
        while perc.valor is not valor:
            cont += 1
            perc = perc.proximo
        return cont

    def editar_item(self, index, novo_valor):
        if self.tamanho == 0:
            raise IndexError('Não há itens para serem editados na lista')
        perc = self.inicio
        for i in range(index):
            perc = perc.proximo
        perc.valor = novo_valor

    def buscar_valores_repetidos(self):
        # DETECTAR O SE A LISTA ESTA VAZIA
        if self.tamanho == 0:
            raise Exception('Lista Vazia!!!')

        string1 = ''
        string2 = ''
        perc = self.inicio
        # BUSCAR VALORES REPETIDOS

        while perc is not None:
            if ':' + str(perc.valor) + ':' not in string1:
                string1 += ':' + str(perc.valor) + ':'
            elif ':' + str(perc.valor) + ':' in string1:
                string2 += ':' + str(perc.valor) + ':'
            perc = perc.proximo
        if string2 == '':
            print('Não há valores repetidos')
        else:
            return string2

    def ordenar(self, crescente=True):
        if self.tamanho == 0:
            raise Exception('Lista Vazia!!!')
        # Método Usado: BublleSort
        if crescente:
            perc = self.inicio
            for o in range(self.tamanho - 1):
                for i in range(self.tamanho - 1):
                    valor = perc.valor
                    valdafrente = perc.proximo.valor
                    if valor > valdafrente:
                        perc.valor = perc.proximo.valor
                        perc.proximo.valor = valor
                    perc = perc.proximo
                perc = self.inicio
        else:
            perc = self.inicio
            for o in range(self.tamanho - 1):
                for i in range(self.tamanho - 1):
                    valor = perc.valor
                    valdafrente = perc.proximo.valor
                    if valor < valdafrente:
                        perc.valor = perc.proximo.valor
                        perc.proximo.valor = valor
                    perc = perc.proximo
                perc = self.inicio


