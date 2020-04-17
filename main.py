import pygame

pygame.init()

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Checkers")

# constants
TILE_SIZE = 60
TILE_OFFSET = 100

PIECE_SIZE = 60

redPNG = pygame.image.load("./res/red.png").convert_alpha()
bluePNG = pygame.image.load("./res/blue.png").convert_alpha()

# sprites
spr_tiles = pygame.sprite.Group()
spr_red = pygame.sprite.Group()
spr_blue = pygame.sprite.Group()

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
    def __init__(self, x, y, color):
        pygame.sprite.Sprite.__init__(self)

        self.color = color

        if (color == "red"):
            self.image = redPNG
        elif (color == "blue"):
            self.image = bluePNG

        self.rect = self.image.get_rect()

        # position
        self.rect.center = (x, y)

        if (color == "red"):
            spr_red.add(self)
        elif (color == "blue"):
            spr_blue.add(self)


# board init
white = True
tiles = []
for i in range(8):
    for j in range(8):
        if white:
            color = (255, 255, 255)
        else:
            color = (0, 0, 0)
        white = not white
        tiles.append( Tile(TILE_OFFSET + j * TILE_SIZE, TILE_OFFSET + i * TILE_SIZE, color, i, j) )

    # to stagger the tiles
    white = not white

# pieces
# red
reds = []
for i in range(3):
    for j in range(8):
        if (i % 2 != j % 2):
            reds.append( Piece(TILE_OFFSET + j * PIECE_SIZE, TILE_OFFSET + i * PIECE_SIZE, "red") )

# blue
blues = []
for i in range(5, 8):
    for j in range(8):
        if (i % 2 != j % 2):
            blues.append( Piece(TILE_OFFSET + j * PIECE_SIZE, TILE_OFFSET + i * PIECE_SIZE, "blue") )

clock = pygame.time.Clock()

while True:
    clock.tick(60)

    for event in pygame.event.get():
        # quit
        if event.type == pygame.QUIT:
            exit()

        # mouse
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            for red in reds:
                if red.rect.collidepoint(x, y):
                    print("Clicked on red piece")
            for blue in blues:
                if blue.rect.collidepoint(x, y):
                    print("Clicked on blue piece")

    # update

    # render
    screen.fill((190, 175, 175))
    spr_tiles.draw(screen)
    spr_red.draw(screen)
    spr_blue.draw(screen)

    pygame.display.flip()
