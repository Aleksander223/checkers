# constants
BOARD_SIZE = 8
RED_SYMBOL = 'r'
BLUE_SYMBOL = 'b'
RED_KING_SYMBOL = 'R'
BLUE_KING_SYMBOL = 'B'
BLANK_SYMBOL = '.'

class Board:
    def __init__(self):
        self.board = [[ BLANK_SYMBOL for i in range(BOARD_SIZE) ] for j in range (BOARD_SIZE)]
        self.BOARD_SIZE = BOARD_SIZE

        self.RED_SYMBOL = RED_SYMBOL
        self.BLUE_SYMBOL = BLUE_SYMBOL

        self.RED_KING_SYMBOL = RED_KING_SYMBOL
        self.BLUE_KING_SYMBOL = BLUE_KING_SYMBOL

        self.BLANK_SYMBOL = BLANK_SYMBOL

        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                # red
                if (i == 0 or i == 2):
                    if (j % 2 == 1):
                        self.board[i][j] = RED_SYMBOL
                elif (i == 1):
                    if (j % 2 == 0):
                        self.board[i][j] = RED_SYMBOL
                # blue
                elif (i == 5 or i == 7):
                    if (j % 2 == 0):
                        self.board[i][j] = BLUE_SYMBOL
                elif (i == 6):
                    if (j % 2 == 1):
                        self.board[i][j] = BLUE_SYMBOL

    def inBounds(self, i, j):
        return (i >= 0 and j >= 0 and i < BOARD_SIZE and j < BOARD_SIZE)

    def isBlank(self, i, j):
        if not self.inBounds(i, j):
            return False

        return (self.board[i][j] == BLANK_SYMBOL)

    def isOpponent(self, i, j, symbol):
        if (not self.inBounds(i, j)):
            return False

        if (symbol == RED_SYMBOL or symbol == RED_KING_SYMBOL):
            return (self.board[i][j] == BLUE_SYMBOL or self.board[i][j] == BLUE_KING_SYMBOL)

        return (self.board[i][j] == RED_SYMBOL or self.board[i][j] == RED_KING_SYMBOL)

    def canEatPieceDown(self, i, j, symbol):
        pieces = []

        if (self.inBounds(i + 1, j - 1) and self.isOpponent(i + 1, j - 1, symbol) and self.isBlank(i + 2, j - 2)):
            pieces.append((i + 1, j - 1))

        if (self.inBounds(i + 1, j + 1) and self.isOpponent(i + 1, j + 1, symbol) and self.isBlank(i + 2, j + 2)):
            pieces.append((i + 1, j + 1))

        return pieces

    def canEatPieceUp(self, i, j, symbol):
        pieces = []

        if (self.inBounds(i - 1, j - 1) and self.isOpponent(i - 1, j - 1, symbol) and self.isBlank(i - 2, j - 2)):
            pieces.append((i - 1, j - 1))

        if (self.inBounds(i - 1, j + 1) and self.isOpponent(i - 1, j + 1, symbol) and self.isBlank(i - 2, j + 2)):
            pieces.append((i - 1, j + 1))

        return pieces

    def canEatPieces(self, symbol, down=False, up=False):
        pieces = []

        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                if (self.board[i][j].lower() == symbol or self.board[i][j].upper() == symbol):
                    if (symbol.isupper()):
                        pieces += (self.canEatPieceDown(i, j, symbol))
                        pieces += (self.canEatPieceUp(i, j, symbol))
                    else:
                        if (down):
                            pieces += (self.canEatPieceDown(i, j, symbol))

                        if (up):
                            pieces += (self.canEatPieceUp(i, j, symbol))

        return pieces

    def goingThroughPiece(self, i, j, x, y, symbol):
        down = (x > i)
        up = (x < i)

        left = (y < j)
        right = (y > j)

        if (down):
            if (left):
                if (self.isOpponent(i + 1, j - 1, symbol)):
                    return (i + 1, j - 1)
                else:
                    return tuple()
            elif (right):
                if (self.isOpponent(i + 1, j + 1, symbol)):
                    return (i + 1, j + 1)
                else:
                    return tuple()

        if (up):
            if (left):
                if (self.isOpponent(i - 1, j - 1, symbol)):
                    return (i + 1, j - 1)
                else:
                    return tuple()
            elif (right):
                if (self.isOpponent(i - 1, j + 1, symbol)):
                    return (i + 1, j + 1)
                else:
                    return tuple()

    def move(self, startX, startY, endX, endY, symbol):
        eatingPiece = False

        if (self.board[startX][startY] != symbol):
            raise Exception("Please move a valid piece")

        if (self.board[endX][endY] != BLANK_SYMBOL):
            raise Exception("Please move the piece onto a blank space")

        if (startX < 0 or startX >= BOARD_SIZE or startY < 0 or startY >= BOARD_SIZE):
            raise Exception("Invalid start coordinates")

        if (endX < 0 or endX >= BOARD_SIZE or endY < 0 or endY >= BOARD_SIZE):
            raise Exception("Invalid end coordinates")

        if (symbol == RED_SYMBOL):
            print(self.canEatPieces(symbol, up=True), self.goingThroughPiece(startX, startY, endX, endY, symbol))
            # check if must eat piece and not eating
            if (self.canEatPieces(symbol, down=True) and not self.goingThroughPiece(startX, startY, endX, endY, symbol)):
                raise Exception("Must eat piece")

            if (endX != startX + 1 or not(endY == startY + 1 or endY == startY - 1)):
                # check if eating a piece
                if (endX != startX + 2):
                    raise Exception("Illegal move")

                # if not(self.isOpponent(startX + 1, startY - 1, symbol) or self.isOpponent(startX + 1, startY + 1, symbol)):
                #     raise Exception("Illegal move")

                if not(self.canEatPieceDown(startX, startY, symbol)):
                    raise Exception("Illegal move")

                if not(endY == startY - 2 or endY == startY + 2):
                    raise Exception("Illegal move")

                eatingPiece = True

                eatX = startX + 1

                if (endY > startY):
                    eatY = endY - 1
                else:
                    eatY=  endY + 1

        elif (symbol == BLUE_SYMBOL):
            print(self.canEatPieces(symbol, up=True), self.goingThroughPiece(startX, startY, endX, endY, symbol))
            if (self.canEatPieces(symbol, up=True) and not self.goingThroughPiece(startX, startY, endX, endY, symbol)):
                raise Exception("Must eat piece")

            if (endX != startX - 1 or  not(endY == startY + 1 or endY == startY - 1)):
                # check if eating a piece
                if (endX != startX - 2):
                    raise Exception("Illegal move 1")

                # if not(self.isOpponent(startX -1, startY - 1, symbol) or self.isOpponent(startX - 1, startY + 1, symbol)):
                #     raise Exception("Illegal move")

                if not(self.canEatPieceUp(startX, startY, symbol)):
                    raise Exception("Illegal move 2")

                if not(endY == startY - 2 or endY == startY + 2):
                    raise Exception("Illegal move 3")

                eatingPiece = True

                eatX = startX - 1

                if (endY > startY):
                    eatY = endY - 1
                else:
                    eatY=  endY + 1

        elif (symbol == RED_KING_SYMBOL or symbol == BLUE_KING_SYMBOL):
            print(self.canEatPieces(symbol, up=True), self.goingThroughPiece(startX, startY, endX, endY, symbol))
            if (self.canEatPieces(symbol, down=True, up=True) and not self.goingThroughPiece(startX, startY, endX, endY, symbol)):
                raise Exception("Must eat piece")

            if (not(endX == startX + 1 or endX == startX - 1) or not(endY == startY + 1 or endY == startY - 1)):
                # check if eating a piece
                if not(endX == startX + 2 or endX == startX - 2):
                    raise Exception("Illegal move | bad X coordinate")

                # check for enemies
                # if not(self.isOpponent(startX + 1, startY - 1, symbol) or self.isOpponent(startX + 1, startY + 1, symbol)
                #     or self.isOpponent(startX - 1, startY - 1, symbol) or self.isOpponent(startX - 1, startY + 1, symbol)):
                #     raise Exception("Illegal move | no enemy")

                if not(self.canEatPieceUp(startX, startY, symbol) or self.canEatPieceDown(startX, startY, symbol)):
                    raise Exception("Illegal move | no enemy")

                if not(endY == startY - 2 or endY == startY + 2):
                    raise Exception("Illegal move | bad Y coordinate")

                eatingPiece = True

                if (endX > startX):
                    eatX = startX + 1
                else:
                    eatX = startX - 1

                if (endY > startY):
                    eatY = endY - 1
                else:
                    eatY=  endY + 1


        self.board[endX][endY] = self.board[startX][startY]
        self.board[startX][startY] = BLANK_SYMBOL

        if (eatingPiece):
            self.board[eatX][eatY] = BLANK_SYMBOL

        # red upgrade
        if (symbol == RED_SYMBOL and endX == BOARD_SIZE - 1):
            self.board[endX][endY] = RED_KING_SYMBOL

        # blue upgrade
        if (symbol == BLUE_SYMBOL and endX == 0):
            self.board[endX][endY] = BLUE_KING_SYMBOL


    def print(self):
        # print guides
        print("   0 1 2 3 4 5 6 7")
        print("   ---------------")

        # print board
        for i in range(BOARD_SIZE):

            # print horizontal guide
            print(i, "| ", sep='', end='')

            for j in range(BOARD_SIZE):
                print(self.board[i][j], end=' ')
            print()

# while(True):
#     board.print()
#
#     choice = input("Type quit if you want to quit, else just enter: ")
#     if choice == "quit":
#         # score
#         break
#
#     sym = input("Symbol: ")
#     print(sym, "| New move (i, j) -> (x, y)")
#
#     try:
#         i = int(input("i: "))
#         j = int(input("j: "))
#         x = int(input("x: "))
#         y = int(input("y: "))
#
#     except Exception as E:
#         print("Invalid format, try again\n")
#         continue
#
#     try:
#         board.move(i, j, x, y, sym)
#     except Exception as E:
#         print("Error:", E)
