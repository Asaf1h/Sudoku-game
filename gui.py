import pygame
from constants import *
import utils


class gui:
    def __init__(self):
        self.FPS_CLOCK = pygame.time.Clock()

        pygame.font.init()
        self.win = pygame.display.set_mode((WIN_WIDTH, WIN_LENGTH))
        self.buttons = gui.make_buttons()
        pygame.display.set_caption("Sudoku Game")

    @staticmethod
    def make_buttons():
        # Creates the rects on the window.
        reset_surf, reset_rect = make_text(
            'Reset ', BLACK, RED, WIN_WIDTH - 93, WIN_LENGTH - 105)
        new_surf, new_rect = make_text(
            'New Game', BLACK, SILVER, WIN_WIDTH - 153, WIN_LENGTH - 70)
        solution_surf, solution_rect = make_text(
            'Show_Solution ', BLACK, GREEN, WIN_WIDTH - 210, WIN_LENGTH - 35)
        solve_surf, solve_rect = make_text(
            'Solve ', BLACK, GREEN, WIN_WIDTH / 2.5, WIN_LENGTH - 80, size=45)
        credits1_surf, credits1_rect = make_text(
            'Looking for my next challenge ', BLACK, ORANGE, 110, 5)
        credits2_surf, credits2_rect = make_text(
            'insert num and press Enter', BLACK, ORANGE, 125, 43)

        buttons = {'reset': (reset_surf, reset_rect), 'new game': (new_surf, new_rect),
                   'solution': (solution_surf, solution_rect), 'solve': (solve_surf, solve_rect),
                   'credits1': (credits1_surf, credits1_rect), 'credits2': (credits2_surf, credits2_rect)}
        return buttons

    def draw_high_light_box(self, color, row, col):
        """Draw the frame for each box."""
        left, top = utils.left_top_cube_coords(row, col)
        pygame.draw.rect(self.win, color, (left - 5, top - 5,
                                           BOX_SIZE + 10, BOX_SIZE + 10), 4)

    def redraw_window(self, timer, board, board_row, board_col):
        """Draw the game window."""
        self.win.fill(WINDOW_COLOR)
        fnt = pygame.font.SysFont('arial', 30, bold=True)
        time_surf = fnt.render(timer, True, BLACK)
        self.win.blit(time_surf, (20, WIN_LENGTH - 65))

        for val in self.buttons.values():
            surf, rect = val
            self.win.blit(surf, rect)
            self.draw_board(board)
        # the nasty syntax is because zero is a valid input for board_col, board_row
        if board_row != None and board_col != None:
            if board.insert == 'Success':
                self.draw_high_light_box(GREEN, board_row, board_col)
            elif board.insert == 'Failure':
                self.draw_high_light_box(RED, board_row, board_col)
            else:
                self.draw_high_light_box(BLACK, board_row, board_col)

    def draw_board(self, game_board):
        """Get the x,y position values for given cube position.

        Args:
            win (pygame object): helps to draw the board.

        Returns:  None
        """

        for row in range(N):
            for col in range(N):
                left, top = utils.left_top_cube_coords(row, col)
                pygame.draw.rect(
                    self.win, BOX_COLOR, (left, top, BOX_SIZE, BOX_SIZE))
                self.draw_cube(game_board.cubes[row][col], left, top)
                
    def draw_cube(self, cube, left, top):
        """Draw each cube number val.

            Args:
                win (pygame object): helps to draw the board.
                left (int): x cube position value, from 0 to the win width.
                top (int): y cube position value, from 0 to the win length.

            Returns:  None
        """
        val = cube.value
        temp = cube.temp
        if val != 0:
            if cube.original:
                font = pygame.font.SysFont('arial', 30, bold=True)
                text_surf = font.render(str(val), True, BLACK)
            else:
                font = pygame.font.SysFont('comicsansms', 25)
                text_surf = font.render(str(val), True, MID_BLACK)
        elif temp:
            font = pygame.font.SysFont('comicsansms', 25, )
            text_surf = font.render(str(temp), True, GREY)
        # return if it's an empty cube
        else:
            return
        text_rect = text_surf.get_rect()
        text_rect.center = int(left + BOX_SIZE / 2), int(top + BOX_SIZE / 2)
        self.win.blit(text_surf, text_rect)


def make_text(text, color, bgcolor, top, left, size=30):
    """Create rect and surf pygame object for the game window."""
    font = pygame.font.SysFont('calibri', size)
    text_surf = font.render(text, True, color, bgcolor)
    text_rect = text_surf.get_rect()
    text_rect.topleft = (top, left)
    return text_surf, text_rect
