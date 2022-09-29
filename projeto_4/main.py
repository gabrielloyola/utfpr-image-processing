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

GABARITO = 114

# *** Valores de ajuste ***
# Blur
KERNEL = 15
SIGMA = 5

# Binarizacao
THRESHOLD = 0.8

def main ():
    img = cv2.imread("img/{}.bmp".format(GABARITO), cv2.IMREAD_GRAYSCALE)
    if img is None:
        print('Erro abrindo a imagem.\n')
        sys.exit()

    img = 1 - img

    cv2.imshow('02 - Cinza', img * 255)
    cv2.imwrite('02 - Cinza.png', img)

    borrada = cv2.GaussianBlur(img, (KERNEL, KERNEL), SIGMA)

    cv2.imshow('02 - Borrada', borrada * 255)
    cv2.imwrite('02 - Borrada.png', borrada)

    binarizada = 1 - cv2.adaptiveThreshold(borrada, 1, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, KERNEL, SIGMA)
    cv2.imshow('03 - Binarizada', binarizada * 255)
    cv2.imwrite('03 - Binarizada.png', binarizada * 255)

    _ret, componentes = cv2.connectedComponents(binarizada, connectivity = 8)
    _unique, n_componentes = np.unique(componentes, return_counts = True)
    n_componentes = len(componentes)
    print('%d componentes detectados.' % n_componentes)

    cv2.waitKey()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()

#===============================================================================
