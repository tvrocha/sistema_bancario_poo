from datetime import datetime
from pathlib import Path

from db import filtrar_cpf

PASTA_RAIZ = Path(__file__).parent


def log_transacao(func):
    def envelope(*args, **kwargs):
        resultado = func(*args, **kwargs)
        if (
            func.__name__.lower() == "cadastrar_clientes"
            or func.__name__.lower() == "criar_nova_conta"
        ):
            with open(
                PASTA_RAIZ / "cadastra_clientes_log.txt",
                "a",
                encoding="utf-8",
                newline="",
            ) as arquivo_cadastros:
                arquivo_cadastros.write(
                    f'[{datetime.now().strftime(r"%d-%m-%Y %H:%M:%S")}] | Função: {func.__name__.upper()} | Args: [{args}] & [{kwargs}] | Retorno: {resultado}\n'
                )
        else:
            with open(
                PASTA_RAIZ / "log.txt", "a", encoding="utf-8", newline=""
            ) as arquivo_log:
                arquivo_log.write(
                    f'[{datetime.now().strftime(r"%d-%m-%Y %H:%M:%S")}] | Função: {func.__name__.upper()} | Args: [{args}] & [{kwargs}] | Retorno: {resultado}\n'
                )

    return envelope


def organizar_menu(titulo, opcoes=[]):
    print()
    print("=" * 32)
    print(f"{titulo:^32}")
    print("=" * 32)
    print()
    for i, opcao in enumerate(opcoes):
        print(f'[{i + 1 if opcao != "Sair" else "0"}] - {opcao.title()}')
    print()


def menu_cadastro():
    organizar_menu(
        "Sistema Bancário - Cadastro",
        ["Cadastrar", "Já tenho cadastro", "Clientes cadastrados", "Sair"],
    )
    return input("Entre com a opção: ")


def selecionar_contas(contas):
    if len(contas) == 1:
        conta = contas[0]
    else:
        organizar_menu(
            "Seleção de Conta", [f"Conta {conta.numero}" for conta in contas] + ["Sair"]
        )
        while True:
            opcao = int(input("Escolha a conta: "))
            if opcao > len(contas) or opcao < 0:
                print("\nOpção inválida. Tente novamente!")
            else:
                break
        if opcao == 0:
            return opcao
        conta = contas[opcao - 1]
    return conta


def menu_opcoes(cpf_login, lista_clientes):
    cliente = filtrar_cpf(cpf_login)
    contas = cliente.contas
    conta = selecionar_contas(contas)
    if conta == 0:
        return "0", None
    organizar_menu(
        "Menu - Sistema Bancário",
        [
            "Deposito",
            "Saque",
            "Extrato",
            "Cadastrar nova conta",
            "Listar contas",
            "Sair",
        ],
    )
    print(f"Titular: {cliente.nome}")
    print(f"Conta: {conta.numero}")
    print(f"Saldo: R${conta.saldo:,.2f}")
    return input("Entre com a opção: "), conta

