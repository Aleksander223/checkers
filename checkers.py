import copy
import ai
import time


# constants
BOARD_SIZE = 8
RED_SYMBOL = 'r'
BLUE_SYMBOL = 'b'
RED_KING_SYMBOL = 'R'
BLUE_KING_SYMBOL = 'B'
BLANK_SYMBOL = '.'

class Board:
    DRAW_COUNTER = 0 # turns without attacking
    DRAW_MOVES = 20

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
                aux = self.board[i][j]
                if (aux.lower() == symbol or aux.upper() == symbol):
                    if (symbol.isupper() and self.board[i][j].isupper()):
                        pieces += (self.canEatPieceDown(i, j, symbol))
                        pieces += (self.canEatPieceUp(i, j, symbol))

                    elif (symbol.islower() and self.board[i][j].islower()):
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

    def checkWin(self):
        if (Board.DRAW_COUNTER >= Board.DRAW_MOVES):
            return "draw"

        if (not self.getMoves('r') and not self.blue_moves):
            return "blue"

        if (not self.getMoves('b') and self.blue_moves):
            return "red"

        return False

    def move(self, startX, startY, endX, endY, symbol, check=False):
        eatingPiece = False

        if (symbol not in [RED_SYMBOL, RED_KING_SYMBOL, BLUE_SYMBOL, BLUE_KING_SYMBOL]):
            raise Exception("Invalid symbol")

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
                raise Exception("Must eat piece")

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
                raise Exception("Must eat piece")

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
                raise Exception("Must eat piece")

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

                Board.DRAW_COUNTER += 1
            else:
                Board.DRAW_COUNTER = 0

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

    # counts pieces with weight
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

    # only count pieces
    def scoreHeuristic2(self, player):
        score = 0
        if (player == 'blue'):
            for i in range(BOARD_SIZE):
                for j in range(BOARD_SIZE):
                    if (self.board[i][j] == 'b'):
                        score += 1
                    elif (self.board[i][j] == 'B'):
                        score += 1
        else:
            for i in range(BOARD_SIZE):
                for j in range(BOARD_SIZE):
                    if (self.board[i][j] == 'r'):
                        score += 1
                    elif (self.board[i][j] == 'R'):
                        score += 1

        return score

    def calculateScore(self, depth):
        winner = self.checkWin()

        if winner == 'blue':
            return (99 + depth)
        elif winner == 'red':
            return (-99 - depth)
        elif winner == 'draw':
            return 0
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



def console(board, algorithm, maximum_depth):
    current_state = ai.State(board, board.aiPlayer, maximum_depth)
    timerStarted = False


    while(True):
        board.print()

        if (board.checkWin()):
            if (board.checkWin() == 'draw'):
                print("Draw!")
                print("Blue score:", board.scoreHeuristic("blue"))
                print("Red score:", board.scoreHeuristic("red"))
                break

            if (board.checkWin() == 'red'):
                print("Red wins!")
                print("Blue score:", board.scoreHeuristic("blue"))
                print("Red score:", board.scoreHeuristic("red"))
                break

            if (board.checkWin() == 'blue'):
                print("Blue wins!")
                print("Blue score:", board.scoreHeuristic("blue"))
                print("Red score:", board.scoreHeuristic("red"))
                break

        if ((board.humanPlayer == 'blue' and board.blue_moves) or (board.humanPlayer == 'red' and not board.blue_moves)):
            choice = input("Type quit if you want to quit, else just enter: ")
            if choice == "quit":
                print("Blue score:", board.scoreHeuristic("blue"))
                print("Red score:", board.scoreHeuristic("red"))
                break


            print("BLUE" if board.blue_moves else "RED", "moves")
            print("new move (i, j) -> (x, y)")
            if (not timerStarted):
                timerStarted = True
                t_before = int(round(time.time() * 1000))

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

            t_after = int(round(time.time() * 1000))
            timerStarted = False

            print("Human thought for:", str(t_after - t_before), "miliseconds")
        else:
            print("BLUE" if board.blue_moves else "RED", "moves")
            t_before = int(round(time.time() * 1000))

            if (algorithm == 1):
                current_state = ai.min_max(current_state)
            else:
                current_state = ai.ab_pruning(-1000, +1000, current_state)

            t_after = int(round(time.time() * 1000))

            print("AI thought for:", str(t_after - t_before), "miliseconds")

            board.board = current_state.choice.board.board
            board.blue_moves = current_state.choice.board.blue_moves
