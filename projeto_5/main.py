#===============================================================================
# Chroma Key
#-------------------------------------------------------------------------------
# Universidade Tecnológica Federal do Paraná
# Alunos: Gabriel Leão Bernarde - 2194228
#         Gabriel Loyola - 1558587
#===============================================================================

import sys
import numpy as np
import cv2
import math

#===============================================================================

# *** Valores de ajuste ***

def main ():
    imagem = escolhe_imagem()

    img = cv2.imread("img/{}.bmp".format(imagem))
    if img is None:
        print('Erro abrindo a imagem.\n')
        sys.exit()

    img = img.astype(np.float32) / 255

    cv2.imshow('Img', img)

    fundo = cv2.imread('xpwallpaper.webp')
    fundo = fundo.astype(np.float32) / 255

    cv2.imshow('OUT', chroma_key(img, fundo))

    cv2.waitKey()
    cv2.destroyAllWindows()

def escolhe_imagem():
    while(True):
        escolha = int(input('Escolha uma imagem de 0 a 8: '))

        if escolha >= 0 and escolha <= 8: return escolha

        print('Opcao invalida.')

def chroma_key(img, fundo):
    blended = np.zeros(img.shape)
    sem_verde = img

    altura, largura, _n_camadas = img.shape
    fundo_resized = cv2.resize(fundo, (largura, altura))

    for y in range(altura):
        for x in range(largura):
            grau_verde = calcula_verdicidade(img[y][x])
            sem_verde[y][x][1] -= grau_verde

            blended[y][x] = fundo_resized[y][x] * grau_verde + sem_verde[y][x]

    return blended

def calcula_verdicidade(pixel):
    return max(pixel[1] - max(pixel[0], pixel[2]), 0)

if __name__ == '__main__':
    main()
