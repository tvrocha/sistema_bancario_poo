from abc import ABC, abstractmethod, abstractproperty
from datetime import datetime

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
    
    def realizar_transacao(self, conta, transacao):
        pass

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
    
class Conta:
    def __init__(self, numero, cliente) -> None:
        self._saldo = 0 # float
        self._numero = numero # int - numero da conta
        self._agencia = '0001' # str - '0001'
        self._cliente = cliente 
        self._historico = Historico() 

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
            print('\Saldo insuficiente!\n')
            return False
        elif valor > 0:
            self._saldo -= valor
            print('\nSaque realizado com sucesso!')
            return True
        else:
            print('\nOpção inválida!')
            return False
        
    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            print('\nDepósito realizado com sucesso')
            return True
        else:
            print('\nValor inválido!')
            return False
    
    def adicionar_transacao(self, transacao):
        transacao.executar(self)
    
class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite_saques=3, limite_valor_saque=500) -> None:
        super().__init__(numero, cliente)
        self._LIMITE_SAQUES = limite_saques
        self._LIMITE_VALOR_SAQUES = limite_valor_saque
    
    def sacar(self, valor):
        numero_saques = len([transacao for transacao in self.historico.transacoes if transacao['Tipo'] == Saque.__name__])

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
        return f'\nAgência: {self.agencia} | C/C: {self.numero}\nTitular: {self.cliente.nome} | Saldo: R${self.saldo}\n'

class Historico:
    def __init__(self, transacoes=None) -> None:
        if transacoes is None:
            transacoes = []
        self._transacoes = transacoes

    def adicionar_transacao(self, transacao):
        self._transacoes.append(
            {
                'Tipo': transacao.__class__.__name__,
                'Valor': transacao.valor,
                'Data': datetime.now().strftime(r"%d-%m-%Y %H:%M:%S"),
            }
        )
    
    def exibir_extrato(self, conta): ## Alterar a forma de mostrar o extrato e usar um gerador
        if not self._transacoes:
            print('\nNenhuma transação realizada!\n')
        else:
            for transacao in self._transacoes:
                yield f'Tipo: {transacao["Tipo"]} | Valor: R${transacao["Valor"]:.2f} | Horário: {transacao["Data"]}'
            print()
            print(f'Saldo: R${conta.saldo:.2f}')
    
    @property
    def transacoes(self):
        return self._transacoes

class Transacao(ABC): 
    @abstractmethod
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
        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)
    
    @property
    def valor(self):
        return self._valor

class Deposito(Transacao):
    def __init__(self, valor) -> None:
        self._valor = valor
    
    def executar(self, conta):
        sucesso_transacao = conta.depositar(self.valor)
        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)
    
    @property
    def valor(self):
        return self._valor

def log_transacao(func):
    def envelope(*args, **kwargs):        
        func(*args, **kwargs)
        print(f'{func.__name__.upper()} : {datetime.now().strftime(r"%d-%m-%Y %H:%M:%S")}')
    return envelope

def organizar_menu(titulo, opcoes=[]):
    print()
    print('=' * 32)
    print(f'{titulo:^32}')
    print('=' * 32)
    print()
    for i, opcao in enumerate(opcoes):
        print(f'[{i + 1 if opcao != "Sair" else "0"}] - {opcao.title()}')
    print()

def menu_cadastro():
    organizar_menu('Sistema Bancário - Cadastro', ['Cadastrar', 'Já tenho cadastro', 'Clientes cadastrados', 'Sair'])
    return input('Entre com a opção: ')

def menu_opcoes(cpf_login, lista_clientes):
    cliente = [cliente for cliente in lista_clientes if cliente.cpf == cpf_login][0]
    contas = cliente.contas
    if len(contas) == 1:
        conta = contas[0]
    else:
        organizar_menu('Seleção de Conta', [f'Conta {conta.numero}' for conta in contas] + ['Sair'])
        while True:
            opcao = int(input('Escolha a conta: '))
            if opcao > len(contas) or opcao < 0:
                print('\nOpção inválida. Tente novamente!')
            else:
                break
        if opcao == 0:
            return '0', None
        conta = contas[opcao - 1]
    organizar_menu('Menu - Sistema Bancário', ['Deposito', 'Saque', 'Extrato', 'Cadastrar nova conta', 'Listar contas', 'Sair'])
    print(f'Titular: {cliente.nome}')
    print(f'Conta: {conta.numero}')
    return input('Entre com a opção: '), conta

