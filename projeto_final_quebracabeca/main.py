#===============================================================================
# Projeto Final - Puzzle Solver
#-------------------------------------------------------------------------------
# Universidade Tecnológica Federal do Paraná
# Alunos: Gabriel Leão Bernarde - 2194228
#         Gabriel Loyola - 1558587
#===============================================================================

import sys
import numpy as np
import cv2

from piece_of import Piece
from neighbor import Neighbor, Side

#===============================================================================
# IMAGE='aaa.jpg'
# IMAGE='example.bmp'
# IMAGE='vava.jpg'
IMAGE='aaa.jpg'

# -> slice
N_LINHAS=6
N_COLUNAS=6

THRESHOLD = 50

def main ():
    img = cv2.imread("{}".format(IMAGE))
    if img is None:
        print('Erro abrindo a imagem.\n')
        sys.exit()

    img = img.astype(np.float32) / 255

    cv2.imshow('Img', img)

    puzzled = puzzle_image(img)

    cv2.imshow('Puzzled', puzzled)
    cv2.imwrite('puzzled-{}'.format(IMAGE), puzzled * 255)

    first_piece = solve(puzzled)

    if not first_piece:
        exit('No way to begin without a first piece. :\'(')

    solved = mount_puzzle(first_piece, img.shape)

    cv2.imshow('Solved', solved)
    cv2.imwrite('solved-{}'.format(IMAGE), solved * 255)

    cv2.waitKey()
    cv2.destroyAllWindows()


def puzzle_image(img):
    altura, largura, _n_canais = img.shape
    piece_size_y = altura // N_LINHAS
    piece_size_x = largura // N_COLUNAS

    pieces = slice_image(img, piece_size_y, piece_size_x)
    puzzled = randomize_pieces(pieces, img.shape, piece_size_y, piece_size_x)

    return puzzled

def slice_image(img, piece_size_y, piece_size_x):
    pieces = []

    for y in range(N_LINHAS):
        for x in range(N_COLUNAS):
            piece_start_y = y * piece_size_y
            piece_end_y = piece_start_y + piece_size_y
            piece_start_x = x * piece_size_x
            piece_end_x = piece_start_x + piece_size_x

            piece = Piece(content = img[piece_start_y:piece_end_y, piece_start_x:piece_end_x])
            pieces.append(piece)

    return pieces

def randomize_pieces(pieces, out_shape, piece_size_y, piece_size_x):
    out = np.zeros(out_shape)

    for y in range(N_LINHAS):
        for x in range(N_COLUNAS):
            start_y = y * piece_size_y
            end_y = start_y + piece_size_y
            start_x = x * piece_size_x
            end_x = start_x + piece_size_x

            next_piece_idx = np.random.randint(len(pieces))
            next_piece = pieces.pop(next_piece_idx)
            out[start_y:end_y, start_x:end_x] = next_piece.content

    return out

def solve(img):
    altura, largura, _n_canais = img.shape
    piece_size_y = altura // N_LINHAS
    piece_size_x = largura // N_COLUNAS

    puzzle_pieces = slice_image(img, piece_size_y, piece_size_x)
    pieces_done = []

    current_piece = puzzle_pieces.pop()
    while(len(puzzle_pieces)):
        puzzle_pieces, pieces_done = find_neighbors(puzzle_pieces, pieces_done, current_piece)
        current_piece = puzzle_pieces.pop()

    pieces_done.append(current_piece)

    first_piece = get_first_piece(pieces_done)

    return first_piece

