# Define o menu do sistema bancário
menu = '''
♦️ Sistema Bancário ♦️
----🥇 MENU 🥇----

[d] Depositar
[s] Sacar
[e] Extrato
[c] Consultar saldo
[q] Sair

----------------

👉  '''

# Inicializa as variáveis
saldo = 0.0  # Saldo inicial é 0.0
limite = 1000.0  # Limite para saque por transação
extrato = []  # Lista para armazenar as transações
numero_saques = 0  # Contador de saques realizados
numero_deposito = 0  # Contador de depósitos realizados
LIMITE_SAQUE = 3  # Limite de saques diários

# Inicia o loop do sistema bancário
while True:
    # Mostra o menu e captura a opção do usuário
    opcao = input(menu).strip().lower()

    if opcao == "d":
        # Depositar
        try:
            # Solicita o valor do depósito e converte para float
            deposito = float(input("Digite o valor do depósito: "))
            if deposito > 0:
                saldo += deposito  # Adiciona o valor ao saldo
                extrato.append(f"Depósito: +R${deposito:.2f}")  # Adiciona a transação ao extrato
                numero_deposito += 1  # Incrementa o contador de depósitos
                print(f"Depósito de R${deposito:.2f} realizado com sucesso.")
            else:
                print("O valor do depósito deve ser positivo.")
        except ValueError:
            print("Entrada inválida. Por favor, insira um valor numérico.")

    elif opcao == "s":
        # Sacar
        if numero_saques < LIMITE_SAQUE:
            try:
                # Solicita o valor do saque e converte para float
                saque = float(input("Digite o valor do saque: "))
                if saque > 0:
                    if saque <= saldo and saque <= limite:
                        saldo -= saque  # Subtrai o valor do saldo
                        extrato.append(f"Saque: -R${saque:.2f}")  # Adiciona a transação ao extrato
                        numero_saques += 1  # Incrementa o contador de saques
                        print(f"Saque de R${saque:.2f} realizado com sucesso.")
                    elif saque > limite:
                        print(f"\nO saque excede o limite de R${limite:.2f} por saque.\n")
                        print(f"O valor da disponivel na conta é R${saldo}")
                    else:
                        print("Saldo insuficiente!")
                else:
                    print("O valor do saque deve ser positivo.")
            except ValueError:
                print("Entrada inválida. Por favor, insira um valor numérico.")
        else:
            print(f"Você atingiu o limite diário de {LIMITE_SAQUE} saques.")

    elif opcao == "e":
        # Mostrar Extrato
        print("\n========Extrato:========")
        if extrato:
            for item in extrato:
                print(item)  # Imprime cada transação do extrato
        else:
            print("Nenhuma transação realizada.")
        print(f"Saldo atual: R${saldo:.2f}\n")  # Mostra o saldo atual   

    elif opcao == "c":
        # Consultar Saldo
        print(f"Saldo atual: R${saldo:.2f}")  # Mostra o saldo atual

    elif opcao == "q":
        # Sair
        print("Saindo do sistema. Até logo!")
        break  # Sai do loop e encerra o programa

    else:
        print("Opção inválida! Por favor, escolha uma opção válida do menu.")



