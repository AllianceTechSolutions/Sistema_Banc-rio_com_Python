# Definimos a variável 'nome' e atribuímos a ela a string "Thiago ABC".
nome = "Thiago ABC"

# Definimos a variável 'idade' e atribuímos a ela o valor inteiro 34.
idade = 34

# Definimos a variável 'profissao' e atribuímos a ela a string "Programador".
profissao = "Programador"

# Definimos a variável 'linguagem' e atribuímos a ela a string "Python & JavaScript".
linguagem = "Python & JavaScript"

# Definimos a variável 'saldo' e atribuímos a ela o valor de ponto flutuante 2600.30.
saldo = 2600.30

# Definimos um dicionário 'dados' contendo várias informações associadas a suas respectivas chaves.
dados = {
    "nome": "Thiago ABC", 
    "idade": 34, 
    "profissao": "Programador", 
    "linguagem": "Python & JavaScript", 
    "saldo": 2600.30
}

# Imprime o dicionário 'dados' que contém todas as informações definidas anteriormente.
print(dados)
# Output: {'nome': 'Thiago ABC', 'idade': 34, 'profissao': 'Programador', 'linguagem': 'Python & JavaScript', 'saldo': 2600.30}

# Usando a formatação de strings estilo C, insere os valores de 'nome' e 'idade' na string e imprime.
print("Nome: %s Idade: %s" % (nome, idade))
# Output: Nome: Thiago ABC Idade: 34

# Usando o método '.format()', insere os valores de 'nome' e 'idade' na string e imprime.
print("Nome: {} Idade: {}".format(nome, idade))
# Output: Nome: Thiago ABC Idade: 34

# Usando o método '.format()' com indexação, insere os valores de 'nome' e 'idade' na string e imprime.
print("Nome: {0} Idade: {1}".format(nome, idade))
# Output: Nome: Thiago ABC Idade: 34

# Usando o método '.format()' com nomeação de argumentos, insere os valores de 'nome' e 'idade' na string e imprime.
print("Nome: {nome} Idade: {idade}".format(nome=nome, idade=idade))
# Output: Nome: Thiago ABC Idade: 34

# Usando o método '.format()' com o operador de expansão (**), insere os valores de 'dados' na string e imprime.
print("Nome: {nome} Idade: {idade}".format(**dados))
# Output: Nome: Thiago ABC Idade: 34

# Usando f-strings (strings formatadas), insere os valores de 'nome', 'idade', 'profissao' e 'linguagem' na string e imprime.
print(f"Nome: {nome} Idade: {idade} Profissão: {profissao} Linguagem: {linguagem}")
# Output: Nome: Thiago ABC Idade: 34 Profissão: Programador Linguagem: Python & JavaScript

# Usando f-strings, insere os valores de 'nome', 'idade' e 'saldo' na string, formatando 'saldo' para 2 casas decimais, e imprime.
print(f"Nome: {nome} Idade: {idade} Saldo: {saldo:0.2f}")
# Output: Nome: Thiago ABC Idade: 34 Saldo: 2600.30

# Usando f-strings, insere os valores de 'nome', 'idade' e 'saldo' na string, formatando 'saldo' para 10 caracteres de largura e 2 casas decimais, e imprime.
print(f"Nome: {nome} Idade: {idade} Saldo: {saldo:10.2f}")
# Output: Nome: Thiago ABC Idade: 34 Saldo:    2600.30


