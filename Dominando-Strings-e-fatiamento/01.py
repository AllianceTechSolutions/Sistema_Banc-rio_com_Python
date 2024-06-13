# Definimos uma variável chamada 'nome' e atribuímos a ela a string "tHiaGo".
nome = "tHiaGo"

# Converte a string 'nome' para maiúsculas e a imprime.
print(nome.upper())  # Output: THIAGO

# Converte a string 'nome' para minúsculas e a imprime.
print(nome.lower())  # Output: thiago

# Converte a primeira letra de cada palavra em 'nome' para maiúscula e as restantes para minúscula, e imprime.
print(nome.title())  # Output: Thiago

# Definimos uma variável chamada 'texto' e atribuímos a ela a string "   Olá mundo!   ", que contém espaços extras no início e no fim.
texto = "   Olá mundo!   "

# Imprime a string 'texto' seguida de um ponto. Os espaços extras são mantidos.
print(texto + ".")  # Output:    Olá mundo!   .

# Remove os espaços extras do início e do fim da string 'texto' e imprime a string resultante seguida de um ponto.
print(texto.strip() + ".")  # Output: Olá mundo!.

# Remove os espaços extras somente do final da string 'texto' e imprime a string resultante seguida de um ponto.
print(texto.rstrip() + ".")  # Output:    Olá mundo!.

# Remove os espaços extras somente do início da string 'texto' e imprime a string resultante seguida de um ponto.
print(texto.lstrip() + ".")  # Output: Olá mundo!   .

# Definimos uma variável chamada 'menu' e atribuímos a ela a string "Python".
menu = "Python"

# Imprime a string 'menu' com quatro sinais de hash (#) antes e depois.
print("####" + menu + "####")  # Output: ####Python####

# Centraliza a string 'menu' em um campo de largura 20, preenchendo os espaços ao redor com espaços em branco, e a imprime.
print(menu.center(20))  # Output: '       Python       '

# Centraliza a string 'menu' em um campo de largura 20, preenchendo os espaços ao redor com o caractere hash (#), e a imprime.
print(menu.center(20, "#"))  # Output: #######Python#######

# Insere o caractere "-" entre cada letra da string 'menu' e a imprime.
print("-".join(menu))  # Output: P-y-t-h-o-n
