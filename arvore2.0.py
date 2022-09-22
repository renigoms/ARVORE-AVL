import sys
from typing import AnyStr
from ListaEncadeadaSimples import *


# Estrutura do nó
class _No:
    def __init__(self, valor):
        self.valor = valor
        self.esquerda = None
        self.direita = None
        self.altura = None  # tem que fazer uma função para saber a altura
        # obs: estudar altura da arvore

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
        # o nó a ser removido é um nó folha CONCLUIDO
        # o nó a ser removido possui somente um filho É O QUE FALTA
        # o nó a ser removido possui dois filhos CONCLUIDO
        perc, anterior = self._get_perc(self.raiz, valor)
        if not perc:
            raise Exception('ESSE VALOR NÃO EXISTE')
        #   ESSA PARTE REMOVE AS FOLHAS
        if perc.is_folha():
            if perc.valor > anterior.valor:
                anterior.direita = None
            else:
                anterior.esquerda = None
        else:
            sucessor = self._get_sucessor(perc)
            predecessor = self._get_predecessor(perc)
            if sucessor:# menor valor maior que chave[x]
                if perc == anterior.direita:
                    anterior.direita = perc.direita
                    sucessor.esquerda = perc.esquerda
                    perc.direita = None
                    perc.esquerda = None
                    print('entrou linha 138')
                elif perc == anterior.esquerda:
                    anterior.esquerda = perc.direita
                    sucessor.esquerda = perc.esquerda
                    perc.direita = None
                    perc.esquerda = None
                    print('entrou linha 141')

            elif predecessor: #  é o maior valor menor que chave[x]
                if perc == anterior.esquerda:
                    anterior.esquerda = perc.esquerda
                    predecessor.direita = perc.direita
                    perc.esquerda = None
                    perc.direita = None
                    print('entrou linha 140')
                elif perc == anterior.direita:
                    anterior.direita = perc.esquerda
                    predecessor.direita = perc.direita
                    perc.esquerda = None
                    perc.direita = None
                    print('entrou linha 151')
            if not sucessor and predecessor:  # FALTA TERMINAR ISSO DAI
                # TEM QUE FAZER ISSO AQUI ATE 04/10
                # ACREDITO QUE SEJA PARA REMOVER A RAIZ
                pass
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

    def cereate_arvore_to_lista(self, lista):  # TEM QUE FAZER ISSO AQUI ATE 04/10
        for i in lista:
            if i is None:
                return
            else:
                self.add(i)

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

    def fator_balanceamento(self, valor):
        perc = self._get_raiz(self.raiz, valor)
        return self._get_altura(perc.esquerda) - self._get_altura(perc.direita)

    # rotação

    def _rotacao_direita(self, raiz):  # falta terminar

        apont = raiz
        apont2 = apont.esquerda
        apont3 = apont2.direita
        apont2.direita = apont
        apont.esquerda = apont3
        apont2.altura = self._get_altura(self.raiz)
        apont.altura = self._get_altura(self.raiz)
        return apont2

    def _rotacao_esquerda(self, raiz):  # falta terminar
        apont = raiz
        apont2 = apont.direita
        apont3 = apont2.esquerda
        apont3.esquerda = apont
        apont.direita = apont3
        apont2.altura = self._get_altura(self.raiz)
        apont.altura = self._get_altura(self.raiz)
        return apont2

    def _rotacao_direita_esquerda(self, raiz):  # falta terminar
        raiz.direita = self._rotacao_direita(raiz.direita)
        return self._rotacao_esquerda(raiz)

    def _rotacao_esquerda_direita(self, raiz):
        raiz.esquerda = self._rotacao_esquerda(raiz.esquerda)
        return self._rotacao_direita(raiz)

    # BALANCEAMENTO
    def _get_balancear(self, raiz):
        if not raiz:
            return
        else:
            # ROTAÇÃO À ESQUERDA
            if self.fator_balanceamento(raiz.valor) < -1 and self.fator_balanceamento(raiz.direita.valor) <= 0:
                raiz = self._rotacao_esquerda(raiz)
            # ROTAÇÃO À DIREITA
            elif self.fator_balanceamento(raiz.valor) < -1 and self.fator_balanceamento(raiz.esquerda.valor) >= 0:
                print('ok2linha202', raiz.valor)
                raiz = self._rotacao_direita(raiz)
            # ROTAÇÃO DUPLA/ESQUERDA
            elif self.fator_balanceamento(raiz.valor) > 1 and self.fator_balanceamento(raiz.esquerda.valor) < 0:
                raiz = self._rotacao_esquerda_direita(raiz)
            # ROTAÇÃO DUPLA/DIREITA
            elif self.fator_balanceamento(raiz.valor) < -1 and self.fator_balanceamento(raiz.direita.valor) > 0:
                raiz = self._rotacao_direita_esquerda(raiz)
            self._get_balancear(raiz.esquerda)
            self._get_balancear(raiz.direita)

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

    def teste(self):
        return self._get_predecessor(self.raiz)


arvore = ArvoreBinaria()
lista = []
lista2 = []
for i in range(1,50,12):
    lista.append(i)
for i in range(50,1,-9):
    lista2.append(i)
print(lista2)
lista2.extend(lista)
print(lista2)
arvore.cereate_arvore_to_lista(lista2)
arvore.add(80)
arvore.add(870)
arvore.add(810)
arvore.add(70)
arvore.add(680)
arvore.add(66)
arvore.remover(80)
arvore.remover(870)
arvore.remover(810)
arvore.remover(70)
arvore.remover(680)
arvore.remover(66)
arvore.remover(1)
arvore.remover(13)
arvore.remover(41)
arvore.remover(32)
arvore.remover(23)
arvore.remover(14)
arvore.remover(5)
arvore.remover(25)
arvore.remover(37)
arvore.remover(49)
arvore.add(51)
arvore.add(49)
arvore.remover(49)
arvore.remover(51)

print(arvore.total)
print(arvore.raiz.altura)
arvore.print()