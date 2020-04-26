import checkers
import ai
import time


while True:
    player = input("1. Blue / 2. Red ")
    if (int(player) == 1):
        humanPlayer = 'blue'
        break
    elif (int(player) == 2):
        humanPlayer = 'red'
        break
    else:
        print("Invalid choice!")
        continue

while True:
    algorithm = input("1. MinMax / 2. AB Pruning ")
    if (int(algorithm) == 1):
        algo = 1
        break
    elif (int(algorithm) == 2):
        algo = 2
        break
    else:
        print("Invalid choice!")
        continue

while True:
    difficulty = input("1. Easy / 2. Medium / 3. Hard ")
    if (int(difficulty) == 1):
        max_depth = 2
        break
    elif (int(difficulty) == 2):
        max_depth = 4
        break
    elif (int(difficulty) == 3):
        max_depth = 6
        break
    else:
        print("Invalid choice!")
        continue

game = checkers.Board(humanPlayer)

while True:
    gameplay = input("1. Console / 2. GUI ")

    if int(gameplay) == 1:
        checkers.console(game, algo, max_depth)
        exit()
    elif int(gameplay) == 2:
        break
    else:
        print("Invalid choice!")
        continue

import pygame
pygame.init()

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Checkers")

# constants
TILE_SIZE = 60
TILE_OFFSET = 120

PIECE_SIZE = 40
PIECE_OFFSET = (TILE_SIZE - PIECE_SIZE)

redPNG = pygame.image.load("./res/red.png").convert_alpha()
bluePNG = pygame.image.load("./res/blue.png").convert_alpha()
redKingPNG = pygame.image.load("./res/red_king.png").convert_alpha()
blueKingPNG = pygame.image.load("./res/blue_king.png").convert_alpha()

# sprites
spr_tiles = pygame.sprite.Group()
spr_red = pygame.sprite.Group()
spr_blue = pygame.sprite.Group()

# fonts
font = pygame.font.SysFont('arial', 32)

# texts
error_text = font.render('', True, (0, 0, 0))
error_rect = error_text.get_rect()
error_rect = (88, 20)

blue_text = font.render('BLUE moves', True, (41, 88, 170))
blue_rect = blue_text.get_rect()
blue_rect = (300, 20)

red_text = font.render('RED moves', True, (234, 43, 31))
red_rect = red_text.get_rect()
red_rect = (300, 20)

# classes
class Tile(pygame.sprite.Sprite):
    def __init__(self, x, y, color, i, j):
        pygame.sprite.Sprite.__init__(self)

        self.i = i
        self.j = j

        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))
        self.image.fill(color)
        self.rect = self.image.get_rect()

        # position
        self.rect.center = (x, y)

        spr_tiles.add(self)

class Piece(pygame.sprite.Sprite):
    def __init__(self, x, y, color, i, j, king=False):
        pygame.sprite.Sprite.__init__(self)

        self.color = color

        self.i = i
        self.j = j
        self.king = king

        if (color == "red"):
            if (king):
                self.image = redKingPNG
            else:
                self.image = redPNG
        elif (color == "blue"):
            if (king):
                self.image = blueKingPNG
            else:
                self.image = bluePNG

        self.rect = self.image.get_rect()

        # position
        self.rect.center = (x, y)

        if (color == "red"):
            spr_red.add(self)
        elif (color == "blue"):
            spr_blue.add(self)



# board init
# logic board
tiles = []
reds = []
blues = []

def renderBoardFromState():
    # clear pieces
    spr_red.empty()
    spr_blue.empty()

    reds.clear()
    blues.clear()

    for i in range(game.BOARD_SIZE):
        for j in range(game.BOARD_SIZE):
            if (game.board[i][j] == game.RED_SYMBOL):
                reds.append( Piece(TILE_OFFSET + j * (PIECE_SIZE + PIECE_OFFSET), TILE_OFFSET + i * (PIECE_SIZE + PIECE_OFFSET), "red", i, j) )
            elif (game.board[i][j] == game.BLUE_SYMBOL):
                blues.append( Piece(TILE_OFFSET + j * (PIECE_SIZE + PIECE_OFFSET), TILE_OFFSET + i * (PIECE_SIZE + PIECE_OFFSET), "blue", i, j) )
            elif (game.board[i][j] == game.RED_KING_SYMBOL):
                reds.append( Piece(TILE_OFFSET + j * (PIECE_SIZE + PIECE_OFFSET), TILE_OFFSET + i * (PIECE_SIZE + PIECE_OFFSET), "red", i, j, king = True) )
            elif (game.board[i][j] == game.BLUE_KING_SYMBOL):
                blues.append( Piece(TILE_OFFSET + j * (PIECE_SIZE + PIECE_OFFSET), TILE_OFFSET + i * (PIECE_SIZE + PIECE_OFFSET), "blue", i, j, king = True) )

white = True
for i in range(8):
    for j in range(8):
        if white:
            color = (255, 238, 187)
        else:
            color = (85, 136, 34)
        white = not white
        tiles.append( Tile(TILE_OFFSET + j * TILE_SIZE, TILE_OFFSET + i * TILE_SIZE, color, i, j) )

    # to stagger the tiles
    white = not white

clock = pygame.time.Clock()

