
def community_similarity(l1, l2):
    totalElementos = 0
    similaridade = 0
    for lista1 in l1:
        taml1 = len(lista1)
        totalElementos += taml1

        setl1 = set(lista1)
        maiorSemelhanca = 0
        for lista2 in l2:
            setl2 = set(lista2)
            common = setl1.intersection(setl2)
            if len(common) > maiorSemelhanca:
                maiorSemelhanca = len(common)

        similaridade += maiorSemelhanca

    return similaridade/totalElementos

# Exemplo de uso
l1 = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
l2 = [[2, 3, 4], [1, 5, 6], [7, 8, 9]]

similarity = community_similarity(l1, l2)
print(f"A similaridade entre as formações de comunidades é: {similarity}")

'''
Nesse exemplo, as listas l1 e l2 representam as formações de comunidades nos grafos. 
Cada sublista dentro das listas l1 e l2 representa uma comunidade separada. 
O resultado do será um valor entre 0 e 1, em que 1 indica uma similaridade perfeita, 
e 0 indica a ausência de similaridade.
'''
