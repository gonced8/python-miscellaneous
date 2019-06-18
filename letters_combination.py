n
key = ['A']*26

while True:
    print(''.join(key))
    #input()

    if key[0]<'Z':
            key[0] = chr(ord(key[0])+1)
    else:
            flag = False
            for index in range(len(key)):
                    if key[index]!='Z':
                            flag = True
                            break
            if not flag:
                    print("Solution not found")
                    break

            key[index] = chr(ord(key[index])+1)
            key[:index] = ['A']*index
