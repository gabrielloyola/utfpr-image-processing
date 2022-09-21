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

THRESHOLD = .482
SIGMA = 2
INPUT_IMG = 'GT2.bmp'
#INPUT_IMG = 'Wind Waker GC.bmp'
IMG_MULT = 0.9
BLOOM_MULT = .05

def main():
    img = cv2.imread(INPUT_IMG)
    if img is None:
        print('Erro ao abrir a imagem.\n')
        sys.exit()
    mask = cv2.imread(INPUT_IMG,cv2.IMREAD_GRAYSCALE)
    mask = mask.reshape((mask.shape[0], mask.shape[1], 1))
    # Convertendo para float32.
    img = img.astype(np.float32) / 255
    mask = mask.astype(np.float32) / 255
    
    cv2.imshow('01 - Original', img)
    cv2.imwrite('01 - Original.bmp', img * 255)
    
    img_limiar = np.where(mask > THRESHOLD, img, 0)

    cv2.imshow('02 - limiar', img_limiar)
    bloom_media = np.zeros(img.shape)
    for i in range(0,4):
      bloom_media += cv2.blur(img_limiar,(19,19))
    cv2.imshow('BLOOM FILTRO DA MEDIA', bloom_media)  

    k = 33
    bloom = np.zeros(img.shape)
    for sigma_mult in [1, 2, 4, 8, 16, 32, 64, 128]:
        sg = k * sigma_mult
        bloom += cv2.GaussianBlur(img_limiar, (k, k), sg)

    cv2.imshow('BLOOOOM', bloom)

    img = img * IMG_MULT + bloom_media * BLOOM_MULT

    cv2.imshow('OUT', img)

    cv2.waitKey()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
