import heapq

class SlidingTile():
    def __init__(self):
        self.board = ('B','B','B',' ','W','W','W')
        self.visited = [] # board
        self.unvisited = [] # (g(n)+h(n), g(n), board)
        self.shortestPath = {} # board: (g(n)+h(n), g(n), parent board)
        heapq.heappush(self.unvisited, (9, 0, self.board))

    def printBoard(self, state):
        print("|"+state[0]+"|"+state[1]+"|"+state[2]+"|"+state[3]+"|"+state[4]+"|"+state[5]+"|"+state[6]+"|")
        return

    def printPath(self, lastBoard):
        steps = []
        curr = lastBoard
        cost = self.shortestPath[lastBoard][0]
        depth = 0

        while curr != self.board:
            steps.insert(0, curr)
            depth += 1
            curr = self.shortestPath[curr][2]
        steps.insert(0, self.board)
        for step in steps:
            self.printBoard(step)
        print("\nThe puzzle was completed with a cost of: " + str(cost) + " and a depth of: " + str(depth))

    def moveRight(self, curr):
        index = curr.index(" ")
        currCopy = curr.copy()
        boards = []
        if index+1 <= 6:
            currCopy[index], currCopy[index+1] = currCopy[index+1], currCopy[index]
            boards.append((tuple(currCopy), 1))
            currCopy = curr.copy()
        if index+2 <= 6:
            currCopy[index], currCopy[index+2] = currCopy[index+2], currCopy[index]
            boards.append((tuple(currCopy), 1))
            currCopy = curr.copy()
        if index+3 <= 6:
            currCopy[index], currCopy[index+3] = currCopy[index+3], currCopy[index]
            boards.append((tuple(currCopy), 2))

        return boards # (cost from parent board, board)

    def moveLeft(self, curr):
        index = curr.index(" ")
        currCopy = curr.copy()
        boards = []
        if index -1 >= 0:
            currCopy[index], currCopy[index - 1] = currCopy[index - 1], currCopy[index]
            boards.append((tuple(currCopy), 1))
            currCopy = curr.copy()
        if index - 2 >= 0:
            currCopy[index], currCopy[index - 2] = currCopy[index - 2], currCopy[index]
            boards.append((tuple(currCopy), 1))
            currCopy = curr.copy()
        if index - 3 >= 0:
            currCopy[index], currCopy[index - 3] = currCopy[index - 3], currCopy[index]
            boards.append((tuple(currCopy), 2))

        return boards # (board, cost from parent board)

    def heuristic(self, board):
        h = 0
        count = 0
        for n in board:
            if n == "B":
                count+=1
            elif n == "W":
                h += count
        return h


    def play(self):
        while len(self.unvisited) != 0:
            curr = heapq.heappop(self.unvisited)
            if self.heuristic(curr[2]) == 0:
                self.printPath(curr[2])
                return
                # c) generate q's successors and set their parents to q
            nextMoves = self.moveRight(list(curr[2])) + self.moveLeft(list(curr[2]))
            # d) for each successor
            for move in nextMoves:
                if move[0] not in self.visited:
                    h = self.heuristic(move[0])
                    g = move[1] + curr[1]
                    f = g + h
                    if move[0] not in self.shortestPath:
                        heapq.heappush(self.unvisited, (f, g, move[0]))
                        self.shortestPath[move[0]] = (f, g, curr[2])
                    else:
                        index = self.unvisited.index((self.shortestPath[move[0]][0], self.shortestPath[move[0]][1], move[0]))
                        if self.unvisited[index][0] > f or self.unvisited[index][1] > g:
                            self.unvisited[index] = (f, g, move[0])
                            self.shortestPath[move[0]] = (f, g, curr[2])
                            heapq.heapify(self.unvisited)
            self.visited.append(curr[2])

puzzle = SlidingTile()
puzzle.play()