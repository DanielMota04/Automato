import random
import matplotlib.pyplot as plt
from estados import *
from imagem_to_tabuleiro import converte_imagem_para_tabuleiro

PROB_ESPALHAR = 0.6
VENTO = (0, 1) 
BONUS_VENTO = 0.3

REGRA_VIZINHOS = [
    (-1, -1), (-1, 0), (-1, 1),
    (0, -1),          (0, 1),
    (1, -1),  (1, 0),  (1, 1)
]

CORES_MPL = {
    AGUA: (0, 0, 1),  
    VEGETACAO: (0, 1, 0),
    QUEIMANDO: (1, 0, 0),  
    QUEIMADO: (0.3, 0.3, 0.3)
}

def desenha_tabuleiro_grafico(tab):
    img = [[CORES_MPL[cell] for cell in linha] for linha in tab]
    plt.imshow(img)
    plt.axis('off')
    plt.draw()
    plt.pause(0.3)


def calcula_vizinhos_em_chamas(tab, l, c):
    total = 0
    L = len(tab)
    C = len(tab[0])

    for dl, dc in REGRA_VIZINHOS:
        nl, nc = l + dl, c + dc
        if 0 <= nl < L and 0 <= nc < C:
            if tab[nl][nc] == QUEIMANDO:
                total += 1

    return total


def influencia_do_vento(l, c, nl, nc):
    dx = nl - l
    dy = nc - c
    return (dx, dy) == VENTO


def avanca_geracao(tab):
    L = len(tab)
    C = len(tab[0])

    novo = [[tab[i][j] for j in range(C)] for i in range(L)]

    for l in range(L):
        for c in range(C):
            estado = tab[l][c]

            if estado == AGUA:
                continue

            if estado == QUEIMANDO:
                novo[l][c] = QUEIMADO
                continue

            if estado == QUEIMADO:
                continue

            if estado == VEGETACAO:
                viz = calcula_vizinhos_em_chamas(tab, l, c)

                if viz > 0:
                    prob = PROB_ESPALHAR

                    for dl, dc in REGRA_VIZINHOS:
                        nl, nc = l+dl, c+dc
                        if (
                            0 <= nl < L and 0 <= nc < C and 
                            tab[nl][nc] == QUEIMANDO and 
                            influencia_do_vento(l, c, nl, nc)
                        ):
                            prob += BONUS_VENTO

                    if random.random() < prob:
                        novo[l][c] = QUEIMANDO

    return novo


if __name__ == "__main__":
    caminho = "mapas/forest.png"
    # caminho = "mapas/forest1.jpg"

    tabuleiro = converte_imagem_para_tabuleiro(caminho, bloco=5)

    plt.ion()
    while True:
        plt.clf()
        desenha_tabuleiro_grafico(tabuleiro)
        tabuleiro = avanca_geracao(tabuleiro)
