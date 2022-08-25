#===============================================================================
# Exemplo: segmentação de uma imagem em escala de cinza.
#-------------------------------------------------------------------------------
# Autor: Bogdan T. Nassu
# Universidade Tecnológica Federal do Paraná
#===============================================================================

import sys
import timeit
import numpy as np
import cv2

#===============================================================================

INPUT_IMAGE =  'arroz.bmp'

# Valores de ajuste
NEGATIVO = False
THRESHOLD = 0.6
ALTURA_MIN = 18
LARGURA_MIN = 19
N_PIXELS_MIN = 445

# Valores de pixel (nao alterar)
ARROZ = -1
BACKGROUND = 0
FOREGROUND = 1

#===============================================================================

def binariza(img, threshold):
    ''' Binarização simples por limiarização.

Parâmetros: img: imagem de entrada. Se tiver mais que 1 canal, binariza cada
              canal independentemente.
            threshold: limiar.
            
Valor de retorno: versão binarizada da img_in.'''

    binary_img = np.where(img < threshold, BACKGROUND, FOREGROUND)
    return binary_img.astype(np.float32)

#-------------------------------------------------------------------------------

def rotula(img, largura_min, altura_min, n_pixels_min):
    '''Rotulagem usando flood fill. Marca os objetos da imagem com os valores
[0.1,0.2,etc].

Parâmetros: img: imagem de entrada E saída.
            largura_min: descarta componentes com largura menor que esta.
            altura_min: descarta componentes com altura menor que esta.
            n_pixels_min: descarta componentes com menos pixels que isso.

Valor de retorno: uma lista, onde cada item é um vetor associativo(dictionary)
com os seguintes campos:

'label': rótulo do componente.
'n_pixels': número de pixels do componente.
'T', 'L', 'B', 'R': coordenadas do retângulo envolvente de um componente conexo,
respectivamente: topo, esquerda, baixo e direita.'''

    largura = len(img[0])
    altura = len(img)
    rotulo = 0.1
    componentes = []

    # Altera branco para -1 para manipulacao
    img = np.where(img == FOREGROUND, ARROZ, BACKGROUND)

    for i in range(0, altura):
        for j in range(0, largura):
            if img[i][j][0] == ARROZ:
                componente = dict(
                    label = rotulo,
                    T = i,
                    L = j,
                    B = i,
                    R = j,
                    n_pixels = 0
                )

                c_processado = inunda(
                    img, altura, largura, i, j, componente
                )

                tamanho_min = dict(
                    altura = altura_min, 
                    largura = largura_min
                )
                # Verifica se o componente processado eh valido
                if (c_processado['n_pixels'] >= n_pixels_min and
                    dimensoes_validas(c_processado, tamanho_min)):
                    # Armazena o componente valido e incrementa o rotulo
                    componentes.append(c_processado)
                    rotulo += 0.1

    return componentes

#===============================================================================

def inunda(img, altura, largura, y, x, componente):
    '''Inunda a imagem a partir de um pixel guardando informacoes do componente.

Parâmetros: img: imagem de entrada E saída.
            y: y do pixel atual.
            x: x do pixel atual.
            componente: componente atual.

Valor de retorno: vetor associativo(dictionary) com os seguintes campos:

'label': rótulo do componente.
'n_pixels': número de pixels do componente.
'T', 'L', 'B', 'R': coordenadas do retângulo envolvente de um componente conexo,
respectivamente: topo, esquerda, baixo e direita.'''

    if img[y][x][0] != ARROZ:
        return componente

    img[y][x][0] = componente['label']
    componente['n_pixels'] += 1

    ### Guarda valores dos cantos
    # Topo se o 'y' for maior do que o já computado
    if componente['T'] > y:
        componente['T'] = y
    # Esquerda se o 'x' for menor do que o já computado
    if componente['L'] < x:
        componente['L'] = x
    # Topo se o 'y' for menor do que o já computado
    if componente['B'] < y:
        componente['B'] = y
    # Topo se o 'x' for maior do que o já computado
    if componente['R'] > x:
        componente['R'] = x

    ### Chama recursivamente a funcao em cada vizinho, se existir.
    # Vizinho de cima
    if y > 0:
        componente = inunda(img, altura, largura, y - 1, x, componente)
    # Vizinho de baixo
    if y < altura - 1:
        componente = inunda(img, altura, largura, y + 1, x, componente)
    # Vizinho da esquerda
    if x > 0:
        componente = inunda(img, altura, largura, y, x - 1, componente)
    # Vizinho da direita
    if x < largura - 1:
        componente = inunda(img, altura, largura, y, x + 1, componente)

    return componente

