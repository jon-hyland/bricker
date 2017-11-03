class Brick:
    shape_num = 0
    width = 0
    height = 0
    grid = 0
    color = (0, 0, 0)
    x = 0
    y = 0
    top_space = 0
    bottom_space = 0
    # left_space = 0
    # right_space = 0

    def __init__(self, shape_num):
        self.shape_num = shape_num
        if shape_num == 1:
            self.width = 4
            self.height = 4
            self.grid = [[0 for x in range(self.height)] for y in range(self.width)]
            self.grid[0][2] = 1
            self.grid[1][2] = 1
            self.grid[2][2] = 1
            self.grid[3][2] = 1
            self.color = 109, 245, 255
        elif shape_num == 2:
            self.width = 3
            self.height = 3
            self.grid = [[0 for x in range(self.height)] for y in range(self.width)]
            self.grid[0][1] = 1
            self.grid[0][2] = 1
            self.grid[1][2] = 1
            self.grid[2][2] = 1
            self.color = 10, 67, 201
        elif shape_num == 3:
            self.width = 3
            self.height = 3
            self.grid = [[0 for x in range(self.height)] for y in range(self.width)]
            self.grid[2][1] = 1
            self.grid[0][2] = 1
            self.grid[1][2] = 1
            self.grid[2][2] = 1
            self.color = 255, 157, 0
        elif shape_num == 4:
            self.width = 2
            self.height = 2
            self.grid = [[0 for x in range(self.height)] for y in range(self.width)]
            self.grid[0][0] = 1
            self.grid[0][1] = 1
            self.grid[1][0] = 1
            self.grid[1][1] = 1
            self.color = 255, 233, 0
        elif shape_num == 5:
            self.width = 3
            self.height = 3
            self.grid = [[0 for x in range(self.height)] for y in range(self.width)]
            self.grid[1][0] = 1
            self.grid[2][0] = 1
            self.grid[0][1] = 1
            self.grid[1][1] = 1
            self.color = 66, 201, 4
        elif shape_num == 6:
            self.width = 3
            self.height = 3
            self.grid = [[0 for x in range(self.height)] for y in range(self.width)]
            self.grid[1][1] = 1
            self.grid[0][2] = 1
            self.grid[1][2] = 1
            self.grid[2][2] = 1
            self.color = 129, 6, 206
        elif shape_num == 7:
            self.width = 3
            self.height = 3
            self.grid = [[0 for x in range(self.height)] for y in range(self.width)]
            self.grid[0][0] = 1
            self.grid[1][0] = 1
            self.grid[1][1] = 1
            self.grid[2][1] = 1
            self.color = 229, 0, 0

        self.top_space = 0
        for y in range(0, self.height):
            empty = True
            for x in range(0, self.width):
                if self.grid[x][y] == 1:
                    empty = False
            if empty:
                self.top_space += 1
            else:
                break

        self.bottom_space = 0
        for y in reversed(range(0, self.height)):
            empty = True
            for x in range(0, self.width):
                if self.grid[x][y] == 1:
                    empty = False
            if empty:
                self.bottom_space += 1
            else:
                break

        self.x = int((12 - self.width) / 2)
        self.y = 1 - self.top_space

    def collision(self, matrix):
        for x in range(0, self.width):
            for y in range(0, self.height):
                if (self.grid[x][y] == 1) and (matrix[x + self.x][y + self.y] == 1):
                    return True
        return False

    def move_left(self, matrix):
        self.x -= 1
        if self.collision(matrix):
            self.x += 1

    def move_right(self, matrix):
        self.x += 1
        if self.collision(matrix):
            self.x -= 1

    def move_down(self, matrix):
        self.y += 1
        if self.collision(matrix):
            self.y -= 1

    def rotate(self, matrix):
        new_grid = [[0 for x in range(self.width)] for y in range(self.height)]
        for x1 in range(0, self.width):
            for y1 in range(0, self.height):
                x2 = -y1 + (self.height - 1)
                y2 = x1
                new_grid[x2][y2] = self.grid[x1][y1]
        self.grid = new_grid

        steps = 0
        while self.collision(matrix):
            self.y += 1
            steps += 1
            if steps >= 3:
                self.y -= 3
                break

        steps = 0
        while self.collision(matrix):
            self.y -= 1
            steps += 1
            if steps >= 3:
                self.y += 3
                break

        steps = 0
        while self.collision(matrix):
            self.x -= 1
            steps += 1
            if steps >= 3:
                self.x += 3
                break

        steps = 0
        while self.collision(matrix):
            self.x += 1
            steps += 1
            if steps >= 3:
                self.x -= 3
                break

