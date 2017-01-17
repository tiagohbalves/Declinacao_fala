import math


# função para detectar os valores nan de um vetor retorna a primeira
# posição que não é
def detect_nan(vector):

    n = len(vector)

    for i in range(0, n):
        if not math.isnan(vector[i]):
            return i
