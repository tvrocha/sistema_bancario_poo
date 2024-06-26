# Sistema Bancário em Python

Este projeto implementa um sistema bancário simples em Python, utilizando persistência de dados em SQLite para clientes, contas e transações.

## Funcionalidades

### Classes Principais

- **PessoaFisica**: Representa um cliente pessoa física com CPF, nome, data de nascimento e endereço.
- **ContaCorrente**: Modelo de conta bancária com número, agência, saldo e histórico de transações.
- **Transações**: Implementa classes como Saque e Depósito, que herdam de uma classe abstrata Transação.
- **Historico**: Gerencia o histórico de transações de uma conta.

### Funções Principais

- **cadastrar_clientes(clientes)**: Permite o cadastro de novos clientes, verificando duplicidades por CPF.
- **criar_nova_conta(novo_cliente, clientes)**: Cria uma nova conta para um cliente já cadastrado.
- **login()**: Realiza o login de um cliente existente utilizando o CPF.
- **realizar_deposito(conta)**: Realiza um depósito em uma conta existente.
- **realizar_saque(conta)**: Realiza um saque em uma conta existente.
- **exibir_extrato(contas)**: Exibe o extrato das transações de uma conta.
- **exibir_clientes(clientes)**: Lista todos os clientes cadastrados.
- **exibir_contas(cliente)**: Lista todas as contas de um cliente.

### Banco de Dados

- **SQLite**: Utilizado para persistência dos dados de clientes, contas e transações.
- **Funções de Banco de Dados**:
  - `criar_conexao()`: Cria uma conexão com o banco de dados.
  - `criar_cursor(conexao)`: Cria um cursor para executar comandos SQL.
  - `cadastrar_cliente_db(cliente)`: Insere um novo cliente na tabela `cliente`.
  - `cadastrar_conta_db(cliente)`: Insere uma nova conta na tabela `conta`.
  - `filtrar_cpf(cpf)`: Busca um cliente pelo CPF no banco de dados.
  - `listar_clientes_db()`: Lista todos os clientes cadastrados no banco de dados.
  - `atualizar_saldo_db(conta)`: Atualiza o saldo de uma conta no banco de dados.
  - `registrar_transacoes_db(transacao, conta_numero)`: Registra uma nova transação no banco de dados.
  - `listar_transacoes_db(conta)`: Lista todas as transações de uma conta específica.

## Utilitários

- **log_transacao(func)**: Decorador que registra todas as transações realizadas em arquivos de log.

### Menu

- **organizar_menu(titulo, opcoes)**: Função auxiliar para exibir menus no console.
- **menu_cadastro()**: Exibe opções de cadastro para novos clientes.
- **menu_opcoes(cpf_login, lista_clientes)**: Exibe opções de operações disponíveis após o login.

## Executando o Programa

Para executar o programa, execute `sistema_bancario_v2.py`. Certifique-se de ter o Python instalado e as dependências necessárias listadas no arquivo `requirements.txt`.

## Observações

- Este projeto foi desenvolvido como parte de um estudo sobre persistência de dados em Python usando SQLite e orientação a objetos.
- Para mais informações, consulte os arquivos individuais de cada módulo (`models.py`, `transacoes.py`, `utils.py`, `db.py`) para detalhes de implementação.