def find_neighbors(pieces, pieces_done, current_piece):
    neighbor_candidates = {
        Side.LEFT: Neighbor(),
        Side.RIGHT: Neighbor(),
        Side.BOTTOM: Neighbor(),
        Side.TOP: Neighbor(),
    }

    for piece in pieces:
        left_diff = quadratic_diff(left_border(current_piece.content), right_border(piece.content))
        right_diff = quadratic_diff(right_border(current_piece.content), left_border(piece.content))
        bottom_diff = quadratic_diff(bottom_border(current_piece.content), top_border(piece.content))
        top_diff = quadratic_diff(top_border(current_piece.content), bottom_border(piece.content))

        if(left_diff < neighbor_candidates[Side.LEFT].diff):
            neighbor_candidates[Side.LEFT].diff = left_diff
            neighbor_candidates[Side.LEFT].piece = piece

        if(right_diff < neighbor_candidates[Side.RIGHT].diff):
            neighbor_candidates[Side.RIGHT].diff = right_diff
            neighbor_candidates[Side.RIGHT].piece = piece

        if(bottom_diff < neighbor_candidates[Side.BOTTOM].diff):
            neighbor_candidates[Side.BOTTOM].diff = bottom_diff
            neighbor_candidates[Side.BOTTOM].piece = piece

        if(top_diff < neighbor_candidates[Side.TOP].diff):
            neighbor_candidates[Side.TOP].diff = top_diff
            neighbor_candidates[Side.TOP].piece = piece


    # LEFT
    if(neighbor_candidates[Side.LEFT].diff < THRESHOLD):
        neighbor_idx = pieces.index(neighbor_candidates[Side.LEFT].piece)
        if ((current_piece.neighbors[Side.LEFT].piece == None or
            current_piece.neighbors[Side.LEFT].diff > neighbor_candidates[Side.LEFT].diff) and
            (pieces[neighbor_idx].neighbors[Side.RIGHT].piece == None or
            pieces[neighbor_idx].neighbors[Side.RIGHT].diff > neighbor_candidates[Side.LEFT].diff)):

            current_piece.neighbors[Side.LEFT] = neighbor_candidates[Side.LEFT]
            # Update neighbor in pieces array
            if pieces[neighbor_idx].neighbors[Side.RIGHT].piece != None:
                pieces[neighbor_idx].neighbors[Side.RIGHT].piece.neighbors[Side.LEFT] = None
            pieces[neighbor_idx].neighbors[Side.RIGHT] = Neighbor(piece = current_piece, diff = neighbor_candidates[Side.LEFT].diff)

    # RIGHT
    if(neighbor_candidates[Side.RIGHT].diff < THRESHOLD):
        neighbor_idx = pieces.index(neighbor_candidates[Side.RIGHT].piece)
        if ((current_piece.neighbors[Side.RIGHT].piece == None or
            current_piece.neighbors[Side.RIGHT].diff > neighbor_candidates[Side.RIGHT].diff) and
            (pieces[neighbor_idx].neighbors[Side.LEFT].piece == None or
            pieces[neighbor_idx].neighbors[Side.LEFT].diff > neighbor_candidates[Side.RIGHT].diff)):

            current_piece.neighbors[Side.RIGHT] = neighbor_candidates[Side.RIGHT]
            # Update neighbor in pieces array
            if pieces[neighbor_idx].neighbors[Side.LEFT].piece != None:
                pieces[neighbor_idx].neighbors[Side.LEFT].piece.neighbors[Side.RIGHT] = None
            pieces[neighbor_idx].neighbors[Side.LEFT] = Neighbor(piece = current_piece, diff = neighbor_candidates[Side.RIGHT].diff)


    # BOTTOM
    if(neighbor_candidates[Side.BOTTOM].diff < THRESHOLD):
        neighbor_idx = pieces.index(neighbor_candidates[Side.BOTTOM].piece)
        if ((current_piece.neighbors[Side.BOTTOM].piece == None or
            current_piece.neighbors[Side.BOTTOM].diff > neighbor_candidates[Side.BOTTOM].diff) and
            (pieces[neighbor_idx].neighbors[Side.TOP].piece == None or
            pieces[neighbor_idx].neighbors[Side.TOP].diff > neighbor_candidates[Side.BOTTOM].diff)):

            current_piece.neighbors[Side.BOTTOM] = neighbor_candidates[Side.BOTTOM]
            # Update neighbor in pieces array
            if pieces[neighbor_idx].neighbors[Side.TOP].piece != None:
                pieces[neighbor_idx].neighbors[Side.TOP].piece.neighbors[Side.BOTTOM] = None
            pieces[neighbor_idx].neighbors[Side.TOP] = Neighbor(piece = current_piece, diff = neighbor_candidates[Side.BOTTOM].diff)


    # TOP
    if(neighbor_candidates[Side.TOP].diff < THRESHOLD):
        neighbor_idx = pieces.index(neighbor_candidates[Side.TOP].piece)
        if ((current_piece.neighbors[Side.TOP].piece == None or
            current_piece.neighbors[Side.TOP].diff > neighbor_candidates[Side.TOP].diff) and
            (pieces[neighbor_idx].neighbors[Side.BOTTOM].piece == None or
            pieces[neighbor_idx].neighbors[Side.BOTTOM].diff > neighbor_candidates[Side.TOP].diff)):

            current_piece.neighbors[Side.TOP] = neighbor_candidates[Side.TOP]
            # Update neighbor in pieces array
            if pieces[neighbor_idx].neighbors[Side.BOTTOM].piece != None:
                pieces[neighbor_idx].neighbors[Side.BOTTOM].piece.neighbors[Side.TOP] = None
            pieces[neighbor_idx].neighbors[Side.BOTTOM] = Neighbor(piece = current_piece, diff = neighbor_candidates[Side.TOP].diff)

    current_piece.done = True
    pieces_done.append(current_piece)

    return pieces, pieces_done

