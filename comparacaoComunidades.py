

# pip install scikit-learn

from sklearn.metrics.cluster import adjusted_rand_score

def community_similarity(l1, l2):
    similarity = adjusted_rand_score(l1, l2)
    return similarity

# Exemplo de uso
l1 = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
l2 = [[2, 3, 4], [1, 5, 6], [7, 8, 9]]

similarity = community_similarity(l1, l2)
print(f"A similaridade entre as formações de comunidades é: {similarity}")

'''
Nesse exemplo, as listas l1 e l2 representam as formações de comunidades nos grafos. 
Cada sublista dentro das listas l1 e l2 representa uma comunidade separada. 
O resultado do ARI será um valor entre -1 e 1, em que 1 indica uma similaridade perfeita, 
0 indica uma similaridade aleatória e -1 indica uma dissimilaridade perfeita.
'''



