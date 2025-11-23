import cv2
import numpy as np
from estados import *


def classificar_bloco(bloco_hsv):
    H = bloco_hsv[:, :, 0]
    S = bloco_hsv[:, :, 1]
    V = bloco_hsv[:, :, 2]

    h_mean, s_mean, v_mean = np.mean(H), np.mean(S), np.mean(V)

    mascara_fogo = (
    ((H <= 20) & (S > 120) & (V > 170)) |
    ((H >= 150) & (H <= 179) & (S > 130) & (V > 160))
)

    if np.sum(mascara_fogo) > (bloco_hsv.size * 0.03) and np.std(V) > 20:
        return QUEIMANDO


    if 85 <= h_mean <= 135 and s_mean > 45:
        return AGUA
    if 80 <= h_mean <= 115 and s_mean < 60 and v_mean > 160:
        return AGUA
    if s_mean < 35 and v_mean < 90 and 80 <= h_mean <= 140:
        return AGUA

    if 35 <= h_mean <= 90 and s_mean > 25 and v_mean > 40:
        return VEGETACAO

    if 20 <= h_mean <= 45 and s_mean > 28 and v_mean > 100:
        return VEGETACAO

    if s_mean < 35 and (
        (h_mean < 20 or h_mean > 160) or
        (20 < h_mean < 35) or
        (h_mean > 140 and s_mean < 30)
    ):
        return QUEIMADO


    return QUEIMADO

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
