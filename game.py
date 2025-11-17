import time
import os
import random

VAZIO = 0
ARVORE = 1
QUEIMANDO = 2
QUEIMADO = 3

PROB_ESPALHAR = 0.6

VENTO = (0, 1)

BONUS_VENTO = 0.25

REGRA_VIZINHOS = [
    (-1, -1), (-1, 0), (-1, 1),
    (0, -1),          (0, 1),
    (1, -1),  (1, 0),  (1, 1)
]

class Cores:
    COR_VAZIO = '\033[90m■\033[0m'
    COR_ARVORE = '\033[92m■\033[0m'
    COR_QUEIMANDO = '\033[93m■\033[0m'
    COR_QUEIMADO = '\033[91m■\033[0m'
    
    
# def inicializa_tabuleiro():
#     return [
#         [ARVORE, ARVORE, ARVORE, ARVORE, ARVORE, ARVORE, ARVORE, ARVORE, ARVORE, ARVORE],
#         [ARVORE, ARVORE, ARVORE, ARVORE, ARVORE, ARVORE, ARVORE, ARVORE, ARVORE, ARVORE],
#         [ARVORE, ARVORE, ARVORE, ARVORE, ARVORE, ARVORE, ARVORE, ARVORE, ARVORE, ARVORE],
#         [ARVORE, ARVORE, ARVORE, ARVORE, ARVORE, ARVORE, ARVORE, ARVORE, ARVORE, ARVORE],
#         [ARVORE, ARVORE, ARVORE, ARVORE, ARVORE, ARVORE, ARVORE, ARVORE, ARVORE, ARVORE],
#         [ARVORE, ARVORE, ARVORE, ARVORE, ARVORE, ARVORE, ARVORE, ARVORE, ARVORE, ARVORE],
#         [ARVORE, ARVORE, ARVORE, ARVORE, ARVORE, ARVORE, ARVORE, ARVORE, ARVORE, ARVORE],
#         [ARVORE, ARVORE, ARVORE, ARVORE, ARVORE, ARVORE, ARVORE, ARVORE, ARVORE, ARVORE],
#         [ARVORE, ARVORE, ARVORE, ARVORE, ARVORE, ARVORE, ARVORE, ARVORE, ARVORE, ARVORE],
#         [ARVORE, ARVORE, ARVORE, ARVORE, ARVORE, ARVORE, ARVORE, ARVORE, ARVORE, ARVORE],
#     ]

def inicializa_tabuleiro():
    return [
        [ARVORE, ARVORE, VAZIO, ARVORE, ARVORE, ARVORE, ARVORE, ARVORE, ARVORE, ARVORE],
        [ARVORE, ARVORE, VAZIO, ARVORE, ARVORE, ARVORE, ARVORE, ARVORE, ARVORE, ARVORE],
        [ARVORE, ARVORE, VAZIO, ARVORE, ARVORE, ARVORE, ARVORE, ARVORE, ARVORE, ARVORE],
        [ARVORE, ARVORE, VAZIO, ARVORE, ARVORE, ARVORE, ARVORE, ARVORE, ARVORE, ARVORE],
        [ARVORE, ARVORE, VAZIO, ARVORE, ARVORE, ARVORE, ARVORE, ARVORE, ARVORE, ARVORE],
        [ARVORE, ARVORE, VAZIO, ARVORE, ARVORE, ARVORE, ARVORE, ARVORE, ARVORE, ARVORE],
        [ARVORE, ARVORE, VAZIO, ARVORE, ARVORE, QUEIMANDO, ARVORE, ARVORE, ARVORE, ARVORE],
        [ARVORE, ARVORE, VAZIO, ARVORE, ARVORE, ARVORE, ARVORE, ARVORE, ARVORE, ARVORE],
        [ARVORE, ARVORE, VAZIO, ARVORE, ARVORE, ARVORE, ARVORE, ARVORE, ARVORE, ARVORE],
        [ARVORE, ARVORE, VAZIO, ARVORE, ARVORE, ARVORE, ARVORE, ARVORE, ARVORE, ARVORE],
    ]

def desenha_tabuleiro(tabuleiro):
    simbolos = {
        VAZIO: Cores.COR_VAZIO,
        ARVORE: Cores.COR_ARVORE,
        QUEIMANDO: Cores.COR_QUEIMANDO,
        QUEIMADO: Cores.COR_QUEIMADO
    }
    
    for linha in tabuleiro:
        linha_simbolos = [simbolos[estado] for estado in linha]
        print(' '.join(linha_simbolos))


def calcula_vizinhos_em_chamas(tabuleiro, linha, coluna):
    total_vizinhos_em_chamas = 0
    num_linhas = len(tabuleiro)
    num_colunas = len(tabuleiro[0])
    
    for deslocamento in REGRA_VIZINHOS:
        desloc_linha, desloc_coluna = deslocamento
        
        vizinho_linha = linha + desloc_linha
        vizinho_coluna = coluna + desloc_coluna
        
        esta_no_tabuleiro = (
            0 <= vizinho_linha < num_linhas and
            0 <= vizinho_coluna < num_colunas
        )
        
        if esta_no_tabuleiro:
            if tabuleiro[vizinho_linha][vizinho_coluna] == QUEIMANDO:
                total_vizinhos_em_chamas += 1
                
    return total_vizinhos_em_chamas


def influencia_do_vento(linha, coluna, viz_linha, viz_coluna):
    dx = viz_linha - linha
    dy = viz_coluna - coluna
    return (dx, dy) == VENTO


def avanca_geracao(tabuleiro_atual):
    num_linhas = len(tabuleiro_atual)
    num_colunas = len(tabuleiro_atual[0])
    
    proximo_tabuleiro = [[VAZIO for _ in range(num_colunas)] for _ in range(num_linhas)]
    
    for linha in range(num_linhas):
        for coluna in range(num_colunas):
            
            estado_atual = tabuleiro_atual[linha][coluna]
            vizinhos_queimando = calcula_vizinhos_em_chamas(tabuleiro_atual, linha, coluna)
                        
            if estado_atual == QUEIMANDO:
                proximo_tabuleiro[linha][coluna] = QUEIMADO
            
            elif estado_atual == QUEIMADO:
                proximo_tabuleiro[linha][coluna] = VAZIO
                
            elif estado_atual == ARVORE:
                if vizinhos_queimando > 0:
                    prob = PROB_ESPALHAR
                    for d_linha, d_coluna in REGRA_VIZINHOS:
                        viz_linha = linha + d_linha
                        viz_coluna = coluna + d_coluna

                        if (
                            0 <= viz_linha < num_linhas and
                            0 <= viz_coluna < num_colunas and
                            tabuleiro_atual[viz_linha][viz_coluna] == QUEIMANDO and
                            influencia_do_vento(linha, coluna, viz_linha, viz_coluna)
                        ):
                            prob += BONUS_VENTO

                    if random.random() < prob:
                        proximo_tabuleiro[linha][coluna] = QUEIMANDO
                    else:
                        proximo_tabuleiro[linha][coluna] = ARVORE

                else:
                    proximo_tabuleiro[linha][coluna] = ARVORE
                
    return proximo_tabuleiro


def pausa(segundos=0.5):
    time.sleep(segundos) 

def limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear') 


if __name__ == "__main__":
    
    tabuleiro_atual = inicializa_tabuleiro()

    while True:
        limpar_tela() 
        desenha_tabuleiro(tabuleiro_atual)
        pausa(0.5)
        
        tabuleiro_atual = avanca_geracao(tabuleiro_atual)