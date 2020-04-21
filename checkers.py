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

    def isOpponent(self, i, j, symbol):
        if (symbol == RED_SYMBOL or symbol == RED_KING_SYMBOL):
            return (self.board[i][j] == BLUE_SYMBOL or self.board[i][j] == BLUE_KING_SYMBOL)

        return (self.board[i][j] == RED_SYMBOL or self.board[i][j] == RED_KING_SYMBOL)

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
            if (endX != startX + 1 or  not(endY == startY + 1 or endY == startY - 1)):
                # check if eating a piece
                if (endX != startX + 2):
                    raise Exception("Illegal move")

                if not(self.isOpponent(startX + 1, startY - 1, symbol) or self.isOpponent(startX + 1, startY + 1, symbol)):
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
            if (endX != startX - 1 or  not(endY == startY + 1 or endY == startY - 1)):
                # check if eating a piece
                if (endX != startX - 2):
                    raise Exception("Illegal move")

                if not(self.isOpponent(startX -1, startY - 1, symbol) or self.isOpponent(startX - 1, startY + 1, symbol)):
                    raise Exception("Illegal move")

                if not(endY == startY - 2 or endY == startY + 2):
                    raise Exception("Illegal move")

                eatingPiece = True

                eatX = startX - 1

                if (endY > startY):
                    eatY = endY - 1
                else:
                    eatY=  endY + 1

        elif (symbol == RED_KING_SYMBOL or symbol == BLUE_KING_SYMBOL):
            if (not(endX == startX + 1 or endX == startX - 1) or not(endY == startY + 1 or endY == startY - 1)):
                # check if eating a piece
                if not(endX == startX + 2 or endX == startX - 2):
                    raise Exception("Illegal move")

                # forward
                if not(self.isOpponent(startX + 1, startY - 1, symbol) or self.isOpponent(startX + 1, startY + 1, symbol)):
                    raise Exception("Illegal move")

                # backward
                if not(self.isOpponent(startX - 1, startY - 1, symbol) or self.isOpponent(startX - 1, startY + 1, symbol)):
                    raise Exception("Illegal move")

                if not(endY == startY - 2 or endY == startY + 2):
                    raise Exception("Illegal move")

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
