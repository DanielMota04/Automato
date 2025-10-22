import time
import os
class Cores:
    VERDE = '\033[92m'
    CINZA = '\033[90m'
    RESET = '\033[0m'

def tabuleiro():
    return [
        [0, 0, 0, 0, 0],
        [0, 0, 1, 0, 0],
        [0, 0, 1, 0, 0],
        [0, 0, 1, 0, 0],
        [0, 0, 0, 0, 0],
    ]

def desenha(m):

    formas = {
        0: Cores.CINZA + '.' + Cores.RESET,
        1: Cores.VERDE + '■' + Cores.RESET
    }
    
    for i in range(len(m)):
        print(' '.join([formas[e] for e in m[i]]))

def conta_vizinhos_vivos(m, i, y):
    regra_vizinhos = [
        (-1, -1),(-1,0), (-1, 1), 
        (0, -1), (0, 1),
        (1, -1), (1, 0), (1, 1)
        ]
    coordenadas_vizinhos_tabuleiro = [(i+dcv[0], y+dcv[1]) for dcv in regra_vizinhos if 0 <= i+dcv[0] < len(m) and 0 <= y+dcv[1] < len(m[0])]
    return len([1 for cv in coordenadas_vizinhos_tabuleiro if m[cv[0]][cv[1]] ==1])  
     

def atualiza(m):
    novo_formato = [[0 for e in linha] for linha in m]
    for i in range(len(m)):
        for y in range(len(m[i])):
            vizinhos_vivos = conta_vizinhos_vivos(m, i, y)
            if m[i][y] == 1:
                if vizinhos_vivos in {0, 1}:
                    novo_formato[i][y] = 0
                elif vizinhos_vivos >= 4:
                    novo_formato[i][y] = 0
                else:
                    novo_formato[i][y] = 1
            else:
                if vizinhos_vivos == 3:
                    novo_formato[i][y] = 1
                else:
                    novo_formato[i][y] = 0
    return novo_formato

def pausa():
    time.sleep(0.5) 

m = tabuleiro()

while True:
    os.system("clear") 
    desenha(m)
    pausa()
    m = atualiza(m)