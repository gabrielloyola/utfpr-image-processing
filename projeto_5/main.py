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

# Verde Canonico
V = {
    'r': {
        'valor': 0,
        'peso': 0.1,
    },
    'g': {
        'valor': 236,
        'peso': 0.8,
    },
    'b': {
        'valor': 18,
        'peso': 0.1,
    },
}

def main ():
    imagem = escolhe_imagem()

    img = cv2.imread("img/{}.bmp".format(imagem))
    if img is None:
        print('Erro abrindo a imagem.\n')
        sys.exit()

    cv2.imshow('Img', img)

    altura, largura, n_canais = img.shape

    mascara_verde, img = cria_mascara_verde(img, altura, largura)

    cv2.imshow('Sem verde', img)

    img_xp = cv2.imread('xpwallpaper.webp')

    blended = img + cv2.resize(img_xp, (largura, altura))

    cv2.imshow('OUT', blended)

    cv2.waitKey()
    cv2.destroyAllWindows()

def escolhe_imagem():
    while(True):
        escolha = int(input('Escolha uma imagem de 0 a 8: '))

        if escolha >= 0 and escolha <=8: return escolha

        print('Opcao invalida.')

def cria_mascara_verde(img, altura, largura):
    mask = np.zeros((altura, largura))
    aux = img

    for y in range(altura):
        for x in range(largura):
            mask[y][x] = calcula_verdicidade(img[y][x])
            aux[y][x][1] = 0

    cv2.imshow('Mask', mask)

    return mask, aux

def calcula_verdicidade(pixel):
    red = abs(V['r']['valor'] - pixel[0]) * V['r']['peso']
    green = abs(V['g']['valor'] - pixel[1]) * V['g']['peso']
    blue = abs(V['b']['valor'] - pixel[2]) * V['b']['peso']

    return (red + green + blue) / 255

if __name__ == '__main__':
    main()
