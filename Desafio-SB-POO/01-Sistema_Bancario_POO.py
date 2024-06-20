# Importação de Módulos Necessários
from abc import ABC, abstractmethod
from datetime import datetime
import textwrap

# Definição da classe Cliente
class Cliente:
    def __init__(self, endereco):
        """Inicializa o Cliente com endereço e lista de contas."""
        self._endereco = endereco
        self._contas = []

    def realizar_transacao(self, conta, transacao):
        """Realiza uma transação em uma conta."""
        conta.realizar_transacao(transacao)
    
    def adicionar_conta(self, conta):
        """Adiciona uma conta ao cliente."""
        self._contas.append(conta)

# Definição da classe PessoaFisica que herda de Cliente
class PessoaFisica(Cliente):
    def __init__(self, nome, data_nascimento, cpf, endereco):
        """Inicializa a Pessoa Física com nome, data de nascimento, CPF e endereço."""
        super().__init__(endereco)
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf

# Definição da classe Conta
class Conta:
    def __init__(self, numero, cliente):
        """Inicializa a Conta com número, cliente, saldo e histórico."""
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()

    @classmethod
    def nova_conta(cls, numero, cliente):
        """Cria uma nova conta com um número e cliente fornecidos."""
        return cls(numero, cliente)
    
    @property
    def saldo(self):
        """Retorna o saldo da conta."""
        return self._saldo
    
    @property
    def numero(self):
        """Retorna o número da conta."""
        return self._numero
    
    @property
    def agencia(self):
        """Retorna a agência da conta."""
        return self._agencia
        
    @property
    def cliente(self):
        """Retorna o cliente associado à conta."""
        return self._cliente
    
    @property
    def historico(self):
        """Retorna o histórico de transações da conta."""
        return self._historico
    
    def sacar(self, valor):
        """Realiza um saque na conta se o valor for positivo e não exceder o saldo."""
        saldo = self.saldo
        excedeu_saldo = valor > saldo

        if excedeu_saldo:
            print("\n@@@ Operação falhou! Você não tem saldo suficiente. @@@")
            
        elif valor > 0:
            self._saldo -= valor
            print("\n=== Saque realizado com Sucesso! ===")
            return True

        else:
            print("\n@@@ Operação falhou! O valor do saque deve ser positivo. @@@")
            return False
    
    def depositar(self, valor):
        """Realiza um depósito na conta se o valor for positivo."""
        if valor > 0:
            self._saldo += valor
            print("\n=== Depósito realizado com Sucesso! ===")

        else:
            print("\n@@@ Operação falhou! O valor do depósito deve ser positivo. @@@")
            return False
        
        return True
    
    def realizar_transacao(self, transacao):
        """Realiza uma transação e registra no histórico."""
        transacao.registrar(self)

# Definição da classe ContaCorrente que herda de Conta
class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite=500, limite_saque=3):
        """Inicializa a Conta Corrente com limite de saque e limite de valor."""
        super().__init__(numero, cliente)
        self._limite = limite
        self._limite_saque = limite_saque

    def sacar(self, valor):
        """Realiza um saque, respeitando limites de valor e quantidade de saques."""
        numero_saques = len([transacao for transacao in self.historico.transacoes if transacao["tipo"] == Saque.__name__])

        excedeu_limite = valor > self._limite
        excedeu_saques = numero_saques >= self._limite_saque

        if excedeu_limite:
            print("\n@@@ Operação falhou! O valor do saque excede o limite. @@@")

        elif excedeu_saques:
            print("\n@@@ Operação falhou! O número de saques excede o limite. @@@")
            
        else:
            return super().sacar(valor)
        
        return False    
    
    def __str__(self):
        """Retorna uma representação em string da conta."""
        return f"""\
            Agência:\t{self.agencia}
            C/C:\t{self.numero}
            Titular:\t{self.cliente.nome}
        """

# Definição da classe Historico para registrar transações
class Historico:
    def __init__(self):
        """Inicializa o histórico com uma lista de transações."""
        self._transacoes = []

    @property
    def transacoes(self):
        """Retorna a lista de transações."""
        return self._transacoes

    def registrar_transacao(self, transacao):
        """Registra uma transação com tipo, valor e data."""
        self._transacoes.append({
            "tipo": transacao.__class__.__name__,
            "valor": transacao.valor,
            "data": datetime.now().strftime("%d/%m/%Y" + "\t" + "%H:%M:%S")
        })

