# Sistema Bancário em Python

## Descrição

Este projeto implementa um sistema bancário simples em Python. Ele permite cadastrar clientes, criar contas, realizar depósitos e saques, e exibir extratos de transações. O sistema suporta múltiplos clientes e contas, com limites de saques e transações diárias.

## Funcionalidades

- **Cadastro de Clientes**: Permite cadastrar novos clientes com informações como CPF, nome, data de nascimento e endereço.
- **Criação de Contas**: Clientes podem ter múltiplas contas correntes.
- **Depósitos**: Clientes podem realizar depósitos em suas contas.
- **Saques**: Clientes podem realizar saques, respeitando limites de quantidade e valor.
- **Extratos**: Geração de extratos das transações realizadas.
- **Login**: Clientes podem acessar suas contas através do CPF.
- **Iterador de Contas**: Implementação de um iterador para listar contas de um cliente.

## Estrutura do Código

### Classes

- **ContaIterador**: Implementa um iterador para as contas de um cliente.
- **Cliente**: Classe base para clientes, armazena informações pessoais e contas associadas.
- **PessoaFisica**: Subclasse de Cliente, específica para pessoas físicas.
- **Conta**: Representa uma conta bancária genérica.
- **ContaCorrente**: Subclasse de Conta, específica para contas correntes, com limites de saque.
- **Historico**: Armazena o histórico de transações de uma conta.
- **Transacao (abstract)**: Classe abstrata para transações (sacar e depositar).
- **Saque**: Implementa a transação de saque.
- **Deposito**: Implementa a transação de depósito.

### Funções

- **log_transacao**: Decorador para registrar o horário das transações.
- **organizar_menu**: Função para exibir menus.
- **menu_cadastro**: Exibe o menu de cadastro e login.
- **menu_opcoes**: Exibe o menu de operações após o login.
- **cadastrar_clientes**: Cadastra novos clientes.
- **criar_nova_conta**: Cria uma nova conta para um cliente existente.
- **filtrar_cpf**: Filtra clientes pelo CPF.
- **login**: Realiza o login de um cliente.
- **realizar_deposito**: Realiza um depósito em uma conta.
- **realizar_saque**: Realiza um saque de uma conta.
- **exibir_extrato**: Exibe o extrato de uma conta.
- **exibir_clientes**: Lista todos os clientes cadastrados.
- **exibir_contas**: Lista todas as contas de um cliente.

## Como Executar

1. **Clone o repositório**: 
    ```sh
   git clone https://github.com/tvrocha/sistema_bancario_poo.git
   cd sistema_bancario_poo
   ```
2. **Execute o script**:
    ```sh
    python sistema_bancario_poo.py
    ```
3. **Navegue pelos menus para cadastrar clientes, criar contas, realizar depósitos e saques, e visualizar extratos.**

## Exemplo de Uso

- **Cadastro de Cliente**: Informe CPF, nome, data de nascimento e endereço.
- **Criação de Conta**: Automaticamente cria uma conta para o novo cliente.
- **Depósito**: Selecione a opção de depósito no menu, informe o valor e confirme.
- **Saque**: Selecione a opção de saque no menu, informe o valor (respeitando os limites) e confirme.
- **Extrato**: Visualize todas as transações realizadas na conta selecionada.


## Considerações Finais

Este projeto foi desenvolvido para ilustrar conceitos de orientação a objetos em Python, incluindo herança, composição e uso de classes abstratas. Adicionalmente, demonstra a utilização de decoradores e iteradores personalizados.

## Licença

Este projeto é licenciado sob a MIT License - veja o arquivo LICENSE para mais detalhes.
