def inverte_peso(arq):
    l = []
    with open(arq, "r") as f:
        for line in f:
            l.append(line.strip().split(' '))

    for i in l:
        if len(i) < 2:
            break
        if i[2] == '1':
            i[2] = '13'
        elif i[2] == '2':
            i[2] = '12'
        elif i[2] == '3':
            i[2] = '11'
        elif i[2] == '4':
            i[2] = '10'
        elif i[2] == '5':
            i[2] = '9'
        elif i[2] == '6':
            i[2] = '8'
        elif i[2] == '7':
            i[2] = '7'
        elif i[2] == '8':
            i[2] = '6'
        elif i[2] == '9':
            i[2] = '5'
        elif i[2] == '10':
            i[2] = '4'
        elif i[2] == '11':
            i[2] = '3'
        elif i[2] == '12':
            i[2] = '2'
        elif i[2] == '13':
            i[2] = '1'

    with open(arq, "w") as f:
        for line in l:
            if len(line) > 2:
                f.write(f"{line[0]} {line[1]} {line[2]}\n")


def updateRelations(arq):
    l = []
    with open(arq, "r") as f:
        for line in f:
            l.append(line.strip().split(' '))

    for i in l:
        if len(i) < 2:
            break
        if i[2] == '6':
            i[2] = '7'
        elif i[2] == '7':
            i[2] = '8'
        elif i[2] == '8':
            i[2] = '9'
        elif i[2] == '9':
            i[2] = '10'
        elif i[2] == '10':
            i[2] = '12'
        elif i[2] == '11':
            i[2] = '13'

    with open(arq, "w") as f:
        for line in l:
            if len(line) > 2:
                f.write(f"{line[0]} {line[1]} {line[2]}\n")

g = updateRelations('eduardo-conections.txt')

