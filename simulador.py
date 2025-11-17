import time
import os
import random

from estados import *
from imagem_to_tabuleiro import converte_imagem_para_tabuleiro

PROB_ESPALHAR = 0.6
VENTO = (1, 0)
BONUS_VENTO = 0.25


REGRA_VIZINHOS = [
    (-1, -1), (-1, 0), (-1, 1),
    (0, -1),          (0, 1),
    (1, -1),  (1, 0),  (1, 1)
]


def limpar_tela():
    os.system("cls" if os.name == "nt" else "clear")


def pausa(seg=0.2):
    time.sleep(seg)


def influencia_do_vento(linha, coluna, viz_linha, viz_coluna):
    dx = viz_linha - linha
    dy = viz_coluna - coluna
    return (dx, dy) == VENTO


def desenha_tabuleiro(tab):
    for linha in tab:
        print(" ".join(MAPA_CORES[cell] for cell in linha))


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


def avanca_geracao(tab):
    L = len(tab)
    C = len(tab[0])

    novo = [[tab[i][j] for j in range(C)] for i in range(L)]

    for l in range(L):
        for c in range(C):
            estado = tab[l][c]

            if estado in NAO_INFLAMAVEIS:
                continue

            if estado == QUEIMANDO:
                novo[l][c] = QUEIMADO
                continue

            if estado == QUEIMADO:
                novo[l][c] = VAZIO
                continue

            if estado in INFLAMAVEIS:
                viz = calcula_vizinhos_em_chamas(tab, l, c)

                if viz > 0:
                    prob = PROB_ESPALHAR

                    for dl, dc in REGRA_VIZINHOS:
                        nl, nc = l + dl, c + dc
                        if (
                            0 <= nl < L
                            and 0 <= nc < C
                            and tab[nl][nc] == QUEIMANDO
                            and influencia_do_vento(l, c, nl, nc)
                        ):
                            prob += BONUS_VENTO

                    if random.random() < prob:
                        novo[l][c] = QUEIMANDO

    return novo


if __name__ == "__main__":
    caminho = "mapas/forest.png"

    print("💡 Carregando mapa:", caminho)
    tabuleiro = converte_imagem_para_tabuleiro(caminho, bloco=20)

    while True:
        limpar_tela()
        desenha_tabuleiro(tabuleiro)
        pausa(0.5)
        tabuleiro = avanca_geracao(tabuleiro)
