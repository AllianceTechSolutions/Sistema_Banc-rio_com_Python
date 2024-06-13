opcao = int(input("Informe uma opção: [1]sacar \n[2] Extrato:"))

if opcao == 1:
    valor = float(input("Informe o valor a ser sacado:"))
    print("Saque realizado com sucesso!")

elif opcao == 2:
    print("Extrato")


else:
    sys.exit("Opção inválida!")


 #if conta_normal:
 #       if saldo >= saque:
 #           print("Saque realizado com sucesso!") 
 #       elif saque <= (saldo + cheque_especial):
 #           print("Saque realizado com uso do cheque especial!")
 #elif conta_universitaria:
 #    if saldo >= saque:
 #       print("Saque realizado com sucesso!")
 #    else:
 #       print("Saldo insuficiente!") 



    


