import heapq as hq
from copy import deepcopy

class eightPuzzle():
    def __init__(self, init):
        self.final = (1,2,3,8,0,4,7,6,5)
        self.init = init
        self.visited = set()
        self.unvisited = []
        self.path = {}
        self.coords = {
            1: (0, 0),
            2: (1, 0),
            3: (2, 0),
            4: (2, 1),
            5: (2, 2),
            6: (1, 2),
            7: (0, 2),
            8: (0, 1),
        }
        h = self.heuristic(init)
        hq.heappush(self.unvisited, (h, 0, init))
        self.path[init] = (h, 0, None)
        self.display(init)

    def display(self, board):
        for i in range(3):
            print(str(board[i*3+0]) + " " + str(board[i*3+1]) + " " + str(board[i*3+2]))

    def printResult(self):
        moves, curr = 0, self.final
        while curr != self.init:
            moves += 1
            curr = self.path[curr][2]
        print("\n" + str(moves) + " moves")
        # print("visited: " + str(len(self.visited)))
        # print("unvisited: " + str(len(self.unvisited)))
        print("----------------------------------")

    def heuristic(self, board):
        h = 0
        for index, value in enumerate(board):
            if value != 0:
                x, y = index % 3, int(index / 3)
                h += abs(x - self.coords[value][0]) + abs(y - self.coords[value][1])
        return h

    def moves(self, board):
        moves = []
        curr = deepcopy(board)
        index = board.index(0)
        x, y = index % 3, int(index / 3)
        if x > 0 : # left
            curr[index - 1], curr[index] = curr[index], curr[index - 1]
            moves.append(tuple(curr))
            curr = deepcopy(board)
        if x < 2: # right
            curr[index + 1], curr[index] = curr[index], curr[index + 1]
            moves.append(tuple(curr))
            curr = deepcopy(board)
        if y > 0: # up
            curr[index - 3], curr[index] = curr[index], curr[index - 3]
            moves.append(tuple(curr))
            curr = deepcopy(board)
        if y < 2: # down
            curr[index + 3], curr[index] = curr[index], curr[index + 3]
            moves.append(tuple(curr))
        return moves

    def play(self):
        g = 0
        while len(self.unvisited) != 0:
            curr = hq.heappop(self.unvisited)
            nextMoves = self.moves(list(curr[2]))
            g += 1
            for move in nextMoves:
                if self.heuristic(move) == 0:
                    self.path[move] = (g, g, curr[2])
                    self.printResult()
                    return
                else:
                    h = self.heuristic(move)
                    f = g + h
                try:
                    index = self.unvisited.index((self.path[move][0], self.path[move][1], move))
                except:
                    pass
                else:
                    if self.unvisited[index][0] < f:
                        continue
                if move in self.visited and self.path[move][0] < f:
                    continue
                else:
                    hq.heappush(self.unvisited, (f, g, move))
                    self.path[move] = (f, g, curr[2])
            self.visited.add(curr[2])

file = open('config.txt', 'r')
config = 0
while 1:
    init = file.readline()
    if not init:
        break
    init = [int(s) for s in init.split(' ')]
    config += 1
    print("Initial configuration " + str(config) + ":")
    puzzle = eightPuzzle(tuple(init))
    puzzle.play()
    ignore = file.readline()

file.close()
