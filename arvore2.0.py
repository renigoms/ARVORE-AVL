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

    # FUNÇÕES PARA ADICIONAR
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

    def remover(self, valor):
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

    # TRANSFORMAR A ARVORE EM LISTA
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

    # TRANSFORMAR A LISTA EM ÁRVORE
    def create_arvore_to_lista(self, lista):  # TEM QUE FAZER ISSO AQUI ATE 04/10
        for i in range(len(lista)):
            if i is None:
                return
            else:
                self.add(lista[i])

    # FATOR DE BALANCEAMENTO

    def _fator_balanceamento(self, valor):
        perc = self.get(valor)
        if not perc:
            return 0
        else:
            return self._get_altura(perc.esquerda) - self._get_altura(perc.direita)

    # ROTAÇÕES

    def _rotacao_direita(self, raiz, raiz_anterior):
        pai = raiz_anterior
        no = raiz
        perc = no.esquerda
        if perc and perc.direita:
            no.esquerda = perc.direita
        else:
            no.esquerda = None
        if pai is None:
            self.raiz = perc
        elif pai.esquerda == raiz:
            pai.esquerda = perc
        elif pai.direita == raiz:
            pai.direita = perc
        perc.direita = raiz
        return perc

    def _rotacao_esquerda(self, raiz, anterior_raiz):
        no2 = raiz
        perc = no2.direita
        pai = anterior_raiz
        if perc and perc.esquerda:
            no2.direita = perc.esquerda
        else:
            no2.direita = None
        if pai is None:
            self.raiz = perc
        elif pai.esquerda == raiz:
            pai.esquerda = perc
        elif pai.direita == raiz:
            pai.direita = perc

        perc.esquerda = raiz
        return perc

    def _rotacao_direita_esquerda(self, raiz, raiz_anterior):
        raiz.direita = self._rotacao_direita(raiz.direita, raiz_anterior)
        return self._rotacao_esquerda(raiz, raiz_anterior)

    def _rotacao_esquerda_direita(self, raiz, raiz_anterior):
        raiz.esquerda = self._rotacao_esquerda(raiz.esquerda, raiz_anterior)
        return self._rotacao_direita(raiz, raiz_anterior)

    # BALANCEAMENTO

    def _get_balancear(self, raiz, raiz_anterior=None):
        if raiz is None:
            raiz = self.raiz

        if self._fator_balanceamento(raiz.valor) > 1:
            if self._fator_balanceamento(raiz.esquerda.valor) == -1:
                raiz = self._rotacao_esquerda_direita(raiz, raiz_anterior)
            else:
                raiz = self._rotacao_direita(raiz, raiz_anterior)

        if self._fator_balanceamento(raiz.valor) < -1:
            if self._fator_balanceamento(raiz.direita.valor) == 1:
                raiz = self._rotacao_direita_esquerda(raiz, raiz_anterior)
            else:
                raiz = self._rotacao_esquerda(raiz, raiz_anterior)

        if raiz.esquerda:
            self._get_balancear(raiz.esquerda, raiz)
        if raiz.direita:
            self._get_balancear(raiz.direita, raiz)
        # REBALANCEAMENTO
        fb = self._fator_balanceamento(self.raiz.valor)
        if fb < -1 or fb > 1:
            self.balancear()

    # MÉTODO PARA CHAMAR O BALANCEAR
    def balancear(self):
        return self._get_balancear(self.raiz)

    # FUNÇÕES PRINT
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


lista = ListEncadSimples()
lista2 = ListEncadSimples()
lista3 = ListEncadSimples()
for i in range(1, 100, 6):
    lista.adicionaritens(i)
arvore = ArvoreBinaria()
arvore.create_arvore_to_lista(lista)
arvore.print()
arvore.get_lista(arvore.raiz, lista2, 'pos')
print(lista2)
arvore.ordem(arvore.raiz)
print('@!!@@!')
arvore.ordem(arvore.raiz, 'in')
print('@!!@@!')
arvore.ordem(arvore.raiz, 'pos')
print('@!!@@!')
print(arvore.get(19))
print('=--=--=-')
print(arvore.maximo())
print('=--=--=-')
print(arvore.minimo())
print('=--=--=-')
arvore.balancear()
arvore.print()
arvore.remover(85)
arvore.remover(55)
arvore.remover(31)
arvore.print()
arvore.balancear()
arvore.add(9)
arvore.add(77)
arvore.add(81)
arvore.print()
arvore.balancear()
arvore.print()
arvore.get_lista(arvore.raiz, lista3)
for i in range(len(lista3)):
    arvore.remover(lista3[i])
arvore.print()