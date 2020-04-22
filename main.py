import pygame
import checkers

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
game = checkers.Board()
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

# # pieces
# # red
#
# for i in range(3):
#     for j in range(8):
#         if (i % 2 != j % 2):
#
#
# # blue
#
# for i in range(5, 8):
#     for j in range(8):
#         if (i % 2 != j % 2):


clock = pygame.time.Clock()

i_lastClicked = -1
j_lastClicked = -1
sym_lastClicked = ""
madeMove = True
blue_moves = game.blue_moves

while True:
    clock.tick(60)

    if (game.checkWin(game.RED_SYMBOL) or game.checkWin(game.BLUE_SYMBOL)):
        exit()

    for event in pygame.event.get():
        # quit
        if event.type == pygame.QUIT:
            exit()

        # mouse
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            for red in reds:
                if red.rect.collidepoint(x, y) and not blue_moves:
                    print("Clicked on red piece ", red.i, red.j)
                    i_lastClicked = red.i
                    j_lastClicked = red.j

                    if (red.king):
                        sym_lastClicked = game.RED_KING_SYMBOL
                    else:
                        sym_lastClicked = game.RED_SYMBOL

            for blue in blues:
                if blue.rect.collidepoint(x, y) and blue_moves:
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
