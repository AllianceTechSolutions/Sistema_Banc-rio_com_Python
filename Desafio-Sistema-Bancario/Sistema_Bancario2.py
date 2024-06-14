import textwrap  # Importa o módulo textwrap, que será usado para remover a indentação do texto.

# Função para exibir o menu
def menu():
    menu_texto = '''\n
   ♦️  Sistema Bancário  ♦️ 

    -----🥇 MENU 🥇-----

    [d]\tDepositar
    [s]\tSacar
    [e]\tExtrato
    [nc]\tNova conta
    [lc]\tListar contas
    [nu]\tNovo usuário
    [q]\tSair

    ---------------------

    👉  '''
    # Exibe o menu com as opções e retorna a entrada do usuário
    return input(textwrap.dedent(menu_texto))

# Função para depositar dinheiro
def depositar(saldo, valor, extrato, /):
    # Verifica se o valor a ser depositado é maior que zero
    if valor > 0:
        # Adiciona o valor ao saldo
        saldo += valor
        # Adiciona a transação ao extrato
        extrato += f"Depósito: +R${valor:.2f}\n"
        print("\n=== Depósito realizado com sucesso!🤑 ===")
    else:
        # Caso o valor seja inválido (não positivo), exibe uma mensagem de erro
        print("\n@@@ Operação falhou! O valor informado é inválido. @@@")

    # Retorna o saldo atualizado e o extrato
    return saldo, extrato

# Função para sacar dinheiro
def sacar(*, saldo, valor, extrato, limite, numero_saques, limite_saques):
    # Verifica se o valor do saque excede o saldo
    excedeu_saldo = valor > saldo
    # Verifica se o valor do saque excede o limite
    excedeu_limite = valor > limite
    # Verifica se o número de saques excede o limite diário
    excedeu_saques = numero_saques >= limite_saques

    if excedeu_saldo:
        print("\n@@@ Operação falhou! Saldo insuficiente. @@@")
    elif excedeu_limite:
        print("\n@@@ Operação falhou! O valor do saque excede o limite. @@@")
    elif excedeu_saques:
        print("\n@@@ Operação falhou! O número de saques excede o limite. @@@")
    elif valor > 0:
        # Deduz o valor do saque do saldo
        saldo -= valor
        # Adiciona a transação ao extrato
        extrato += f"Saque: -R${valor:.2f}\n"
        # Incrementa o número de saques realizados
        numero_saques += 1
        print("\n=== Saque realizado com sucesso! ===")
    else:
        print("\n@@@ Operação falhou! O valor informado é inválido. @@@")

    # Retorna o saldo atualizado, o extrato e o número de saques
    return saldo, extrato, numero_saques

# Função para exibir o extrato
def exibir_extrato(saldo, /, *, extrato):
    print("\n========== Extrato ==========\n")
    # Exibe uma mensagem caso não haja movimentações, ou o extrato das transações
    print("Não foram realizadas movimentações." if not extrato else extrato)
    # Exibe o saldo atual
    print(f"Saldo atual: R${saldo : .2f}\n")
    print("=============================")

# Função para criar um novo usuário
def criar_usuario(usuarios):
    cpf = input('Informe o CPF (somente número): ')
    # Verifica se o usuário já existe na lista de usuários
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        print("\n@@@ Operação falhou! O usuário já existe. @@@")
        return
    
    # Coleta as informações do novo usuário
    nome = input('Informe o nome completo: ')
    data_nascimento = input('Informe a data de nascimento (dd/mm/aaaa): ')
    endereco = input('Informe o endereço (logradouro, Nro - bairro - cidade/sigla estado): ')

    # Adiciona o novo usuário à lista de usuários
    usuarios.append({
        'nome': nome,
        'data_nascimento': data_nascimento,
        'cpf': cpf,
        'endereco': endereco,
    })
    print("\n=== Usuário criado com sucesso! ===")

# Função para filtrar usuário pelo CPF
def filtrar_usuario(cpf, usuarios):
    # Filtra a lista de usuários para encontrar um usuário com o CPF fornecido
    usuarios_filtrados = [usuario for usuario in usuarios if usuario['cpf'] == cpf]
    # Retorna o primeiro usuário encontrado, ou None se não houver correspondência
    return usuarios_filtrados[0] if usuarios_filtrados else None

# Função para criar uma nova conta
def criar_conta(agencia, numero_conta, usuarios):
    cpf = input('Informe o CPF do usuário: ')
    # Verifica se o usuário com o CPF fornecido existe na lista de usuários
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        print("\n=== Conta criada com sucesso! ===\n")
        # Retorna um dicionário com os dados da conta criada
        return {
            'agencia': agencia,
            'numero_conta': numero_conta,
            'usuario': usuario,
        }
    print("\n@@@ Operação falhou! Usuário não encontrado. @@@")

# Função para listar todas as contas
def listar_contas(contas):
    for conta in contas:
        # Formata os detalhes da conta para exibição
        linha = f"""\
        Agência:\t{conta['agencia']}
        C/C:\t\t{conta['numero_conta']}
        Titular:\t{conta['usuario']['nome']}
        Endereço:\t{conta['usuario']['endereco']}
        """
        print('=' * 50)
        print(textwrap.dedent(linha))

# Função principal para controlar o fluxo do sistema
def main():
    LIMITE_SAQUE = 3  # Limite diário de saques
    AGENCIA = '0001'  # Número da agência bancária

    saldo = 0  # Saldo inicial
    limite = 500  # Limite de saque
    extrato = ""  # Extrato inicial
    numero_saques = 0  # Contador de saques
    usuarios = []  # Lista de usuários
    contas = []  # Lista de contas
    numero_conta = 1  # Contador para número de contas

    while True:
        # Exibe o menu e coleta a opção selecionada
        opcao = menu()

        if opcao == 'd':
            # Depositar
            try:
                # Coleta o valor a ser depositado
                valor = float(input('\nInforme o valor do depósito:💰 '))
                # Chama a função de depósito
                saldo, extrato = depositar(saldo, valor, extrato)
            except ValueError:
                print("\n@@@ Entrada inválida! Por favor, insira um valor numérico. @@@")

        elif opcao == 's':
            # Sacar
            try:
                # Coleta o valor a ser sacado
                valor = float(input('\nInforme o valor do saque:💸 '))
                # Chama a função de saque
                saldo, extrato, numero_saques = sacar(
                    saldo=saldo,
                    valor=valor,
                    extrato=extrato,
                    limite=limite,
                    numero_saques=numero_saques,
                    limite_saques=LIMITE_SAQUE
                )
            except ValueError:
                print("\n@@@ Entrada inválida! Por favor, insira um valor numérico. @@@")

        elif opcao == 'e':
            # Mostrar Extrato
            # Chama a função de exibição de extrato
            exibir_extrato(saldo, extrato=extrato)

        elif opcao == 'nu':
            # Criar Usuário
            # Chama a função de criação de usuário
            criar_usuario(usuarios)

        elif opcao == 'nc':
            # Criar Conta
            # Chama a função de criação de conta
            conta = criar_conta(AGENCIA, numero_conta, usuarios)
            if conta:
                # Adiciona a nova conta à lista de contas e incrementa o número de contas
                contas.append(conta)
                numero_conta += 1

        elif opcao == 'lc':
            # Listar Contas
            # Chama a função de listagem de contas
            listar_contas(contas)

        elif opcao == 'q':
            # Sair
            print("\nSaindo do sistema. Até logo!👋\n")
            break

        else:
            print('Opção inválida, por favor selecione novamente a operação desejada.')

# Executa o programa se o script for executado diretamente
if __name__ == "__main__":
    main()