def quadratic_diff(a, b):
    if len(a) != len(b): return print("QUADRATIC DIFF: Different sizes of array!")

    diff_sum = 0
    for i in range(len(a)):
        max_diff = 0
        for channel in range(len(a[i])):
            diff = pow(a[i][channel] - b[i][channel], 2)
            if diff > max_diff:
                max_diff = diff

        diff_sum += max_diff

    return diff_sum / len(a)

def left_border(piece):
    altura, _largura, _n_canais = piece.shape
    return piece[0:altura, 0]

def right_border(piece):
    altura, largura, _n_canais = piece.shape
    return piece[0:altura, largura - 1]

def bottom_border(piece):
    altura, largura, _n_canais = piece.shape
    return piece[altura - 1, 0:largura]

def top_border(piece):
    _altura, largura, _n_canais = piece.shape
    return piece[0, 0:largura]

def mount_puzzle(first_piece, shape):
    mounted = np.zeros(shape)
    piece_size_y, piece_size_x, _channels = first_piece.content.shape

    current_piece = first_piece
    first_of_line = first_piece
    for y in range(N_LINHAS):
        if y > 0 and y < N_LINHAS:
            if first_of_line and first_of_line.neighbors[Side.BOTTOM]:
                current_piece = first_of_line.neighbors[Side.BOTTOM].piece
                first_of_line = current_piece
            # else:
            #     mounted = np.roll(mounted, -piece_size_y, axis = 0)
        for x in range(N_COLUNAS):
            start_y = y * piece_size_y
            end_y = start_y + piece_size_y
            start_x = x * piece_size_x
            end_x = start_x + piece_size_x

            if current_piece:
                mounted[start_y:end_y, start_x:end_x] = current_piece.content

                if x < N_LINHAS:
                    if current_piece.neighbors[Side.RIGHT]:
                        current_piece = current_piece.neighbors[Side.RIGHT].piece
                    # else:
                    #     mounted = np.roll(mounted, piece_size_x)
            # else:
            #     mounted = np.roll(mounted, piece_size_x, axis = 1)

            cv2.imshow('Step', mounted)
            cv2.waitKey(50)

    return mounted

def get_first_piece(pieces):
    for piece in pieces:
        if piece.has_neighbor(Side.RIGHT) and \
            piece.has_neighbor(Side.BOTTOM) and \
            not piece.has_neighbor(Side.LEFT) and \
            not piece.has_neighbor(Side.TOP):

            return piece

if __name__ == '__main__':
    main()