# Definição da classe abstrata Transacao
class Transacao(ABC):
    @property
    @abstractmethod
    def valor(self):
        """Propriedade abstrata para obter o valor da transação."""
        pass
   
    @abstractmethod
    def registrar(self, conta):
        """Método abstrato para registrar a transação."""
        pass

# Definição da classe Saque que herda de Transacao
class Saque(Transacao):
    def __init__(self, valor):
        """Inicializa o saque com um valor."""
        self._valor = valor

    @property
    def valor(self):
        """Retorna o valor do saque."""
        return self._valor

    def registrar(self, conta):
        """Registra o saque em uma conta."""
        sucesso_transacao = conta.sacar(self.valor)

        if sucesso_transacao:
            conta.historico.registrar_transacao(self)

# Definição da classe Deposito que herda de Transacao
class Deposito(Transacao):
    def __init__(self, valor):
        """Inicializa o depósito com um valor."""
        self._valor = valor

    @property
    def valor(self):
        """Retorna o valor do depósito."""
        return self._valor

    def registrar(self, conta):
        """Registra o depósito em uma conta."""
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

# Função para recuperar a conta de um cliente
def recuperar_conta_cliente(cliente):
    if not cliente._contas:
        print("\n@@@ O cliente não possui conta! @@@")
        return None
    # FIXME: Não permite cliente escolher a conta
    return cliente._contas[0]

# Função para realizar um depósito
def depositar(clientes):
    cpf = input("Digite o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n@@@ Cliente não encontrado! @@@")
        return
    
    valor = float(input("Digite o valor do depósito: "))
    transacao = Deposito(valor)

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    cliente.realizar_transacao(conta, transacao)

# Função para realizar um saque
def sacar(clientes):
    cpf = input("Digite o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n@@@ Cliente não encontrado! @@@")
        return

    valor = float(input("Digite o valor do saque: "))
    transacao = Saque(valor)

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    cliente.realizar_transacao(conta, transacao)

# Função para exibir o extrato da conta de um cliente
def exibir_extrato(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n@@@ Cliente não encontrado! @@@")
        return
        
    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return
    
    print("\n============ EXTRATO ============")
    transacoes = conta.historico.transacoes

    extrato = ""
    if not transacoes:
        extrato = "Nenhuma transação realizada."
    else:
        for transacao in transacoes:
            extrato += f"\n{transacao['data']} - {transacao['tipo']}:\tR$ {transacao['valor']:.2f}"

    print(extrato)
    print(f"\nSaldo:\tR$ {conta.saldo:.2f}")
    print("=================================")

# Função para criar um novo cliente
def criar_cliente(clientes):
    cpf = input("Informe o CPF (somente número): ")
    cliente = filtrar_cliente(cpf, clientes)

    if cliente:
        print("\n@@@ Já existe cliente com esse CPF! @@@")
        return
    
    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (DD/MM/AAAA): ")
    endereco = input("Informe o endereço (logradouro, Nro - bairro - cidade/sigla estado): ")

    cliente = PessoaFisica(nome, data_nascimento, cpf, endereco)

    clientes.append(cliente)

    print("\n=== Cliente criado com Sucesso! ===")

# Função para criar uma nova conta
def criar_conta(numero, clientes, contas):
    cpf = input("Digite o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n@@@ Cliente não encontrado, fluxo de criação de conta encerrado! @@@")
        return

    conta = ContaCorrente.nova_conta(numero, cliente)
    contas.append(conta)
    cliente.adicionar_conta(conta)

    print("\n=== Conta Corrente criada com Sucesso! ===")

# Função para listar todas as contas
def listar_contas(contas):
    for conta in contas:
        print("=" * 55)
        print(textwrap.dedent(str(conta)))

# Função principal
def main():
    clientes = []
    contas = []

    while True:
        opcao = menu()

        if opcao == "1":
            depositar(clientes)

        elif opcao == "2":
            sacar(clientes)

        elif opcao == "3":
            exibir_extrato(clientes)

        elif opcao == "4":
            criar_cliente(clientes)

        elif opcao == "5":
            numero_conta = len(contas) + 1
            criar_conta(numero_conta, clientes, contas)

        elif opcao == "6":
            listar_contas(contas)

        elif opcao.lower() == "q":
            break
        else:
            print("Opção inválida!")

# Execução do sistema bancário
if __name__ == "__main__":
    main()
