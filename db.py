import sqlite3
from datetime import datetime

from pathlib import Path
from contextlib import contextmanager

PASTA_RAIZ = Path(__file__).parent

@contextmanager
def criar_conexao():
    conexao = sqlite3.connect(PASTA_RAIZ / 'clientes_bd.db')
    try:
        yield conexao
    finally:
        conexao.close() 


@contextmanager
def criar_cursor(conexao):
    cursor = conexao.cursor()
    try:
        yield cursor
        conexao.commit()
    finally:
        cursor.close()


def criar_tabela(cursor):
    with criar_conexao() as conexao:
        with criar_cursor(conexao) as cursor:
            cursor.executescript("""
            CREATE TABLE IF NOT EXISTS cliente (
                cpf TEXT PRIMARY KEY,
                nome TEXT NOT NULL,
                data_nascimento DATETIME,
                endereco TEXT 
                );
                        
            CREATE TABLE IF NOT EXISTS conta (
                numero INTEGER PRIMARY KEY,
                agencia TEXT NOT NULL,
                saldo REAL,
                cliente_cpf TEXT,
                FOREIGN KEY (cliente_cpf) REFERENCES cliente (cpf)
                );
            
            CREATE TABLE IF NOT EXISTS transacao (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tipo TEXT,
                valor REAL,
                data DATETIME,
                conta_numero INTEGER,
                FOREIGN KEY (conta_numero) REFERENCES conta (numero)
                );
            """)


def cadastrar_cliente_db(cliente: object): # objeto PessoaFisica
    with criar_conexao() as conexao:
        with criar_cursor(conexao) as cursor:
            cursor.execute(
                "INSERT INTO cliente (cpf, nome, data_nascimento, endereco) VALUES (?, ?, ?, ?)",
                (cliente.cpf, cliente.nome, cliente.data_nascimento, cliente.endereco)
                )


def cadastrar_conta_db(cliente):
    with criar_conexao() as conexao:
        with criar_cursor(conexao) as cursor:
            cursor.execute(
                "INSERT INTO conta (numero, agencia, saldo, cliente_cpf) VALUES (?, ?, ?, ?)",
                (cliente.contas[-1].numero, cliente.contas[-1].agencia, cliente.contas[-1].saldo, cliente.cpf)
            )


def filtrar_cpf(cpf):
    from models import ContaCorrente, PessoaFisica
    with criar_conexao() as conexao:
        with criar_cursor(conexao) as cursor:
            cursor.execute(
                "SELECT cpf, nome, data_nascimento, endereco FROM cliente WHERE cpf = (?)", (cpf,)
            )
            resultado_cliente = cursor.fetchone()

            if not resultado_cliente:
                return None          
            
            cliente = PessoaFisica(*resultado_cliente)

            # Buscar as contas do cliente
            cursor.execute(
                "SELECT numero, agencia, saldo FROM conta WHERE cliente_cpf = (?)", (cpf,)
            )
            contas = cursor.fetchall()

            for conta_info in contas:
                numero, agencia, saldo = conta_info
                conta = ContaCorrente(numero, cliente)
                conta._saldo = saldo
                cliente.adicionar_conta(conta)

            return cliente


def listar_clientes_db():
    from models import ContaCorrente, PessoaFisica
    clientes = []

    with criar_conexao() as conexao:
        with criar_cursor(conexao) as cursor:
            cursor.execute(
                "SELECT cpf, nome, data_nascimento, endereco FROM cliente"
            )
            resultados = cursor.fetchall()

            for resultado in resultados:
                cpf, nome, data_nascimento, endereco = resultado
                cliente = PessoaFisica(cpf, nome, data_nascimento, endereco)
                
                # Buscar as contas do cliente
                cursor.execute(
                    "SELECT numero, agencia, saldo FROM conta WHERE cliente_cpf = (?)", (cpf,)
                )
                contas = cursor.fetchall()

                for conta_info in contas:
                    numero, agencia, saldo = conta_info
                    conta = ContaCorrente(numero, cliente)
                    conta._saldo = saldo
                    cliente.adicionar_conta(conta)
                    atualizar_saldo_db(conta)
                
                clientes.append(cliente)
            
    return clientes

def atualizar_saldo_db(conta):
    with criar_conexao() as conexao:
        with criar_cursor(conexao) as cursor:
            cursor.execute(
                "UPDATE conta SET saldo = (?) WHERE numero = (?)", (conta.saldo, conta.numero)
            )

def registrar_transacoes_db(transacao, conta_numero):
    with criar_conexao() as conexao:
        with criar_cursor(conexao) as cursor:
            cursor.execute(
                "INSERT INTO transacao (tipo, valor, data, conta_numero) VALUES (?, ?, ?, ?)",
                (transacao.__class__.__name__, transacao.valor, datetime.now().strftime(r"%d-%m-%Y %H:%M:%S"), conta_numero)
            )

def listar_transacoes_db(conta):
    transacoes = []
    with criar_conexao() as conexao:
        with criar_cursor(conexao) as cursor:
            cursor.execute(
                "SELECT tipo, valor, data FROM transacao WHERE conta_numero = (?)", (conta.numero,)
            )

            resultado = cursor.fetchall()
            
            for tipo, valor, data in resultado:
                transacao = {"Tipo": tipo,
                             "Valor": valor,
                             "Data": data}
                transacoes.append(transacao)

    return transacoes