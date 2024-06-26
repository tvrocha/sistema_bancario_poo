from datetime import datetime
from transacoes import Historico, Saque

class ContaIterador:
    def __init__(self, contas) -> None:
        self.contas = contas
        self._index = 0

    def __iter__(self):
        return self

    def __next__(self):
        try:
            conta = self.contas[self._index]
        except IndexError:
            raise StopIteration
        self._index += 1
        return conta


class Cliente:
    def __init__(self, endereco) -> None:
        self._contas = []
        self.endereco = endereco

    def adicionar_conta(self, conta):
        self._contas.append(conta)

    @property
    def contas(self):
        return self._contas


class PessoaFisica(Cliente):
    def __init__(self, cpf, nome, data_nascimento, endereco) -> None:
        super().__init__(endereco)
        self._nome = nome
        self._cpf = cpf
        self._data_nascimento = data_nascimento

    @property
    def nome(self):
        return self._nome

    @property
    def cpf(self):
        return self._cpf

    @property
    def data_nascimento(self):
        return self._data_nascimento

    def __repr__(self) -> str:  # representação (parecido com str)
        return f"[{self.__class__.__name__}]: [CPF: {self.cpf}]"


class Conta:
    def __init__(self, numero, cliente) -> None:
        self._saldo = 0  # float
        self._numero = numero  # int - numero da conta
        self._agencia = "0001"  # str - '0001'
        self._cliente = cliente
        self._historico = Historico(self)

    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(numero, cliente)

    @property
    def saldo(self):
        return self._saldo

    @property
    def numero(self):
        return self._numero

    @property
    def agencia(self):
        return self._agencia

    @property
    def cliente(self):
        return self._cliente

    @property
    def historico(self):
        return self._historico

    def sacar(self, valor):
        saldo = self._saldo
        excedeu_saldo = valor > saldo

        if excedeu_saldo:
            print("\nSaldo insuficiente!")
            return False
        elif valor > 0:
            self._saldo -= valor
            print("\nSaque realizado com sucesso!")
            return True
        else:
            print("\nOpção inválida!")
            return False

    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            print("\nDepósito realizado com sucesso")
            return True
        else:
            print("\nValor inválido!")
            return False

    def adicionar_transacao(self, transacao):
        if self.historico.transacoes_do_dia() >= 10:
            print("\nVocê excedeu o número de transações permitidas para hoje!")
            return
        sucesso_transacao = transacao.executar(self)
        if sucesso_transacao:
            self.historico.adicionar_transacao(transacao, self.numero)


class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite_saques=3, limite_valor_saque=500) -> None:
        super().__init__(numero, cliente)
        self._LIMITE_SAQUES = limite_saques
        self._LIMITE_VALOR_SAQUES = limite_valor_saque

    def sacar(self, valor):
        numero_saques = len(
            [transacao for transacao in self.historico.transacoes if transacao["Tipo"] == Saque.__name__]
        )

        excedeu_limite = valor > self._LIMITE_VALOR_SAQUES
        excedeu_saques = numero_saques >= self._LIMITE_SAQUES

        if excedeu_limite:
            print("\nOperação falhou! O valor do saque excede o limite!")
            return False

        elif excedeu_saques:
            print("\nOperação falhou! Número máximo de saques excedido!")
            return False

        else:
            return super().sacar(valor)

    def __str__(self):
        return f"\nAgência: {self.agencia} | C/C: {self.numero}\nTitular: {self.cliente.nome} | Saldo: R${self.saldo}\n"

    def __repr__(self) -> str:
        return f"[{self.__class__.__name__}]: [Ag: {self.agencia}, Conta: {self.numero}, Cliente: {self.cliente.nome}]"

