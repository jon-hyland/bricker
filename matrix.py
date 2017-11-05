class Matrix:
    width = 12
    height = 22
    matrix = None
    color = None

    def __init__(self):
        self.matrix = [[0 for x in range(self.height)] for y in range(self.width)]
        self.color = [[(0, 0, 0) for x in range(self.height)] for y in range(self.width)]
        for x in range(0, 12):
            self.matrix[x][0] = 1
            self.matrix[x][21] = 1
        for y in range(0, 22):
            self.matrix[0][y] = 1
            self.matrix[11][y] = 1

    def add_brick(self, brick):
        for x in range(0, brick.width):
            for y in range(0, brick.height):
                if brick.grid[x][y] == 1:
                    self.matrix[x + brick.x][y + brick.y] = 1
                    self.color[x + brick.x][y + brick.y] = brick.color
