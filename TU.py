while True:
    tu=input("Tu: ")

    if len(tu)==0:
        continue

    i = tu.find("tu ")
    while i!=-1:
        tu = tu[i + 2:]
        i = tu.find("tu ")

    i = tu.find("Tu ")
    while i!=-1:
        tu = tu[i + 2:]
        i = tu.find("Tu ")

    i = tu.find("tU ")
    while i != -1:
        tu = tu[i + 2:]
        i = tu.find("tU ")

    i = tu.find("TU ")
    while i != -1:
        tu = tu[i + 2:]
        i = tu.find("TU ")

    if tu=="tu" or tu=="Tu" or tu=="TU":
        tu = ""

    if len(tu)>0:
        while(tu[0]==' '):
            tu=tu[1:]
            if len(tu)==0:
                break

    if len(tu)>0:
        check=tu[-1]
        while (check=="." or check=="?" or check=="!" or check==" "):
            tu=tu[:-1]
            if len(tu):
                check = tu[-1]
            else:
                check = ""

        if len(tu) > 0:
            goncalo = "Não, TU é que " + tu[0].lower() + tu[1:] + "!"

        else:
            goncalo = "Não, TU!"

    else:
        goncalo = "Não, TU!"

    print ("Gonçalo: ", goncalo, '\n')
