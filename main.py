class Field:
    def __init__(self, x, y, owned):
        self.x = x
        self.y = y
        self.owned = owned


class Board:
    def __init__(self, fields):
        self.fields = fields


class Player:
    def __init__(self, name):
        self.name = name

size = 3
winSize = 3
none = Player("_")
ai = Player("x")
human = Player("o")


def horizontalWin(board, player):
    for xx in range(size):
        winningStrike = 0
        for yy in range(size):
            if board.fields[xx][yy].owned == player:
                winningStrike += 1
            else:
                winningStrike = 0

            if winningStrike >= winSize:
                return True
    return False


def verticalWin(board, player):
    for yy in range(size):
        winningStrike = 0
        for xx in range(size):
            if board.fields[xx][yy].owned == player:
                winningStrike += 1
            else:
                winningStrike = 0

            if winningStrike >= winSize:
                return True
    return False


def diagonal_1_1lWin(board, player):
    for xx in range(size):
        winningStrike = 0
        for yy in range(size):
            actualXx = xx + yy
            if actualXx < size:
                if board.fields[actualXx][yy].owned == player:
                    winningStrike += 1
                else:
                    winningStrike = 0

                if winningStrike >= winSize:
                    return True
    return False


def diagonal_1_2lWin(board, player):
    for xx in range(size):
        winningStrike = 0
        for yy in range(size):
            actualYy = xx + yy
            if actualYy < size:
                if board.fields[xx][actualYy].owned == player:
                    winningStrike += 1
                else:
                    winningStrike = 0

                if winningStrike >= winSize:
                    return True
    return False


def diagonal_2_1lWin(board, player):
    for xx in range(size):
        winningStrike = 0
        for yy in range(size):
            actualXx = xx - yy
            if actualXx >= 0:
                if board.fields[actualXx][yy].owned == player:
                    winningStrike += 1
                else:
                    winningStrike = 0

                if winningStrike >= winSize:
                    return True
    return False


def diagonal_2_2lWin(board, player):
    for xx in range(size):
        winningStrike = 0
        for yy in range(size):
            actualYy = yy - xx
            if actualYy > 0:
                if board.fields[xx][actualYy].owned == player:
                    winningStrike += 1
                else:
                    winningStrike = 0

                if winningStrike >= winSize:
                    return True
    return False


def win(board, player):
    return horizontalWin(board, player) or verticalWin(board, player) or diagonal_1_1lWin(board, player) or diagonal_1_2lWin(board, player) or diagonal_2_1lWin(board, player) or diagonal_2_2lWin(board, player)

def initialBoard():
    fields = []
    for xx in range(size):
        innerFields = []
        for yy in range(size):
            field = Field(xx, yy, none)
            innerFields.append(field)
        fields.append(innerFields)
    return Board(fields)


def emptyFields(board):
    result = []
    for xx in range(size):
        for yy in range(size):
            if board.fields[xx][yy].owned == none:
                result.append(board.fields[xx][yy])
    return result


def makeMove(board, player, fieldToAdd):
    fields = []
    for xx in range(size):
        innerFields = []
        for yy in range(size):
            field = Field(xx, yy, board.fields[xx][yy].owned)
            innerFields.append(field)
        fields.append(innerFields)
    result = Board(fields)

    result.fields[fieldToAdd.x][fieldToAdd.y].owned = player
    return result


def isEnd(board, player1, player2):
    if win(board, player1):
        return True
    elif win(board, player2):
        return True
    elif not emptyFields(board):
        return True
    else:
        return False

def evaluate(board, player, enemy):
    if win(board, player):
        return 1
    elif win(board, enemy):
        return -1
    else:
        return 0


def min_minimax(board, alfa, beta):
    moves = emptyFields(board)
    bestMove = None
    bestEval = 2
    for curMove in moves:
        appliedMove = makeMove(board, human, curMove)
        if isEnd(appliedMove, ai, human):
            evaluated = evaluate(appliedMove, ai, human)
            if evaluated < bestEval:
                bestEval = evaluated
                bestMove = curMove

                if bestEval <= alfa:
                    return (curMove, evaluated)

        else:
            (__, evaluated) = max_minimax(appliedMove, alfa, min(beta, bestEval))
            if evaluated < bestEval:
                bestEval = evaluated
                bestMove = curMove

                if bestEval <= alfa:
                    return (curMove, evaluated)

    return (bestMove, bestEval)

def max_minimax(board, alfa, beta):
    moves = emptyFields(board)
    bestMove = None
    bestEval = -2
    for curMove in moves:
        appliedMove = makeMove(board, ai, curMove)
        if isEnd(appliedMove, ai, human):
            evaluated = evaluate(appliedMove, ai, human)
            if evaluated > bestEval:
                bestEval = evaluated
                bestMove = curMove

                if bestEval >= beta:
                    return (curMove, evaluated)

        else:
            (__, evaluated) = min_minimax(appliedMove, max(alfa, bestEval), beta)

            if evaluated > bestEval:
                bestEval = evaluated
                bestMove = curMove

                if bestEval >= beta:
                    return (curMove, evaluated)

    return (bestMove, bestEval)


def printBoard(board):
    for xx in range(size):
        line = ""
        for yy in range(size):
            line += (board.fields[xx][yy].owned.name+" ")
        print(line)


def validMove(board, x, y):
    return board.fields[x][y].owned == none


def getHumanMove(board):
    print("Your move\n")
    #inverted since that is graphically correct
    y = input("x: ")
    x = input("y: ")
    if not validMove(board, x, y):
        print("invalid move, again")
        return getHumanMove(board)
    else:
        return Field(x, y, human)


def main():
    board = initialBoard()

    while not isEnd(board, ai, human):
        (move, evaluated) = max_minimax(board, -1, 1)
        board = makeMove(board, ai, move)
        printBoard(board)
        if isEnd(board, ai, human):
            break

        humanMove = getHumanMove(board)
        board = makeMove(board, human, humanMove)

    print("\ngame result:\n")
    printBoard(board)
    won = win(board, ai)
    lost = win(board, human)
    if won:
        print("you lost")
    elif lost:
        print("you won!")
    else:
        print("drawn")

    print("end of game")

if __name__ == "__main__":
    main()

