import utils
import logic
import gui
import pygame
import time

from constants import *


def main():

    # initializing values
    board_row, board_col, mouse_x, mouse_y, key, prev_board_row, prev_board_col = [
        None] * 7

    win = gui.gui()

    start_time = time.time()

    # ולהכניס ללוגיקה לתקן!!!!!!!!!!!!!
    game_board = logic.Grid(*logic.sudoku_generator())

    run = True
    while run:
        play_time = utils.format_time(round(time.time() - start_time))
        win.FPS_CLOCK.tick(gui.FPS)

        for event in pygame.event.get():
            # exit the game
            if event.type == pygame.QUIT:
                run = False
            # check if key was pressed the game
            # the nasty syntax is because zero is a valid input for board_col, board_row
            elif event.type == pygame.KEYDOWN and (board_row, board_col) != (None, None):
                # check if the user entered number
                if 47 < event.key < 58:
                    key = event.key - 48
                # check if the user removed number
                elif event.key == pygame.K_BACKSPACE or event.key == pygame.K_DELETE:
                    key = 0
                    game_board.cubes[board_row][board_col].remove()
                    game_board.sudoku_board[board_row][board_col] = 0
                # check if the user insert number
                elif event.key == pygame.K_RETURN:
                    if game_board.cubes[board_row][board_col].temp != 0:
                        if game_board.place(game_board.cubes[board_row][board_col].temp, board_row, board_col):
                            game_board.insert = 'Success'
                        else:
                            game_board.insert = 'Failure'
                        key = None

            # get user mouse clicked position

            rects = [val[1] for val in win.buttons.values()]

            [reset_rect, new_rect, solve_rect, solution_rect,
                credits1_rect, credits2_rect] = rects

            if event.type == pygame.MOUSEMOTION:
                mouse_x, mouse_y = event.pos
            # get user mouse clicked position
            elif event.type == pygame.MOUSEBUTTONUP:
                mouse_x, mouse_y = event.pos
                # check if the user clicked on any of the game commands
                if solution_rect.collidepoint(mouse_x, mouse_y):
                    game_board.sudoku_board = [
                        game_board.sol[i].copy() for i in range(N)]
                    game_board.cubes = [
                        [logic.Cube(game_board.sol[i][j]) for j in range(N)] for i in range(N)]

                elif reset_rect.collidepoint(mouse_x, mouse_y):
                    game_board.reset_board()

                elif new_rect.collidepoint(mouse_x, mouse_y):
                    # ולהכניס ללוגיקה לתקן!!!!!!!!!
                    game_board = logic.Grid(*logic.sudoku_generator())

                    start_time = time.time()
                elif solve_rect.collidepoint(mouse_x, mouse_y) and utils.find_empty(game_board.sudoku_board):
                    comb_sets = sorted(logic.Grid.get_comb_sets(game_board.sudoku_board),
                                       reverse=True, key=lambda cube: len(cube[0]))
                    while not game_board.solver(comb_sets, win):
                        # fix wrong user input
                        game_board.fix_player_set_point(win)
                        comb_sets = sorted(logic.Grid.get_comb_sets(game_board.sudoku_board),
                                           reverse=True, key=lambda cube: len(cube[0]))

                    """comb_sets = sorted(Board.get_comb_sets(game_board.sudoku_board),
                                       reverse=True, key=lambda cube: len(cube[0]))
                    while not game_board.solver(comb_sets, win):
                        # fix wrong user input
                        game_board.fix_player_set_point(win)
                        comb_sets = sorted(Board.get_comb_sets(game_board.sudoku_board),
                                           reverse=True, key=lambda cube: len(cube[0]))"""

        board_row, board_col = utils.get_box_from_pixel(mouse_x, mouse_y)

        # the nasty syntax is because zero is a valid input for board_col, board_row
        if board_row != None and board_col != None:
            # clear the key variable if the user moves to an other cube
            if key:
                game_board.cubes[board_row][board_col].set_temp(key)
                key = None
            # takes care to change the color of the cube after passing a square
            elif (prev_board_row, prev_board_col) != (board_row, board_col):
                game_board.insert = 0
            prev_board_row, prev_board_col = board_row, board_col

        win.redraw_window(play_time, game_board, board_row, board_col)
        pygame.display.update()


if __name__ == '__main__':
    main()
