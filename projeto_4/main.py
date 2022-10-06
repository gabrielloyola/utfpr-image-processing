#===============================================================================
# Exemplo: segmentação de uma imagem em escala de cinza.
#-------------------------------------------------------------------------------
# Autor: Bogdan T. Nassu
# Universidade Tecnológica Federal do Paraná
# Alunos: Gabriel Leão Bernarde - 2194228
#         Gabriel Loyola - 1558587
#===============================================================================

import sys
import numpy as np
import cv2

#===============================================================================

GABARITO = 150

# *** Valores de ajuste ***
# Blur
KERNEL = 21
SIGMA = 3

# Limiarizacao
T_KERNEL = 3
T_SIGMA = 0

# Fechamento
F_KERNEL = 3

# Abertura
O_KERNEL = 5

# Blur 2
B2_KERNEL = 7
B2_SIGMA = 0

# Selecao
MIN_SIZE = 16

def main ():
    img = cv2.imread("img/{}.bmp".format(GABARITO), cv2.IMREAD_GRAYSCALE)
    if img is None:
        print('Erro abrindo a imagem.\n')
        sys.exit()

    cv2.imshow('00 - Original', img)
    cv2.imwrite('00 - Original.png', img)

    borrada = cv2.GaussianBlur(img, (KERNEL, KERNEL), SIGMA)

    cv2.imshow('01 - Borrada', borrada)
    cv2.imwrite('01 - Borrada.png', borrada)

    binarizada = cv2.adaptiveThreshold(borrada, 1, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, T_KERNEL, T_SIGMA)
    cv2.imshow('02 - Binarizada', binarizada * 255)
    cv2.imwrite('02 - Binarizada.png', binarizada * 255)

    fechada = cv2.dilate(binarizada, (F_KERNEL, F_KERNEL))
    fechada = cv2.erode(fechada, (F_KERNEL, F_KERNEL))

    cv2.imshow('03 - fechada', fechada * 255)
    cv2.imwrite('03 - Fechada.png', fechada * 255)

    aberta = cv2.erode(fechada, (O_KERNEL, O_KERNEL))
    aberta = cv2.dilate(aberta, (O_KERNEL, O_KERNEL))

    cv2.imshow('04 - aberta', aberta * 255)
    cv2.imwrite('04 - Aberta.png', aberta * 255)

    borradona = cv2.GaussianBlur(aberta, (B2_KERNEL, B2_KERNEL), B2_SIGMA)

    cv2.imshow('05 - borradona', borradona * 255)
    cv2.imwrite('05 - Borradona.png', borradona * 255)

    # Componentes conexos
    _ret, comp = cv2.connectedComponents(borradona, connectivity = 8)
    _uniq, componentes = np.unique(comp, return_counts = True)

    # Descartando os componentes pequenos
    componentes_validos = [size for size in componentes if size > MIN_SIZE]
    n_componentes = len(componentes_validos) - 1

    diff = abs(GABARITO - n_componentes)
    erro = diff * 100 / GABARITO

    print('%d componentes detectados.' % n_componentes)
    print('erro: %.2f%%' % erro)

    cv2.waitKey()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()

#===============================================================================
