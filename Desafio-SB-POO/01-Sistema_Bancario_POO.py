# Importação de Módulos Necessários
from abc import ABC, abstractmethod
from datetime import datetime
import textwrap

class ContasIterador:
    def __init__(self, contas):
        self._contas = contas
        self._index = 0

    def __iter__(self):
        return self
    
    def __next__(self):
        try:
            conta = self._contas[self._index]
            return f"""\
            Agência:\t{conta.agencia}
            Número:\t\t{conta.numero}
            Titular:\t{conta.cliente.nome}
            Saldo:\t\tR$ {conta.saldo:.2f}
        """
        except IndexError:
            raise StopIteration
        finally:
            self._index += 1

# Definição da classe Cliente
class Cliente:
    def __init__(self, endereco):
        """Inicializa o Cliente com endereço e lista de contas."""
        self._endereco = endereco
        self._contas = []

    def realizar_transacao(self, conta, transacao):
        """Realiza uma transação na conta especificada se os limites diários não forem excedidos."""
        tipo_transacao = transacao.__class__.__name__

        if tipo_transacao == 'Deposito' and conta.historico.numero_depositos_do_dia() >= 3:
            print("\n@@@ Operação falhou! O limite diário de depósitos foi atingido. @@@")
            return

        if tipo_transacao == 'Saque' and conta.historico.numero_saques_do_dia() >= 3:
            print("\n@@@ Operação falhou! O limite diário de saques foi atingido. @@@")
            return

        transacao.registrar(conta)

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
    _numero_sequencial = 1  # Contador estático para gerar número de conta único

    def __init__(self, cliente):
        """Inicializa a Conta com número gerado automaticamente, cliente, saldo e histórico."""
        self._saldo = 0
        self._numero = Conta._numero_sequencial
        Conta._numero_sequencial += 1
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()

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
            print("\n========= Depósito realizado com Sucesso! =========")

        else:
            print("\n@@@ Operação falhou! O valor do depósito deve ser positivo. @@@")
            return False
        
        return True
    
    def realizar_transacao(self, transacao):
        """Realiza uma transação e registra no histórico."""
        transacao.registrar(self)

# Definição da classe ContaCorrente que herda de Conta
class ContaCorrente(Conta):
    def __init__(self, cliente, limite=500):
        """Inicializa a Conta Corrente com limite de saque e limite de valor."""
        super().__init__(cliente)
        self._limite = limite

    def sacar(self, valor):
        """Realiza um saque, respeitando limites de valor e quantidade de saques."""
        excedeu_limite = valor > self._limite

        if excedeu_limite:
            print("\n@@@ Operação falhou! O valor do saque excede o limite. @@@")
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
    
    def adicionar_transacao(self, transacao):
        """Adiciona uma transação ao histórico."""
        self._transacoes.append({
            "tipo": transacao.__class__.__name__,
            "valor": transacao.valor,
            "data": datetime.now().strftime("%d/%m/%Y" + "\t" + "%H:%M:%S")
        })

    def gerar_relatorio(self):
        """Gera um relatório de transações com data, tipo e valor."""
        print("\t** Relatório de Transações **\n")
        for transacao in self._transacoes:    # Itera sobre cada transação no histórico
            yield transacao                   # Utiliza o yield para gerar transações uma a uma 

    def transacoes_do_dia(self):
        """Retorna as transações do dia atual."""
        data_atual = datetime.now().date()
        return [transacao for transacao in self._transacoes
                if datetime.strptime(transacao["data"], "%d/%m/%Y\t%H:%M:%S").date() == data_atual]

    def numero_saques_do_dia(self):
        """Conta o número de saques realizados no dia."""
        return len([transacao for transacao in self.transacoes_do_dia() if transacao["tipo"] == "Saque"])

    def numero_depositos_do_dia(self):
        """Conta o número de depósitos realizados no dia."""
        return len([transacao for transacao in self.transacoes_do_dia() if transacao["tipo"] == "Deposito"])

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

# Função para recuperar uma conta associada a um cliente
def recuperar_conta_cliente(cliente):
    if not cliente._contas:
        print("\n@@@ Cliente não possui conta! @@@")
        return
    
    # Retorna a primeira conta encontrada
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

            cliente.realizar_transacao(conta, transacao)

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

            cliente.realizar_transacao(conta, transacao)

        elif opcao == "3":
            cpf = input("Informe o CPF do cliente: ")
            cliente = filtrar_cliente(cpf, clientes)
            
            if not cliente:
                print("\n@@@ Cliente não encontrado! @@@")
                continue
            
            conta = recuperar_conta_cliente(cliente)
            if not conta:
                continue

            print("\n================== EXTRATO ===================")
            transacoes = conta.historico.gerar_relatorio()
            for transacao in transacoes:
                print(f"{transacao['data']} - {transacao['tipo']}: R$ {transacao['valor']:.2f}")
            print(f"\nSaldo Atual: R$ {conta.saldo:.2f}")
            print("==============================================")

        elif opcao == "4":
            cpf = input("Informe o CPF (somente números): ")
            cliente = filtrar_cliente(cpf, clientes)

            if cliente:
                print("\n@@@ Já existe cliente com esse CPF! @@@")
                continue

            nome = input("Informe o nome completo: ")
            data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
            endereco = input("Informe o endereço: ")

            cliente = PessoaFisica(nome=nome, data_nascimento=data_nascimento, cpf=cpf, endereco=endereco)
            clientes.append(cliente)

            print("\n=== Cliente criado com sucesso! ===")

        elif opcao == "5":
            cpf = input("Informe o CPF do cliente: ")
            cliente = filtrar_cliente(cpf, clientes)
            
            if not cliente:
                print("\n@@@ Cliente não encontrado! @@@")
                continue

            conta = ContaCorrente(cliente=cliente)
            cliente.adicionar_conta(conta)
            contas.append(conta)

            print("\n=== Conta criada com sucesso! ===")

        elif opcao == "6":
            if not contas:
                print("\n@@@ Não há contas cadastradas! @@@")
            
            for conta in ContasIterador(contas):
                print("=" * 100)
                print(textwrap.dedent(str(conta)))

        elif opcao == "q":
            break

        else:
            print("\n@@@ Opção inválida! @@@")

# Execução do sistema bancário
if __name__ == "__main__":
    main()
