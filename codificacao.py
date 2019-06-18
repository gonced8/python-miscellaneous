str = input("Escreva a frase em maiúsclas\n")

alfabeto = [0]*257

for i in range (0, len(str)-1):
    codigo=ord(str[i])
    if alfabeto[codigo]==1:
        continue
    else:
        print(str[i])
        alfabeto[codigo]=1

        
    
