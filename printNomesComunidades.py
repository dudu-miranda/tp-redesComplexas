
def printComunidades(l1, arq):
    pessoasArquivo = {}
    with open(arq, "r") as f:
        next(f)  # ignora a primeira linha
        for line in f:
            fields = line.strip().split('\t')
            if len(fields) >= 4:
                nome, apelido, cidade = fields[1], fields[2], fields[3]
                pessoasArquivo[fields[0]] = f"{fields[0]} - {nome}, {apelido}, {cidade}"

    i = 1
    for pessoas in l1:
        print(f"Comunidade {i}:")
        for pessoa in pessoas:
            print(pessoasArquivo[str(pessoa)])
        i += 1
        print("")


l1 = [[1], [243], [2,  3,  4,  5,  6,  7,  8,  9,  10,  11,  12,  13,  14,  15,  16,  17,  18,  19,  20,  21]]
arq = 'grafos/guilherme/guilherme.txt'
printComunidades(l1, arq)