#===============================================================================
### Funcoes auxiliares

def altura(top, bottom):
    '''Calcula a altura de um componente baseada nos pontos superior e inferior
do eixo y.

Parâmetros: top: y superior.
            bottom: y inferior.

Valor de retorno: altura em pixels.'''

    if bottom > top:
        return abs(bottom - top)

    return abs(top - bottom)

def largura(left, right):
    '''Calcula a largura de um componente baseada nos pontos da esquerda e da
direita no eixo x.

Parâmetros: left: x da esquerda.
            right: x da direita.

Valor de retorno: largura em pixels.'''

    if left > right:
        return abs(left - right)

    return abs(right - left)

def dimensoes_validas(componente, tamanho_min):
    '''Valida o componente quanto ao seu tamanho minimo baseando-se nas
dimensoes de altura e largura

Parâmetros: componente: componente a ser validado.
            tamanho_min: dicionario contendo largura e altura minimas em pixels.

Valor de retorno: booleano indicando se as dimensoes sao validas ou nao.'''

    return (
        altura(componente['T'], componente['B']) >= tamanho_min['altura'] and
        largura(componente['L'], componente['R']) >= tamanho_min['largura']
    )

def sugere_parametros(componentes):
    '''Sugere parametros ideais baseando-se nos componentes encontrados.

Parâmetros: componentes: componentes encontrados.

Valor de retorno: nenhum. Resultado impresso no terminal.'''

    min_largura = 99999
    min_altura = 99999
    min_pixels = 99999

    for c in componentes:
        c_altura = altura(c['L'], c['R'])
        c_largura = largura(c['T'], c['B'])
        
        if c_largura < min_largura:
            min_largura = c_largura
        if c_altura < min_altura:
            min_altura = c_altura
        if c['n_pixels'] < min_pixels:
            min_pixels = c['n_pixels']

    print("\nCaso a imagem de saída tenha sido gerada como o esperado, para o threshold %.2f, os valores mínimos ideais seriam:" % THRESHOLD)
    print("Largura:", min_largura)
    print("Altura:", min_altura)
    print("Pixels:", min_pixels)

#===============================================================================

def main ():
    # Abre a imagem em escala de cinza.
    img = cv2.imread(INPUT_IMAGE, cv2.IMREAD_GRAYSCALE)
    if img is None:
        print('Erro abrindo a imagem.\n')
        sys.exit()

    # É uma boa prática manter o shape com 3 valores, independente da imagem ser
    # colorida ou não. Também já convertemos para float32.
    img = img.reshape((img.shape[0], img.shape[1], 1))
    img = img.astype(np.float32) / 255

    # Mantém uma cópia colorida para desenhar a saída.
    img_out = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)

    # Segmenta a imagem.
    if NEGATIVO:
        img = 1 - img
    img = binariza(img, THRESHOLD)
    cv2.imshow('01 - binarizada', img * 255)
    cv2.imwrite('01 - binarizada.png', img)

    start_time = timeit.default_timer()
    componentes = rotula(img, LARGURA_MIN, ALTURA_MIN, N_PIXELS_MIN)
    n_componentes = len(componentes)
    print('Tempo: %f' % (timeit.default_timer() - start_time))
    print('%d componentes detectados.' % n_componentes)

    sugere_parametros(componentes)

    # Mostra os objetos encontrados.
    for c in componentes:
        cv2.rectangle(img_out, (c ['L'], c ['T']), (c ['R'], c ['B']), (0,0,1))

    cv2.imshow('02 - out', img_out)
    cv2.imwrite('02 - out.png', img_out*255)
    cv2.waitKey()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()

#===============================================================================
