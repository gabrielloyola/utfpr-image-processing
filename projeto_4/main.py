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

# *** Valores de ajuste ***
# Blur
KERNEL = 13
SIGMA = 2.8

# Limiarizacao
T_KERNEL = 3
T_SIGMA = 0

# Blur 2
B2_KERNEL = 7
B2_SIGMA = 0

# Selecao
MIN_SIZE_FROM_MEAN = .5
MAX_SIZE_FROM_MEDIAN = 1.2

def main ():
    gabarito = escolhe_gabarito()

    img = cv2.imread("img/{}.bmp".format(gabarito), cv2.IMREAD_GRAYSCALE)
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

    borradona = cv2.GaussianBlur(binarizada, (B2_KERNEL, B2_KERNEL), B2_SIGMA)

    cv2.imshow('05 - borradona', borradona * 255)
    cv2.imwrite('05 - Borradona.png', borradona * 255)

    # Componentes conexos
    _n_components, labels, stats, _centroids = cv2.connectedComponentsWithStats(borradona, connectivity=8)

    valid_stats = graos_validos(stats)

    # Mostra os objetos encontrados.
    img_out = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    for stat in valid_stats:
        top_left_yx = (stat[cv2.CC_STAT_LEFT], stat[cv2.CC_STAT_TOP])
        bottom_right_yx = (stat[cv2.CC_STAT_LEFT] + stat[cv2.CC_STAT_WIDTH], stat[cv2.CC_STAT_TOP] + stat[cv2.CC_STAT_HEIGHT])
        cv2.rectangle(img_out, top_left_yx, bottom_right_yx, (0,0,1))

    cv2.imshow('06 - OUT', img_out)
    cv2.imwrite('06 - OUT.png', img_out)

    n_graos = len(valid_stats)
    diff = abs(gabarito - n_graos)
    erro = diff * 100 / gabarito

    print('Gabarito escolhido:', gabarito)
    print('%d componentes detectados.' % n_graos)
    print('Erro: %.2f%%' % erro)

    cv2.waitKey()
    cv2.destroyAllWindows()

def escolhe_gabarito():
    while(True):
        print('1 - 60')
        print('2 - 82')
        print('3 - 114')
        print('4 - 150')
        print('5 - 205')

        escolha = str(input('Escolha uma imagem: '))

        if escolha == '1':
            return 60
        elif escolha == '2':
            return 82
        elif escolha == '3':
            return 114
        elif escolha == '4':
            return 150
        elif escolha == '5':
            return 205
        else:
            print('Opcao invalida.')

def graos_validos(stats):
    # Desconsidera fundo
    stats = stats[1:]

    sizes = [stat[cv2.CC_STAT_AREA] for stat in stats]
    mean_size = np.mean(sizes)

    return [valid_stat for valid_stat in stats if valid_stat[cv2.CC_STAT_AREA] > mean_size * MIN_SIZE_FROM_MEAN]

if __name__ == '__main__':
    main()

#===============================================================================
