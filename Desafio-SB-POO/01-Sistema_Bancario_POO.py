# Importação de Módulos Necessários
import textwrap
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path

ROOT_PATH = Path(__file__).parent


# Definição do Decorador de Log
def log_transacao(func):
    def envelope(*args, **kwargs):
        # Execução da função decorada
        resultado = func(*args, **kwargs)

        # Preparação do log
        data_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        nome_funcao = func.__name__
        argumentos = f"args={args}, kwargs={kwargs}"
        retorno = f"retorno={resultado}"

        # Registro no log
        with open(ROOT_PATH / "log.txt", "a", encoding="utf-8") as arquivo:
            arquivo.write(f"[{data_hora}] Função '{nome_funcao}' executada com {argumentos}. {retorno}\n")

        return resultado

    return envelope


# Definição da classe Cliente
class Cliente:
    def __init__(self, endereco):
        self._endereco = endereco
        self._contas = []

    @log_transacao
    def realizar_transacao(self, conta, transacao):
        tipo_transacao = transacao.__class__.__name__

        if tipo_transacao == "Deposito" and conta.historico.numero_depositos_do_dia() >= 3:
            return "\n@@@ Operação falhou! O limite diário de depósitos foi atingido. @@@"

        if tipo_transacao == "Saque" and conta.historico.numero_saques_do_dia() >= 3:
            return "\n@@@ Operação falhou! O limite diário de saques foi atingido. @@@"

        transacao.registrar(conta)
        return "\n=== Operação realizada com sucesso! ==="

    @log_transacao
    def adicionar_conta(self, conta):
        self._contas.append(conta)
        return "\n=== Conta adicionada ao cliente com sucesso! ==="


# Definição da classe PessoaFisica que herda de Cliente
class PessoaFisica(Cliente):
    def __init__(self, nome, data_nascimento, cpf, endereco):
        super().__init__(endereco)
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf

    def __repr__(self):
        return f"<{self.__class__.__name__}: ('{self.nome}', '{self.cpf}')>"


# Definição da classe Conta
class Conta:
    _numero_sequencial = 1

    def __init__(self, cliente):
        self._saldo = 0
        self._numero = Conta._numero_sequencial
        Conta._numero_sequencial += 1
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()

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

    @log_transacao
    def sacar(self, valor):
        saldo = self.saldo
        excedeu_saldo = valor > saldo

        if excedeu_saldo:
            return "\n@@@ Operação falhou! Você não tem saldo suficiente. @@@"

        if valor > 0:
            self._saldo -= valor
            return "\n=== Saque realizado com sucesso! ==="
        return "\n@@@ Operação falhou! O valor do saque deve ser positivo. @@@"

    @log_transacao
    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            return "\n=== Depósito realizado com sucesso! ==="
        return "\n@@@ Operação falhou! O valor do depósito deve ser positivo. @@@"

    def realizar_transacao(self, transacao):
        transacao.registrar(self)


# Definição da classe ContaCorrente que herda de Conta
class ContaCorrente(Conta):
    def __init__(self, cliente, limite=500):
        super().__init__(cliente)
        self._limite = limite

    def sacar(self, valor):
        excedeu_limite = valor > self._limite

        if excedeu_limite:
            return "\n@@@ Operação falhou! O valor do saque excede o limite. @@@"
        return super().sacar(valor)

    def __repr__(self):
        return f"<{self.__class__.__name__}: ('{self.agencia}', '{self.numero}', '{self.cliente.nome}')>"

    def __str__(self):
        return f"""\
        Agência:\t{self.agencia}
        C/C:\t{self.numero}
        Titular:\t{self.cliente.nome}
        """


# Definição da classe Historico para registrar transações
class Historico:
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes

    def adicionar_transacao(self, transacao):
        self._transacoes.append(
            {
                "tipo": transacao.__class__.__name__,
                "valor": transacao.valor,
                "data": datetime.now().strftime("%d/%m/%Y" + "\t" + "%H:%M:%S"),
            }
        )

    def gerar_relatorio(self):
        relatorio = "\t** Relatório de Transações **\n\n"
        for transacao in self._transacoes:
            relatorio += f"{transacao['data']}: {transacao['tipo']} de R$ {transacao['valor']:.2f}\n"
        return relatorio

    def transacoes_do_dia(self):
        data_atual = datetime.now().date()
        return [
            transacao
            for transacao in self._transacoes
            if datetime.strptime(transacao["data"], "%d/%m/%Y\t%H:%M:%S").date() == data_atual
        ]

    def numero_saques_do_dia(self):
        return len([transacao for transacao in self.transacoes_do_dia() if transacao["tipo"] == "Saque"])

    def numero_depositos_do_dia(self):
        return len([transacao for transacao in self.transacoes_do_dia() if transacao["tipo"] == "Deposito"])

    def registrar_transacao(self, transacao):
        self._transacoes.append(
            {
                "tipo": transacao.__class__.__name__,
                "valor": transacao.valor,
                "data": datetime.now().strftime("%d/%m/%Y" + "\t" + "%H:%M:%S"),
            }
        )


