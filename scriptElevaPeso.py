

arq = 'guilherme-conections-invertido.txt'

l = []
with open(arq, "r") as f:
    for line in f:
        l.append(line.strip().split(' '))

nome = arq.split(".")
with open(nome[0] + '_eleva.' + nome[1], "w") as f:
    for i in l:
        if len(i) < 2:
            break
        f.write(f"{i[0]} {i[1]} {str(int(i[2])**2)}\n")

