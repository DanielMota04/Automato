import cv2
import numpy as np
from estados import *

def classificar_bloco(bloco_hsv):

    H = bloco_hsv[:, :, 0]
    S = bloco_hsv[:, :, 1]
    V = bloco_hsv[:, :, 2]

    # ---------- DETECÇÃO DE FOGO ----------
    mascara_fogo_1 = (H <= 10) & (S > 80) & (V > 80)
    mascara_fogo_2 = (H >= 160) & (H <= 179) & (S > 80) & (V > 80)

    num_fogo = np.sum(mascara_fogo_1 | mascara_fogo_2)

    # se mais de 1% do bloco for fogo → marcar como QUEIMANDO
    if num_fogo > (bloco_hsv.size * 0.01):
        return QUEIMANDO

    # --------- MÉDIAS PARA OUTROS ELEMENTOS ----------
    h_mean = np.mean(H)
    s_mean = np.mean(S)
    v_mean = np.mean(V)

    # Água
    if 90 <= h_mean <= 140 and s_mean > 50:
        return AGUA

    # Vegetação
    if 35 <= h_mean <= 85:
        if s_mean > 60 and v_mean < 150:
            return ARVORE  # verde escuro
        else:
            return ARBUSTO  # verde claro

    # Pedra
    if s_mean < 30 and v_mean > 160:
        return PEDRA

    # Solo / vazio
    return VAZIO




def converte_imagem_para_tabuleiro(caminho_imagem, bloco=20):
    img = cv2.imread(caminho_imagem)

    if img is None:
        raise ValueError("Erro: imagem não encontrada.")

    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    h, w = hsv.shape[:2]

    linhas = h // bloco
    colunas = w // bloco

    tabuleiro = []

    for i in range(linhas):
        linha = []
        for j in range(colunas):
            y0 = i * bloco
            x0 = j * bloco

            bloco_hsv = hsv[y0:y0+bloco, x0:x0+bloco]

            estado = classificar_bloco(bloco_hsv)
            linha.append(estado)

        tabuleiro.append(linha)

    return tabuleiro
