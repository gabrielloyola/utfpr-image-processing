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

    altura, largura, n_canais = img.shape

    mascara_verde, img = cria_mascara_verde(img, altura, largura)

    cv2.imshow('Sem verde', img)

    background = cv2.imread('xpwallpaper.webp')
    background = background.astype(np.float32) / 255

    blended =  + cv2.resize(background, (largura, altura))

    cv2.imshow('OUT', blended)

    cv2.waitKey()
    cv2.destroyAllWindows()

def escolhe_imagem():
    while(True):
        escolha = int(input('Escolha uma imagem de 0 a 8: '))

        if escolha >= 0 and escolha <= 8: return escolha

        print('Opcao invalida.')

def cria_mascara_verde(img, altura, largura):
    mask = np.zeros((altura, largura))
    sem_verde = img

    for y in range(altura):
        for x in range(largura):
            grau_verde = calcula_verdicidade(img[y][x])
            mask[y][x] = grau_verde
            sem_verde[y][x][1] -= grau_verde

    cv2.imshow('Mask', mask)

    return mask, aux

def calcula_verdicidade(pixel):
    return pixel[1] - max(pixel[0], pixel[2])

if __name__ == '__main__':
    main()
