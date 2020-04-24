import copy
import ai

# constants
BOARD_SIZE = 8
RED_SYMBOL = 'r'
BLUE_SYMBOL = 'b'
RED_KING_SYMBOL = 'R'
BLUE_KING_SYMBOL = 'B'
BLANK_SYMBOL = '.'

class Board:
    def __init__(self, human):
        self.board = [[ BLANK_SYMBOL for i in range(BOARD_SIZE) ] for j in range (BOARD_SIZE)]
        self.BOARD_SIZE = BOARD_SIZE

        self.RED_SYMBOL = RED_SYMBOL
        self.BLUE_SYMBOL = BLUE_SYMBOL

        self.RED_KING_SYMBOL = RED_KING_SYMBOL
        self.BLUE_KING_SYMBOL = BLUE_KING_SYMBOL

        self.BLANK_SYMBOL = BLANK_SYMBOL

        self.humanPlayer = human
        self.aiPlayer = 'blue' if human == 'red' else 'red'

        self.blue_moves = True

        # self.board[0] = [BLANK_SYMBOL] * 8
        # self.board[1] = [BLANK_SYMBOL] * 8
        # self.board[2] = [BLANK_SYMBOL] * 8
        # self.board[3] = [BLANK_SYMBOL] * 4 + [RED_SYMBOL] + [BLANK_SYMBOL] * 3
        # self.board[4] = [BLANK_SYMBOL] * 8
        # self.board[5] = [BLANK_SYMBOL] * 2 + [RED_SYMBOL] + [BLANK_SYMBOL] * 5
        # self.board[6] = [BLANK_SYMBOL] * 8
        # self.board[7] = [BLUE_SYMBOL] + [BLANK_SYMBOL] * 7

        # self.board[0] =  [BLANK_SYMBOL] * 7 + [RED_KING_SYMBOL]
        # self.board[1] = [BLANK_SYMBOL] * 8
        # self.board[2] = [BLANK_SYMBOL] * 8
        # self.board[3] = [BLANK_SYMBOL] * 8
        # self.board[4] = [BLANK_SYMBOL] * 8
        # self.board[5] = [BLANK_SYMBOL] * 8
        # self.board[6] = [BLANK_SYMBOL] * 8
        # self.board[7] = [BLUE_KING_SYMBOL] + [BLANK_SYMBOL] * 8

        # self.board[0] = [BLANK_SYMBOL] * 7 + ['r']
        # self.board[1] = [BLANK_SYMBOL] * 4 + ['r'] + [BLANK_SYMBOL] * 3
        # self.board[2] = [BLANK_SYMBOL, 'r'] * 4
        # self.board[3] = ['r'] + [BLANK_SYMBOL] * 3 + ['r'] + [BLANK_SYMBOL] * 3
        # self.board[4] = [BLANK_SYMBOL] * 5 + ['b'] + [BLANK_SYMBOL] + ['b']
        # self.board[5] = ['R'] + [BLANK_SYMBOL] + ['b'] + [BLANK_SYMBOL] + ['r'] + [BLANK_SYMBOL] + ['b'] + [BLANK_SYMBOL]
        # self.board[6] = [BLANK_SYMBOL] * 3 + ['b'] + [BLANK_SYMBOL] * 3 + ['r']
        # self.board[7] = [BLANK_SYMBOL] * 8

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

        # if (i==5 and j == 0 and x == 3 and y == 2 and symbol == 'R'):
        #     print(down, up, left, right)

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

    def checkWin(self):
        if (not self.getMoves('r') and not self.blue_moves):
            return "blue"

        if (not self.getMoves('b') and self.blue_moves):
            return "red"

        return False
        # if (symbol == RED_SYMBOL or symbol == RED_KING_SYMBOL):
        #     enemy_symbols = [BLUE_SYMBOL, BLUE_KING_SYMBOL]
        # else:
        #     enemy_symbols = [RED_SYMBOL, RED_KING_SYMBOL]
        #
        # if (self.blue_moves and enemy_symbols[0] == BLUE_SYMBOL):
        #     if self.getMoves(enemy_symbols[0]):
        #         return True
        # elif (not self.blue_moves and enemy_symbols[0] == RED_SYMBOL):
        #     if self.getMoves(enemy_symbols[0]):
        #         return True
        #
        # return False

    def move(self, startX, startY, endX, endY, symbol, check=False):
        eatingPiece = False

        if (symbol not in [RED_SYMBOL, RED_KING_SYMBOL, BLUE_SYMBOL, BLUE_KING_SYMBOL]):
            raise Exception("Invalid symbol")

        # if (self.blue_moves and symbol in [RED_SYMBOL, RED_KING_SYMBOL]):
        #     raise Exception("Blue moves!")
        #
        # if (not self.blue_moves and symbol in [BLUE_SYMBOL, BLUE_SYMBOL]):
        #     raise Exception("Red moves!")

        if (self.board[startX][startY] != symbol):
            # print(startX, startY, self.board[startX][startY], symbol)
            raise Exception("Please move a valid piece")

        if (self.board[endX][endY] != BLANK_SYMBOL):
            raise Exception("Please move the piece onto a blank space")

        if (startX < 0 or startX >= BOARD_SIZE or startY < 0 or startY >= BOARD_SIZE):
            raise Exception("Invalid start coordinates")

        if (endX < 0 or endX >= BOARD_SIZE or endY < 0 or endY >= BOARD_SIZE):
            raise Exception("Invalid end coordinates")

        if (symbol == RED_SYMBOL):
            # print(self.canEatPieces(symbol, up=True), self.goingThroughPiece(startX, startY, endX, endY, symbol))
            # check if must eat piece and not eating
            if (self.canEatPieces(symbol, down=True) and not self.goingThroughPiece(startX, startY, endX, endY, symbol)):
                raise Exception("Must eat piece 1" + symbol)

            if (endX != startX + 1 or not(endY == startY + 1 or endY == startY - 1)):
                # check if eating a piece
                if (endX != startX + 2):
                    raise Exception("Illegal move")

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
            # print(self.canEatPieces(symbol, up=True), self.goingThroughPiece(startX, startY, endX, endY, symbol))
            if (self.canEatPieces(symbol, up=True) and not self.goingThroughPiece(startX, startY, endX, endY, symbol)):
                raise Exception("Must eat piece 2", symbol)

            if (endX != startX - 1 or  not(endY == startY + 1 or endY == startY - 1)):
                # check if eating a piece
                if (endX != startX - 2):
                    raise Exception("Illegal move")

                if not(self.canEatPieceUp(startX, startY, symbol)):
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
            # print(self.canEatPieces(symbol, up=True), self.goingThroughPiece(startX, startY, endX, endY, symbol))
            if (self.canEatPieces(symbol, down=True, up=True) and not self.goingThroughPiece(startX, startY, endX, endY, symbol)):
                raise Exception("Must eat piece 3", symbol)

            if (not(endX == startX + 1 or endX == startX - 1) or not(endY == startY + 1 or endY == startY - 1)):
                # check if eating a piece
                if not(endX == startX + 2 or endX == startX - 2):
                    raise Exception("Illegal move")

                if not(self.canEatPieceUp(startX, startY, symbol) or self.canEatPieceDown(startX, startY, symbol)):
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

        new_board = copy.deepcopy(self.board)

        new_board[endX][endY] = new_board[startX][startY]
        new_board[startX][startY] = BLANK_SYMBOL

        if (eatingPiece):
            new_board[eatX][eatY] = BLANK_SYMBOL

        # red upgrade
        if (symbol == RED_SYMBOL and endX == BOARD_SIZE - 1):
            new_board[endX][endY] = RED_KING_SYMBOL

        # blue upgrade
        if (symbol == BLUE_SYMBOL and endX == 0):
            new_board[endX][endY] = BLUE_KING_SYMBOL

        if (not check):
            self.board = new_board

            # check if turn is over
            if not eatingPiece:
                self.blue_moves = not self.blue_moves
            else:
                if (symbol == RED_SYMBOL and not self.canEatPieceDown(endX, endY, symbol)):
                    self.blue_moves = True
                elif (symbol == RED_KING_SYMBOL and not (self.canEatPieceDown(endX, endY, symbol) or self.canEatPieceUp(endX, endY, symbol))):
                    self.blue_moves = True
                elif (symbol == BLUE_SYMBOL and not self.canEatPieceUp(endX, endY, symbol)):
                    self.blue_moves = False
                elif (symbol == BLUE_KING_SYMBOL and not (self.canEatPieceDown(endX, endY, symbol) or self.canEatPieceUp(endX, endY, symbol))):
                    self.blue_moves = False
        else:
            new_state = Board(self.humanPlayer)
            new_state.board = new_board
            new_state.blue_moves = self.blue_moves

            # check if turn is over
            if not eatingPiece:
                new_state.blue_moves = not new_state.blue_moves
            else:
                if (symbol == RED_SYMBOL and not new_state.canEatPieceDown(endX, endY, symbol)):
                    new_state.blue_moves = True
                elif (symbol == RED_KING_SYMBOL and not (new_state.canEatPieceDown(endX, endY, symbol) or new_state.canEatPieceUp(endX, endY, symbol))):
                    new_state.blue_moves = True
                elif (symbol == BLUE_SYMBOL and not new_state.canEatPieceUp(endX, endY, symbol)):
                    new_state.blue_moves = False
                elif (symbol == BLUE_KING_SYMBOL and not (new_state.canEatPieceDown(endX, endY, symbol) or new_state.canEatPieceUp(endX, endY, symbol))):
                    new_state.blue_moves = False

            return new_state



    def getMoves(self, symbol):
        moves = []

        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                aux = self.board[i][j]
                if (aux.lower() == symbol):
                    positions = [(i - 2, j - 2), (i - 1, j - 1), (i - 2, j + 2), (i - 1, j + 1),
                                 (i + 2, j - 2), (i + 1, j - 1), (i + 2, j + 2), (i + 1, j + 1)]

                    for position in positions:
                        try:
                            if (aux.isupper()):
                                new_move = self.move(i, j, position[0], position[1], symbol.upper(), check=True)
                            else:
                                new_move = self.move(i, j, position[0], position[1], symbol, check=True)

                            moves.append(new_move)
                        except Exception as E:
                            continue

        return moves

    # counts pieces
    def scoreHeuristic(self, player):
        score = 0
        if (player == 'blue'):
            for i in range(BOARD_SIZE):
                for j in range(BOARD_SIZE):
                    if (self.board[i][j] == 'b'):
                        score += 3
                    elif (self.board[i][j] == 'B'):
                        score += 9
        else:
            for i in range(BOARD_SIZE):
                for j in range(BOARD_SIZE):
                    if (self.board[i][j] == 'r'):
                        score += 3
                    elif (self.board[i][j] == 'R'):
                        score += 9

        return score

    def calculateScore(self, depth):
        winner = self.checkWin()

        if winner == 'blue':
            return (99 + depth)
        elif winner == 'red':
            return (-99 - depth)
        else:
            return self.scoreHeuristic('blue') - self.scoreHeuristic('red')

    def printMoves(self, symbol):
        moves = self.getMoves(symbol)

        for move in moves:
            print("   0 1 2 3 4 5 6 7")
            print("   ---------------")

            # print board
            for i in range(BOARD_SIZE):

                # print horizontal guide
                print(i, "| ", sep='', end='')

                for j in range(BOARD_SIZE):
                    print(move.board[i][j], end=' ')
                print()


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


def console(board):
    current_state = ai.State(board, board.aiPlayer, 5)

    while(True):
        board.print()

        if ((board.humanPlayer == 'blue' and board.blue_moves) or (board.humanPlayer == 'red' and not board.blue_moves)):
            choice = input("Type quit if you want to quit, else just enter: ")
            if choice == "quit":
                break

            print("BLUE" if board.blue_moves else "RED", "new move (i, j) -> (x, y)")

            try:
                i = int(input("i: "))
                j = int(input("j: "))
                x = int(input("x: "))
                y = int(input("y: "))

            except Exception as E:
                print("Invalid format, try again\n")
                continue

            try:
                board.move(i, j, x, y, board.board[i][j])
            except Exception as E:
                print("Error:", E)
        else:
            current_state = ai.min_max(current_state)
            # current_state.choice.board.print()
            board.board = current_state.choice.board.board
            # print(current_state.choice.player)
            board.blue_moves = current_state.choice.board.blue_moves
