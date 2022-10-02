import sys
from typing import AnyStr
from ListaEncadeadaSimples import *


# Estrutura do nó
class _No:
    def __init__(self, valor):
        self.valor = valor
        self.esquerda = None
        self.direita = None
        self.altura = None

    # str do nó
    def __str__(self):
        return f'{self.valor}'

    # veirficar de o no é uma folha
    def is_folha(self):
        return self.direita is None and self.esquerda is None


# Estrutura da árvore
class ArvoreBinaria:
    def __init__(self):
        self.raiz = None
        self.total = 0

    def _add(self, no_raiz, no):
        # função privada que faz o trabalho de adicionar
        if not no_raiz:
            return no
        elif no.valor < no_raiz.valor:
            no_raiz.esquerda = self._add(no_raiz.esquerda, no)
        else:
            no_raiz.direita = self._add(no_raiz.direita, no)
        return no_raiz

    def add(self, valor):  # retorna a função _add
        no = _No(valor)
        self.raiz = self._add(self.raiz, no)
        self.total += 1
        self.raiz.altura = self._get_altura(self.raiz)

    def _get_perc(self, perc, valor, anterior=None):
        if not perc:
            return
        elif perc.valor == valor:
            return perc, anterior
        elif valor > perc.valor:
            return self._get_perc(perc.direita, valor, perc)
        else:
            return self._get_perc(perc.esquerda, valor, perc)

    def get(self, valor):
        perc, anterior = self._get_perc(self.raiz, valor)
        return perc

    # ALTURA DA AVL
    def _get_altura(self, raiz):
        if not raiz:
            return 0
        else:
            if self._get_altura(raiz.esquerda) > self._get_altura(raiz.direita):
                return self._get_altura(raiz.esquerda) + 1
            else:
                return self._get_altura(raiz.direita) + 1

    def __str__(self):
        self.ordem(self.raiz)
        return ''

    def ordem(self, raiz, tipo='pre'):
        if not raiz:
            return
        if tipo == 'pre':
            print(raiz)
        self.ordem(raiz.esquerda, tipo)
        if tipo == 'in':
            print(raiz)
        self.ordem(raiz.direita, tipo)
        if tipo == 'pos':
            print(raiz)

    def _maximo(self, no_raiz):
        while no_raiz and no_raiz.direita:
            no_raiz = no_raiz.direita
        return no_raiz

    def _minimo(self, no_raiz):
        while no_raiz and no_raiz.esquerda:
            no_raiz = no_raiz.esquerda
        return no_raiz

    def minimo(self):
        return self._minimo(self.raiz)

    def maximo(self):
        return self._maximo(self.raiz)

    # MAIOR VALOR DO LADO DIREITO
    def _get_sucessor(self, perc):
        perc = self._minimo(perc.direita)
        return perc

    # MAIOR VALOR DO LADO ESQUERDO
    def _get_predecessor(self, perc):
        perc = self._maximo(perc.esquerda)
        return perc

    def remover(self, valor):  # A FUNÇÃO REMOVER NÃO ESTÁ PRONTA PESQUISAR COMO TERMINÁ-LA
        # TEM QUE FAZER ISSO AQUI ATE 04/10
        perc, anterior = self._get_perc(self.raiz, valor)
        if not perc:
            raise Exception('ESSE VALOR NÃO EXISTE')
        #   ESSA PARTE REMOVE AS FOLHAS
        if perc.valor == self.raiz.valor:
            if perc.direita is None and perc.esquerda is None:
                perc.valor = None
            else:
                sucessor = self._get_sucessor(perc)
                predecessor = self._get_predecessor(perc)
                if sucessor:
                    self.raiz = perc.direita
                    sucessor.esquerda = perc.esquerda
                    perc.direita = None
                    perc.esquerda = None

                elif predecessor:
                    self.raiz = perc.esquerda
                    predecessor.direita = perc.direita
                    perc.direita = None
                    perc.esquerda = None

        elif perc.is_folha():
            if perc.valor > anterior.valor:
                anterior.direita = None
            else:
                anterior.esquerda = None
        else:
            sucessor = self._get_sucessor(perc)
            predecessor = self._get_predecessor(perc)
            if sucessor:  # menor valor maior que chave[x]
                if perc == anterior.direita:
                    anterior.direita = perc.direita
                    sucessor.esquerda = perc.esquerda
                    perc.direita = None
                    perc.esquerda = None
                elif perc == anterior.esquerda:
                    anterior.esquerda = perc.direita
                    sucessor.esquerda = perc.esquerda
                    perc.direita = None
                    perc.esquerda = None
            elif not sucessor and predecessor:  # é o maior valor menor que chave[x]
                if perc == anterior.esquerda:
                    anterior.esquerda = perc.esquerda
                    predecessor.direita = perc.direita
                    perc.esquerda = None
                    perc.direita = None
                elif perc == anterior.direita:
                    anterior.direita = perc.esquerda
                    predecessor.direita = perc.direita
                    perc.esquerda = None
                    perc.direita = None
        self.total -= 1
        self.raiz.altura = self._get_altura(self.raiz)

    # FUNÇÕES QUE EU TENHO QUE FAZER

    def get_lista(self, perc, lista, ordem='pre'):  # TEM QUE FAZER ISSO AQUI ATE 04/10
        if not perc:
            return
        else:
            if ordem == 'pre':
                lista.adicionaritens(perc.valor)
            self.get_lista(perc.esquerda, lista, ordem)
            if ordem == 'in':
                lista.adicionaritens(perc.valor)
            self.get_lista(perc.direita, lista, ordem)
            if ordem == 'pos':
                lista.adicionaritens(perc.valor)

        return lista

    def create_arvore_to_lista(self, lista):  # TEM QUE FAZER ISSO AQUI ATE 04/10
        for i in range(len(lista)):
            if i is None:
                return
            else:
                self.add(lista[i])

    # FATOR DE BALANCEAMENTO

    def _get_raiz(self, perc, valor):
        if not perc:
            return
        elif perc.valor == valor:
            return perc
        elif valor > perc.valor:
            return self._get_raiz(perc.direita, valor)
        else:
            return self._get_raiz(perc.esquerda, valor)

    def _fator_balanceamento(self, valor):
        perc = self._get_raiz(self.raiz, valor)
        if not perc:
            return -1
        else:
            return self._get_altura(perc.esquerda) - self._get_altura(perc.direita)

    # rotação

    def _rotacao_direita(self, raiz, raiz_anterior=None):
        pai = raiz_anterior
        perc = raiz.esquerda
        if not perc.direita is None:
            raiz.esquerda = perc.direita
        if pai is None:
            self.raiz = perc
        elif pai.direita == raiz:
            pai.direita = perc
        else:
            pai.esquerda = perc
        raiz.esquerda = None
        perc.direita = raiz
        return perc

    def _rotacao_esquerda(self, raiz, anterior_raiz=None):
        perc = raiz.direita
        pai = anterior_raiz
        if not raiz.esquerda is None:
            raiz.esquerda = perc.esquerda
        if pai is None:
            self.raiz = perc
        elif pai.direita == raiz:
            pai.esquerda = perc
        else:
            pai.direita = perc
        raiz.direita = None
        perc.esquerda = raiz
        return perc

    def _rotacao_direita_esquerda(self, raiz):  # falta terminar
        self._rotacao_direita(raiz.direita)
        self._rotacao_esquerda(raiz)

    def _rotacao_esquerda_direita(self, raiz):
        self._rotacao_esquerda(raiz.esquerda)
        self._rotacao_direita(raiz)

    # BALANCEAMENTO

    def _get_balancear(self, raiz, raiz_anterior=None):
        if not raiz:
            return
        else:

            if self._fator_balanceamento(raiz.valor) > 1:
                if self._fator_balanceamento(raiz.esquerda.valor) > 0:
                    self._rotacao_direita(raiz, raiz_anterior)
                else:
                    self._rotacao_esquerda_direita(raiz)

            if self._fator_balanceamento(raiz.valor) < -1:
                if self._fator_balanceamento(raiz.direita.valor) < 0:
                    self._rotacao_esquerda(raiz, raiz_anterior)
                else:
                    self._rotacao_direita_esquerda(raiz)

            if raiz.esquerda:
                self._get_balancear(raiz.esquerda, raiz)
            if raiz.direita:
                self._get_balancear(raiz.direita, raiz)

    def balancear(self):
        return self._get_balancear(self.raiz)

    def printHelper(self, currPtr, indent, last):
        if currPtr is not None:
            sys.stdout.write(indent)
            if last:
                sys.stdout.write("R----")
                indent += "     "
            else:
                sys.stdout.write("L----")
                indent += "|    "
            print(currPtr.valor)
            self.printHelper(currPtr.esquerda, indent, False)
            self.printHelper(currPtr.direita, indent, True)

    def print(self):
        self.printHelper(self.raiz, '', True)


arvore = ArvoreBinaria()

arvore.add(4)
arvore.add(3)
arvore.add(2)
arvore.add(1)
arvore.print()
arvore.balancear()
arvore.print()