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
    mascara_verde = np.zeros((altura, largura))
    # Deixando o fundo do tamanho da imagem para não ter problemas de acesso inválido
    fundo = cv2.resize(fundo, (largura, altura))

    for y in range(altura):
        for x in range(largura):
            grau_verde = calcula_verdicidade(img[y][x])
            mascara_verde[y][x] = grau_verde
            sem_verde[y][x][1] -= grau_verde

    mascara_verde_positiva = mascara_verde[mascara_verde > 0]
    media_verde = np.mean(mascara_verde_positiva)
    desvio = np.std(mascara_verde_positiva)


    # TODO: Fazer o flood fill pra decidir melhor as bordas.

    for y in range(altura):
        for x in range(largura):
            if mascara_verde[y][x] < (media_verde - desvio):
                blended[y][x] = sem_verde[y][x]
            else:
                blended[y][x] = fundo[y][x]

    cv2.imshow('Mascara Verde', mascara_verde)

    return blended

def calcula_verdicidade(pixel):
    return max(pixel[1] - max(pixel[0], pixel[2]), 0)

if __name__ == '__main__':
    main()
