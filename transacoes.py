from abc import ABC, abstractclassmethod, abstractproperty
from datetime import datetime

class Historico:
    def __init__(self, conta, transacoes=None) -> None:
        if transacoes is None:
            transacoes = []
        self._transacoes = self._listar_transacoes_db(conta)

    def adicionar_transacao(self, transacao, conta_numero):
        # self._transacoes.append({"Tipo": transacao.__class__.__name__, "Valor": transacao.valor, "Data": datetime.now().strftime(r"%d-%m-%Y %H:%M:%S")})
        self._registrar_transacoes_db(transacao, conta_numero)      
        
    def _registrar_transacoes_db(self, transacao, conta_numero):
        from db import registrar_transacoes_db
        registrar_transacoes_db(transacao, conta_numero)    
    
    def _listar_transacoes_db(self, conta):
        from db import listar_transacoes_db
        return listar_transacoes_db(conta)

    def exibir_extrato(self, conta, tipo_transacao=None):
        if not self._transacoes:
            print("\nNenhuma transação realizada!\n")
        else:
            for transacao in self._transacoes:
                if tipo_transacao is None or transacao["Tipo"].lower() == tipo_transacao.lower():
                    yield f'Tipo: {transacao["Tipo"]} | Valor: R${transacao["Valor"]:.2f} | Horário: {transacao["Data"]}'
            print()
            print(f"Saldo: R${conta.saldo:.2f}")

    @property
    def transacoes(self):
        return self._transacoes

    def transacoes_do_dia(self):

        transacoes_hoje = len(
            [
                transacao
                for transacao in self._transacoes
                if datetime.strptime(transacao["Data"], r"%d-%m-%Y %H:%M:%S").strftime(r"%d-%m-%Y")
                == datetime.today().strftime(r"%d-%m-%Y")
            ]
        )
        return transacoes_hoje


class Transacao(ABC):
    @abstractclassmethod
    def executar(self, conta):
        pass

    @property
    @abstractproperty
    def valor(self):
        pass


class Saque(Transacao):
    def __init__(self, valor) -> None:
        self._valor = valor

    def executar(self, conta):
        sucesso_transacao = conta.sacar(self.valor)
        return sucesso_transacao
        # if sucesso_transacao:
        #     conta.historico.adicionar_transacao(self, conta.numero)

    @property
    def valor(self):
        return self._valor

    def __repr__(self) -> str:
        return f"[{self.__class__.__name__}]: Valor R${self.valor:,.2f}"


class Deposito(Transacao):
    def __init__(self, valor) -> None:
        self._valor = valor

    def executar(self, conta):
        sucesso_transacao = conta.depositar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self, conta.numero)

    @property
    def valor(self):
        return self._valor
    
    def __repr__(self) -> str:
        return f"[{self.__class__.__name__}]: Valor R${self.valor:,.2f}"