i_lastClicked = -1
j_lastClicked = -1
sym_lastClicked = ""
madeMove = True
blue_moves = game.blue_moves

initial_frame = False

current_state = ai.State(game, game.aiPlayer, max_depth)
while True:
    clock.tick(60)

    if (game.checkWin()):
        screen.fill((190, 175, 175))
        renderBoardFromState()

        if (game.checkWin() == 'red'):
            red_text = font.render('RED wins!', True, (234, 43, 31))
            red_rect = red_text.get_rect()
            red_rect = (300, 20)
            screen.blit(red_text, red_rect)
        elif (game.checkWin() == 'blue'):
            blue_text = font.render('BLUE wins!', True, (41, 88, 170))
            blue_rect = red_text.get_rect()
            blue_rect = (300, 20)
            screen.blit(blue_text, blue_rect)
        else:
            error_text = font.render('Draw!', True, (0, 0, 0))
            error_rect = red_text.get_rect()
            error_rect = (300, 20)
            screen.blit(error_text, error_rect)

        red_score = font.render('RED: ' + str(game.scoreHeuristic('red')) , True, (234, 43, 31))
        blue_score = font.render('BLUE: ' + str(game.scoreHeuristic('blue')) , True, (41, 88, 170))

        red_score_rect = red_score.get_rect()
        red_score_rect = (650, 100)

        blue_score_rect = blue_score.get_rect()
        blue_score_rect = (650, 160)

        screen.blit(red_score, red_score_rect)
        screen.blit(blue_score, blue_score_rect)

        spr_tiles.draw(screen)
        spr_red.draw(screen)
        spr_blue.draw(screen)

        pygame.display.flip()
        time.sleep(3)
        exit()

    for event in pygame.event.get():
        # quit
        if event.type == pygame.QUIT:
            screen.fill((190, 175, 175))
            renderBoardFromState()

            red_score = font.render('RED: ' + str(game.scoreHeuristic('red')) , True, (234, 43, 31))
            blue_score = font.render('BLUE: ' + str(game.scoreHeuristic('blue')) , True, (41, 88, 170))

            red_score_rect = red_score.get_rect()
            red_score_rect = (650, 100)

            blue_score_rect = blue_score.get_rect()
            blue_score_rect = (650, 160)

            screen.blit(red_score, red_score_rect)
            screen.blit(blue_score, blue_score_rect)

            spr_tiles.draw(screen)
            spr_red.draw(screen)
            spr_blue.draw(screen)

            pygame.display.flip()
            time.sleep(3)
            exit()

        # mouse
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            for red in reds:
                if red.rect.collidepoint(x, y) and not blue_moves and humanPlayer == 'red':
                    print("Clicked on red piece ", red.i, red.j)
                    i_lastClicked = red.i
                    j_lastClicked = red.j

                    if (red.king):
                        sym_lastClicked = game.RED_KING_SYMBOL
                    else:
                        sym_lastClicked = game.RED_SYMBOL

            for blue in blues:
                if blue.rect.collidepoint(x, y) and blue_moves and humanPlayer == 'blue':
                    print("Clicked on blue piece", blue.i, blue.j)
                    i_lastClicked = blue.i
                    j_lastClicked = blue.j

                    if (blue.king):
                        sym_lastClicked = game.BLUE_KING_SYMBOL
                    else:
                        sym_lastClicked = game.BLUE_SYMBOL

            for tile in tiles:
                if tile.rect.collidepoint(x, y):
                    if (tile.i == i_lastClicked and tile.j == j_lastClicked):
                        continue

                    print("Clicked on tile", tile.i, tile.j)

                    error_text = font.render('', True, (0, 0, 0))
                    error_rect = error_text.get_rect()
                    error_rect = (88, 20)

                    if(i_lastClicked != -1 and j_lastClicked != -1 and sym_lastClicked != ""):
                        try:
                            game.move(i_lastClicked, j_lastClicked, tile.i, tile.j, sym_lastClicked)
                            madeMove = True
                        except Exception as E:
                            print("Error:", E)

                            error_text = font.render(str(E), True, (0, 0, 0))
                            error_rect = error_text.get_rect()
                            error_rect = (88, 20)


                    i_lastClicked = -1
                    j_lastClicked = -1

    # update
    # ai move
    if ( initial_frame and (blue_moves and humanPlayer == 'red') or (not blue_moves and humanPlayer == 'blue' )):
        if (algo == 1):
            current_state = ai.min_max(current_state)
        else:
            current_state = ai.ab_pruning(-1000, +1000, current_state)

        game.board = current_state.choice.board.board
        game.blue_moves = current_state.choice.board.blue_moves

        madeMove = True
        blue_moves = game.blue_moves
    else:
        initial_frame = True

    if(madeMove == True):
        renderBoardFromState()
        game.print()
        madeMove = False

        blue_moves = game.blue_moves



    # render
    screen.fill((190, 175, 175))
    spr_tiles.draw(screen)
    spr_red.draw(screen)
    spr_blue.draw(screen)

    screen.blit(error_text, error_rect)

    if (blue_moves):
        screen.blit(blue_text, blue_rect)
    else:
        screen.blit(red_text, red_rect)

    pygame.display.flip()
