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

INPUT_IMAGE = 'a'
LARGURA_JANELA = 3
ALTURA_JANELA = 3

def blur_basico(img, altura_janela, largura_janela):
    altura, largura, n_canais = img.shape
    img_out = np.zeros(img.shape)

    for canal in range(0, n_canais):
        for y in range(int(altura_janela / 2), altura - int(altura_janela / 2)):
            start_y = y - int(altura_janela / 2)
            end_y = max(y + int(altura_janela / 2), 1) + 1
            for x in range(int(largura_janela / 2), int(largura - largura_janela / 2)):
                start_x = x - int(largura_janela / 2)
                end_x = max(x + int(largura_janela / 2), 1) + 1

                img_out[y][x][canal] = np.average(img[start_y:end_y, start_x:end_x][canal])

    return img_out

def blur_separavel(img, altura_janela, largura_janela):
    altura, largura, n_canais = img.shape

    img_out = np.zeros(img.shape)

    for canal in range(0, n_canais):
        for y in range(0, altura):
            soma = img[y][0:largura_janela][canal].sum()
            for x in range(int(largura_janela / 2), int(largura - largura_janela / 2)):
                if y < 0:
                    soma = soma - img[y-1][x][canal] + img[y + altura_janela][x][canal]

                img_out[y][x][canal] = soma / (altura_janela * largura_janela)
        
        for x in range(0, largura):
            soma = img_out[0:altura_janela][x][canal].sum()
            for y in range(int(altura_janela / 2), int(altura - altura_janela / 2)):
                if x < 0:
                    soma = soma - img_out[y-1][x][canal] + img_out[y + largura_janela][x][canal]

                img_out[y][x][canal] = soma / (altura_janela * largura_janela)

    return img_out

def imagem_integral(img):
    altura, largura, n_canais = img.shape
    
    img_out = np.zeros(img.shape)

    for c in range(0, n_canais):
        for y in range(0, altura):
            img_out[y][0][c] = img[y][0][c]
            for x in range(1, largura):
                img_out[y][x][c] = img[y][x][c] + img_out[y][x-1][c]

        for y in range(1, altura):
            for x in range(0, largura):
                img_out[y][x][c] = img_out[y][x][c] + img_out[y-1][x][c]

    return img_out

def main():
    img = cv2.imread("Exemplos/{} - Original.bmp".format(INPUT_IMAGE))
    if img is None:
        print('Erro ao abrir a imagem.\n')
        sys.exit()

    # Convertendo para float32.
    img = img.astype(np.float32) / 255

    cv2.imshow('01 - Original', img)
    cv2.imwrite('01 - Original.bmp', img * 255)

    start_time = timeit.default_timer()
    img = blur_separavel(img, ALTURA_JANELA, LARGURA_JANELA)
    print('Tempo: %f' % (timeit.default_timer() - start_time))

    cv2.imshow('02 - out', img)
    cv2.imwrite('02 - out.png', img * 255)

    img_base = cv2.imread("Exemplos/{} - Borrada {}x{}.bmp".format(INPUT_IMAGE, LARGURA_JANELA, ALTURA_JANELA))

    img_base = img_base.astype(np.float32) / 255

    cv2.imshow("Exemplos/{} - Borrada {}x{}.bmp".format(INPUT_IMAGE, LARGURA_JANELA, ALTURA_JANELA), img_base)

    cv2.waitKey()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()

#===============================================================================


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