@log_transacao
def cadastrar_clientes(clientes):
    organizar_menu('Cadastrar Cliente')
    while True:
        cpf = input('Informe o CPF [apenas números]: ')
        if not cpf.isdigit() or len(cpf) != 11:
            print('\nCPF inválido. Tente novamente.\n')
        else:
            break
    novo_cliente = filtrar_cpf(cpf, clientes)
    if novo_cliente:
        print('\nJá existe conta com este CPF.\n')
        return
    nome = input('Informe o nome completo: ')
    while True:
        data_nascimento = input('Informe a data de nascimento [dd-mm-aaaa]: ')
        try:
            datetime.strptime(data_nascimento, r'%d-%m-%Y')
            break
        except ValueError:
            print('\nData de nascimento inválida. Tente novamente.\n')
    endereco = input('Informe endereco [Rua, Numero - Bairro - Cidade/MG]: ')
    novo_cliente = PessoaFisica(cpf=cpf, nome=nome, data_nascimento=data_nascimento, endereco=endereco)
    clientes.append(novo_cliente)
    criar_nova_conta(novo_cliente, clientes)    
    print(f'\nCliente [{nome}] cadastrado com sucesso!\n')

@log_transacao
def criar_nova_conta(novo_cliente, clientes):
    max_num_conta = 0
    for cliente in clientes:
        for conta in cliente.contas:
            max_num_conta = max(max_num_conta, conta.numero)
    num_conta = max_num_conta + 1
    nova_conta = ContaCorrente.nova_conta(cliente=novo_cliente, numero=num_conta)
    novo_cliente.adicionar_conta(nova_conta)
    print(f'\nConta {num_conta} criado com sucesso.\n')

def filtrar_cpf(cpf, clientes):
    filtro_cliente = [cliente for cliente in clientes if cliente.cpf == cpf ]
    return filtro_cliente[0] if filtro_cliente else None

def login(clientes):
    organizar_menu('Login')
    cpf_login = input('Entre com o CPF [apenas números]: ')
    se_cadastrado = filtrar_cpf(cpf_login, clientes)
    if se_cadastrado:
        print('\nLogin realizado!\n')
        return cpf_login
    else:
        print('\nCPF não cadastrado!\n')
    return None

@log_transacao
def realizar_deposito(conta):
    organizar_menu('Depósito')
    valor = float(input('Informe o valor do depósito: R$'))
    transacao = Deposito(valor)
    conta.adicionar_transacao(transacao)

@log_transacao
def realizar_saque(conta):
    organizar_menu('Saque')
    valor = float(input('Informe o valor do saque: R$'))
    transacao = Saque(valor)
    conta.adicionar_transacao(transacao)

@log_transacao
def exibir_extrato(contas): 
    organizar_menu('Extrato')
    for conta in contas.historico.exibir_extrato(contas): 
        print(conta)

def exibir_clientes(clientes):
    if not clientes:
        print('\nNenhum cliente encontrado.')
    else:
        for cliente in clientes:
            print(f'Cliente: {cliente.nome} | CPF: {cliente.cpf} | Nascimento: {cliente.data_nascimento}')

def exibir_contas(cliente):
    for conta in ContaIterador(cliente.cliente.contas):
        print(conta)

clientes = []

while True:

    sair = False
    login_realizado = None

    while not login_realizado:

        opcao_cadastro = menu_cadastro()

        if opcao_cadastro == '1':
            cadastrar_clientes(clientes)
        
        elif opcao_cadastro == '2':
            login_realizado = login(clientes)
        
        elif opcao_cadastro == '3':
            exibir_clientes(clientes)
            break
        
        elif opcao_cadastro == '0':
            organizar_menu('Fim do Programa')
            sair = True
            break
        
        else:
            organizar_menu('Opção Inválida')

    if sair:
        break

    while login_realizado:

        opcao_menu, conta = menu_opcoes(login_realizado, clientes) 

        if opcao_menu == '0':
            organizar_menu('Sair da Conta')
            aux_conta_logada = 0
            break
        
        elif opcao_menu == '1':
            realizar_deposito(conta)
        
        elif opcao_menu == '2':
            realizar_saque(conta)
        
        elif opcao_menu == '3':
            exibir_extrato(conta)
        
        elif opcao_menu == '4':
            criar_nova_conta(filtrar_cpf(login_realizado, clientes), clientes)
        
        elif opcao_menu == '5':
            exibir_contas(conta)
        
        else:
            organizar_menu('Opção Inválida')

