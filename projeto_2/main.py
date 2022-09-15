#===============================================================================
# Universidade Tecnológica Federal do Paraná
# Alunos: Gabriel Leão Bernarde - 2194228
#         Gabriel Loyola - 1558587
#===============================================================================

import sys
import timeit
import numpy as np
import cv2

#===============================================================================

INPUT_IMAGE =  'Exemplos/b - Original.bmp'
LARGURA_JANELA = 11
ALTURA_JANELA = 15

def blur_basico(img, altura_janela, largura_janela):
    largura = len(img[0])
    altura = len(img)

    img_out = np.zeros(img.shape)

    for c in range(0, 3):
        for y in range(int(altura_janela / 2), int(altura - altura_janela / 2)):
            start_y = int(y - altura_janela / 2)
            end_y = max(int(y + altura_janela / 2), 1)
            for x in range(int(largura_janela / 2), int(largura - largura_janela / 2)):
                start_x = int(x - largura_janela / 2)
                end_x = max(int(x + largura_janela / 2), 1)

                img_out[y][x][c] = calcula_media(img[start_y:end_y, start_x:end_x], c)

    return img_out

def blur_separavel(img, altura_janela, largura_janela):
    largura = len(img[0])
    altura = len(img)

    img_out = np.zeros(img.shape)

    for c in range(0, 3):
        for y in range(int(altura_janela / 2), int(altura - altura_janela / 2)):
            start_y = int(y - altura_janela / 2)
            end_y = max(int(y + altura_janela / 2), 1)
            for x in range(int(largura_janela / 2), int(largura - largura_janela / 2)):
                start_x = int(x - largura_janela / 2)
                end_x = max(int(x + largura_janela / 2), 1)

                img_out[y][x][c] = calcula_media(img[start_y:end_y, start_x:end_x], c)

    return img_out

def calcula_media(janela, channel):
    largura = len(janela[0])
    altura = len(janela)

    soma = 0
    for y in range(0, altura):
        for x in range(0, largura):
            soma += janela[y][x][channel]

    return soma / (altura * largura)

def imagem_integral(img):
    largura = len(janela[0])
    altura = len(janela)
    
    img_out = np.zeros(img.shape)
    for c in range(0,3):
        for y in range(0,altura):
            img_out[y][0][c] =img[y][0][c]
            for x in range(1,largura):
                img_out[y][x][c] =img[y][x]+img_out[y][x-1][c]
        for y in range(1,altura):
            for x in range(0,largura):
                img_out[y][x][c] = img_out[y][x][c] + img_out[y-1][x][c]

    return img_out            

def main():
    img = cv2.imread(INPUT_IMAGE)
    if img is None:
        print('Erro ao abrir a imagem.\n')
        sys.exit()

    # Convertendo para float32.
    img = img.astype(np.float32) / 255

    cv2.imshow('01 - Original', img)
    cv2.imwrite('01 - Original.bmp', img * 255)

    start_time = timeit.default_timer()
    img = blur_basico(img, ALTURA_JANELA, LARGURA_JANELA)
    print('Tempo: %f' % (timeit.default_timer() - start_time))

    cv2.imshow('02 - out', img)
    cv2.imwrite('02 - out.png', img * 255)

    img_base = cv2.imread("Exemplos/b - Borrada {}x{}.bmp".format(LARGURA_JANELA, ALTURA_JANELA))

    cv2.imshow("Exemplos/b - Borrada {}x{}.bmp".format(LARGURA_JANELA, ALTURA_JANELA), img_base)

    cv2.waitKey()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()

#===============================================================================
"teste"

"""
X   X   X   X   X   X   X   X   X   X   X   X   X   X   X   X   X   X   

X   X   X   X   X   X   X   X   X   X   X   X   X   X   X   X   X   X   

X   X   X   X   X   X   X   X   X   X   X   X   X   X   X   X   X   X   

X   X   X   X   X   X   X   X   X   X   X   X   X   X   X   X   X   X   

X   X   X   X   X   X   X   X   X   X   X   X   X   X   X   X   X   X   

X   X   X   X   X   X   X   X   X   X   X   X   X   X   X   X   X   X   

X   X   X   X   X   X   X   X   X   X   X   X   X   X   X   X   X   X   

X   X   X   X   X   X   X   X   X   X   X   X   X   X   X   X   X   X   

X   X   X   X   X   X   X   X   X   X   X   X   X   X   X   X   X   X   

X   X   X   X   X   X   X   X   X   X   X   X   X   X   X   X   X   X 

""" 