from constants import *
import pygame


def get_box_from_pixel(x, y):
    """Mouse given position to the appropriate row cal in the sudoku board."""
    if x and y:
        for row in range(N):
            for col in range(N):
                left, top = left_top_cube_coords(row, col)
                box_rect = pygame.Rect(left, top, BOX_SIZE, BOX_SIZE)
                if box_rect.collidepoint(x, y):
                    return row, col
    return None, None


def format_time(timer):
    """Get the timer game format."""
    sec = timer % 60
    minute = timer // 60
    return f'{str(minute).zfill(2)}:{str(sec).zfill(2)}'


def get_box_from_pixel(x, y):
    """Mouse given position to the appropriate row cal in the sudoku board."""
    if x and y:
        for row in range(N):
            for col in range(N):
                left, top = left_top_cube_coords(row, col)
                box_rect = pygame.Rect(left, top, BOX_SIZE, BOX_SIZE)
                if box_rect.collidepoint(x, y):
                    return row, col
    return None, None


def find_empty(board):
    """Find an empty location in the sudoku board.

    Args:
        board (list[int][int]): Array that contains all the numbers in the current board.

    Returns:
        i (int): row index position.
        j (int): col index position.
    """
    for i, line in enumerate(board):
        for j, num in enumerate(line):
            if num == 0:
                return i, j


def left_top_cube_coords(row, col):
    """Get the x,y position values for given cube position.

    Args:
        row (int): given cube row.
        col (int): given cube col.

    Returns:
        left (int): x cube position value, from 0 to the win width.
        top (int): y cube position value, from 0 to the win length.
    """
    box_x = row // 3
    box_y = col // 3
    left = (col * (BOX_SIZE + MINI_GAP_SIZE)) + (box_y * GAP_SIZE) + 40
    top = (row * (BOX_SIZE + MINI_GAP_SIZE)) + (box_x * GAP_SIZE) + 80
    return left, top