# Definição da classe abstrata Transacao
class Transacao(ABC):
    @property
    @abstractmethod
    def valor(self):
        pass

    @abstractmethod
    def registrar(self, conta):
        pass


# Definição da classe Saque que herda de Transacao
class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso_transacao = conta.sacar(self.valor)

        if sucesso_transacao:
            conta.historico.registrar_transacao(self)


# Definição da classe Deposito que herda de Transacao
class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso_transacao = conta.depositar(self.valor)

        if sucesso_transacao:
            conta.historico.registrar_transacao(self)


# Função para exibir o menu de opções
def menu():
    print("\n\n=== Bem-vindo ao Sistema Bancário ===")
    print("\n[1] - Depositar")
    print("[2] - Sacar")
    print("[3] - Exibir Extrato")
    print("[4] - Criar Cliente")
    print("[5] - Criar Conta")
    print("[6] - Listar Contas")
    print("[q] - Sair")
    return input("Escolha uma opção: 👉  ")


# Função para filtrar clientes pelo CPF
def filtrar_cliente(cpf, clientes):
    clientes_filtrados = [cliente for cliente in clientes if cliente.cpf == cpf]
    return clientes_filtrados[0] if clientes_filtrados else None


# Função para recuperar uma conta associada a um cliente
def recuperar_conta_cliente(cliente):
    if not cliente._contas:
        print("\n@@@ Cliente não possui conta! @@@")
        return

    return cliente._contas[0]


# Função Principal para Operar o Sistema Bancário
def main():
    clientes = []
    contas = []

    while True:
        opcao = menu()

        if opcao == "1":
            cpf = input("Informe o CPF do cliente: ")
            cliente = filtrar_cliente(cpf, clientes)

            if not cliente:
                print("\n@@@ Cliente não encontrado! @@@")
                continue

            valor = float(input("Informe o valor do depósito: "))
            transacao = Deposito(valor)
            conta = recuperar_conta_cliente(cliente)

            if not conta:
                continue

            print(cliente.realizar_transacao(conta, transacao))

        elif opcao == "2":
            cpf = input("Informe o CPF do cliente: ")
            cliente = filtrar_cliente(cpf, clientes)

            if not cliente:
                print("\n@@@ Cliente não encontrado! @@@")
                continue

            valor = float(input("Informe o valor do saque: "))
            transacao = Saque(valor)
            conta = recuperar_conta_cliente(cliente)

            if not conta:
                continue

            print(cliente.realizar_transacao(conta, transacao))

        elif opcao == "3":
            cpf = input("Informe o CPF do cliente: ")
            cliente = filtrar_cliente(cpf, clientes)

            if not cliente:
                print("\n@@@ Cliente não encontrado! @@@")
                continue

            conta = recuperar_conta_cliente(cliente)
            if not conta:
                continue

            print("\n============ EXTRATO ============")
            extrato = conta.historico.gerar_relatorio()
            print("Não foram realizadas movimentações." if not extrato else extrato)
            print(f"\nSaldo:\tR$ {conta.saldo:.2f}")
            print("==================================")

        elif opcao == "4":
            cpf = input("Informe o CPF do cliente: ")
            cliente = filtrar_cliente(cpf, clientes)

            if cliente:
                print("\n@@@ Já existe cliente com esse CPF! @@@")
                continue

            nome = input("Informe o nome do cliente: ")
            data_nascimento = input("Informe a data de nascimento do cliente: ")
            endereco = input("Informe o endereço do cliente: ")

            cliente = PessoaFisica(nome, data_nascimento, cpf, endereco)
            clientes.append(cliente)

            print("\n=== Cliente criado com sucesso! ===")

        elif opcao == "5":
            cpf = input("Informe o CPF do cliente: ")
            cliente = filtrar_cliente(cpf, clientes)

            if not cliente:
                print("\n@@@ Cliente não encontrado! @@@")
                continue

            conta = ContaCorrente(cliente)
            contas.append(conta)
            cliente.adicionar_conta(conta)

            print("\n=== Conta criada com sucesso! ===")

        elif opcao == "6":
            for conta in contas:
                print("=" * 100)
                print(textwrap.dedent(str(conta)))

        elif opcao == "q":
            break

        else:
            print("\n@@@ Operação inválida! @@@")


# Execução do Sistema
if __name__ == "__main__":
    main()
