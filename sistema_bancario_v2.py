from models import PessoaFisica, ContaCorrente, ContaIterador
from transacoes import Saque, Deposito
from utils import log_transacao, organizar_menu, menu_cadastro, menu_opcoes
from datetime import datetime

from db import criar_conexao, criar_cursor, cadastrar_cliente_db, cadastrar_conta_db, filtrar_cpf, listar_clientes_db
from db import atualizar_saldo_db

@log_transacao
def cadastrar_clientes(clientes):
    organizar_menu("Cadastrar Cliente")
    while True:
        cpf = input("Informe o CPF [apenas números]: ")
        if not cpf.isdigit() or len(cpf) != 11:
            print("\nCPF inválido. Tente novamente.")
        else:
            break
    novo_cliente = filtrar_cpf(cpf)
    if novo_cliente:
        print("\nJá existe conta com este CPF.")
        return
    nome = input("Informe o nome completo: ")
    while True:
        data_nascimento = input("Informe a data de nascimento [dd-mm-aaaa]: ")
        try:
            datetime.strptime(data_nascimento, r"%d-%m-%Y")
            break
        except ValueError:
            print("\nData de nascimento inválida. Tente novamente.")
    endereco = input("Informe endereco [Rua, Numero - Bairro - Cidade/MG]: ")
    novo_cliente = PessoaFisica(
        cpf=cpf, nome=nome, data_nascimento=data_nascimento, endereco=endereco
    )
    clientes.append(novo_cliente)
    criar_nova_conta(novo_cliente, clientes)
    cadastrar_cliente_db(novo_cliente)
    print(f"\nCliente [{nome}] cadastrado com sucesso!")


@log_transacao
def criar_nova_conta(novo_cliente, clientes):
    max_num_conta = 0
    for cliente in clientes:
        for conta in cliente.contas:
            max_num_conta = max(max_num_conta, conta.numero)
    num_conta = max_num_conta + 1   
    nova_conta = ContaCorrente.nova_conta(cliente=novo_cliente, numero=num_conta)
    novo_cliente.adicionar_conta(nova_conta)
    cadastrar_conta_db(novo_cliente)
    print(f"\nConta {num_conta} criado com sucesso.")


def login():
    organizar_menu("Login")
    cpf_login = input("Entre com o CPF [apenas números]: ")
    se_cadastrado = filtrar_cpf(cpf_login)
    if se_cadastrado:
        print("\nLogin realizado!")
        return cpf_login
    else:
        print("\nCPF não cadastrado!")
    return None


@log_transacao
def realizar_deposito(conta):
    organizar_menu("Depósito")
    print(f"Saldo atual: R${conta.saldo:,.2f}")
    valor = float(input("Informe o valor do depósito: R$"))
    transacao = Deposito(valor)
    conta.adicionar_transacao(transacao)
    atualizar_saldo_db(conta)
    # registrar_transacoes_db(transacao, conta.numero)
    
    

@log_transacao
def realizar_saque(conta):
    organizar_menu("Saque")
    valor = float(input("Informe o valor do saque: R$"))
    transacao = Saque(valor)
    conta.adicionar_transacao(transacao)
    atualizar_saldo_db(conta)
    # registrar_transacoes_db(transacao, conta.numero)


@log_transacao
def exibir_extrato(contas):
    organizar_menu("Extrato")
    for conta in contas.historico.exibir_extrato(contas):  # tipo_transacao='Saque' caso queira filtrar
        print(conta)


def exibir_clientes(clientes):
    if not clientes:
        print("\nNenhum cliente encontrado.")
    else:
        for cliente_info in clientes:
            print()
            print(
                f"Cliente: {cliente_info.nome} | CPF: {cliente_info.cpf}"
                f"\nNascimento: {cliente_info.data_nascimento} | Contas: {[conta.numero for conta in cliente_info.contas]}"
            )


def exibir_contas(cliente):
    for conta in ContaIterador(cliente.cliente.contas):
        print(conta)


def resetar_banco_dados():
    with criar_conexao() as conexao:
        with criar_cursor(conexao) as cursor:
            cursor.executescript(
                "DELETE FROM cliente;"
                "DELETE FROM conta;"
                "DELETE FROM transacao;"
                "DELETE FROM sqlite_sequence WHERE name = 'cliente';"
                "DELETE FROM sqlite_sequence WHERE name = 'conta';"
                "DELETE FROM sqlite_sequence WHERE name = 'transacao';"
            )
    global clientes
    clientes = []



while True:

    sair = False
    login_realizado = None

    clientes = listar_clientes_db()

    while not login_realizado:

        opcao_cadastro = menu_cadastro()

        if opcao_cadastro == "1":
            cadastrar_clientes(clientes)

        elif opcao_cadastro == "2":
            login_realizado = login()

        elif opcao_cadastro == "3":
            exibir_clientes(clientes)
            break

        elif opcao_cadastro == "0":
            organizar_menu("Fim do Programa")
            sair = True
            break

        elif opcao_cadastro == "10":
            resetar_banco_dados()
            print("\nBanco de Dados resetado com sucesso!")

        else:
            organizar_menu("Opção Inválida")

    if sair:
        break

    while login_realizado:
        opcao_menu, conta = menu_opcoes(login_realizado, clientes)
        if opcao_menu == "0":
            organizar_menu("Sair da Conta")
            break
        elif opcao_menu == "1":
            realizar_deposito(conta)
        elif opcao_menu == "2":
            realizar_saque(conta)
        elif opcao_menu == "3":
            exibir_extrato(conta)
        elif opcao_menu == "4":
            criar_nova_conta(filtrar_cpf(login_realizado), clientes)
        elif opcao_menu == "5":
            exibir_contas(conta)
        else:
            organizar_menu("Opção Inválida")
