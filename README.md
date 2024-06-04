# Sistema Bancário POO

Este é um sistema bancário desenvolvido em Python utilizando o paradigma de Programação Orientada a Objetos (POO).

## Funcionalidades

- **Cadastro de Clientes**: Permite cadastrar clientes no sistema.
- **Criação de Contas Correntes**: Permite a criação de contas correntes associadas a clientes.
- **Depósitos**: Permite realizar depósitos nas contas.
- **Saques**: Permite realizar saques nas contas, respeitando limites definidos.
- **Extrato**: Exibe um extrato das transações realizadas, juntamente com o saldo atual da conta.

## Estrutura do Código

- **Cliente**: Classe base para clientes.
- **PessoaFisica**: Subclasse de Cliente, representando uma pessoa física.
- **Conta**: Classe base para contas bancárias.
- **ContaCorrente**: Subclasse de Conta, representando uma conta corrente com limites de saque.
- **Historico**: Classe para manter um histórico de transações.
- **Transacao**: Classe abstrata para transações bancárias.
- **Saque**: Subclasse de Transacao, representando um saque.
- **Deposito**: Subclasse de Transacao, representando um depósito.

## Como Executar

1. Certifique-se de ter o Python 3 instalado em seu sistema.
2. Clone o repositório:
   ```sh
   git clone https://github.com/tvrocha/sistema_bancario_poo.git
   ```
3. Navegue até o diretório do projeto:
    ```sh
   cd sistema_bancario_poo
   ```
4. Execute o script Python:
    ```sh
    python sistema_bancario_v2.py
    ```

## Contribuindo

Contribuições são bem-vindas! Sinta-se à vontade para abrir uma _issue_ ou enviar um _pull request_.

## Licença

Este projeto está licenciado sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

---

**Nota**: Este é um projeto educativo desenvolvido para fins de aprendizado. Não é recomendado para uso em produção sem devidas melhorias e validações de segurança.
