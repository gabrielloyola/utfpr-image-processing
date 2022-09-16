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

INPUT_IMAGE = 'b'
LARGURA_JANELA = 7
ALTURA_JANELA = 7

def calcula_media(janela):
    altura, largura = janela.shape

    soma = 0
    for y in range(0, altura):
        for x in range(0, largura):
            soma += janela[y][x]

    return soma / (largura * altura)

def blur_basico(img, altura_janela, largura_janela):
    altura, largura, n_canais = img.shape

    img_out = np.zeros(img.shape)

    cv2.medianBlur()

    for canal in range(0, n_canais):
        for y in range(altura_janela // 2, altura - altura_janela // 2):
            start_y = y - altura_janela // 2
            end_y = max(y + altura_janela // 2, 1) + 1
            for x in range(largura_janela // 2, largura - largura_janela // 2):
                start_x = x - largura_janela // 2
                end_x = max(x + largura_janela // 2, 1) + 1

                img_out[y][x][canal] = calcula_media(img[start_y:end_y, start_x:end_x, canal])

    return img_out

def blur_separavel(img, altura_janela, largura_janela):
    return blur_basico(blur_basico(img, altura_janela, 1), 1, largura_janela) # 1 linha :o

def imagem_integral(img):
    altura, largura, n_canais = img.shape
    
    integral = np.zeros(img.shape)

    for canal in range(0, n_canais):
        for y in range(0, altura):
            integral[y][0][canal] = img[y][0][canal]
            for x in range(1, largura):
                integral[y][x][canal] = img[y][x][canal] + integral[y][x - 1][canal]

        for y in range(1, altura):
            for x in range(0, largura):
                integral[y][x][canal] = integral[y][x][canal] + integral[y - 1][x][canal]

    print(integral[altura - 1][largura - 1])

    return integral

def blur_integral(img, altura_janela, largura_janela):
    altura, largura, n_canais = img.shape

    img_out = np.zeros(img.shape)
    integral = imagem_integral(img)

    for canal in range(0, n_canais):
        for y in range(altura_janela // 2, altura - altura_janela // 2):
            for x in range(largura_janela // 2, largura - largura_janela // 2):
                topo_esquerda = integral[y - altura_janela // 2][x - largura_janela // 2][canal]
                topo_direita = integral[y - altura_janela // 2][x + largura_janela // 2][canal]
                baixo_esquerda = integral[y + altura_janela // 2][x - largura_janela // 2][canal]
                baixo_direita = integral[y + altura_janela // 2][x + largura_janela // 2][canal]

                img_out[y][x][canal] = (baixo_direita - topo_direita - baixo_esquerda + topo_esquerda) / (altura_janela * largura_janela)

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
    img = blur_integral(img, ALTURA_JANELA, LARGURA_JANELA)
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