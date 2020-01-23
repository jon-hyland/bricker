from time import perf_counter
from color import Color


class Brick:
    """Represents a live, moving brick that has not yet joined the static game matrix.
    It will do so once it's hit bottom and come to rest."""

    def __init__(self, shape_num: int) -> None:
        """Class constructor.  Creates one of seven basic shapes."""
        self.__shape_num: int = shape_num
        if shape_num == 1:
            self.width = 4
            self.height = 4
            self.grid = [[0 for x in range(self.height)] for y in range(self.width)]
            self.grid[0][2] = 1
            self.grid[1][2] = 1
            self.grid[2][2] = 1
            self.grid[3][2] = 1
            self.color = Color.SilverPink
        elif shape_num == 2:
            self.width = 3
            self.height = 3
            self.grid = [[0 for x in range(self.height)] for y in range(self.width)]
            self.grid[0][1] = 1
            self.grid[0][2] = 1
            self.grid[1][2] = 1
            self.grid[2][2] = 1
            self.color = Color.TuftsBlue
        elif shape_num == 3:
            self.width = 3
            self.height = 3
            self.grid = [[0 for x in range(self.height)] for y in range(self.width)]
            self.grid[2][1] = 1
            self.grid[0][2] = 1
            self.grid[1][2] = 1
            self.grid[2][2] = 1
            self.color = Color.ChromeYellow
        elif shape_num == 4:
            self.width = 2
            self.height = 2
            self.grid = [[0 for x in range(self.height)] for y in range(self.width)]
            self.grid[0][0] = 1
            self.grid[0][1] = 1
            self.grid[1][0] = 1
            self.grid[1][1] = 1
            self.color = Color.Independence
        elif shape_num == 5:
            self.width = 3
            self.height = 3
            self.grid = [[0 for x in range(self.height)] for y in range(self.width)]
            self.grid[1][0] = 1
            self.grid[2][0] = 1
            self.grid[0][1] = 1
            self.grid[1][1] = 1
            self.color = Color.ForestGreen
        elif shape_num == 6:
            self.width = 3
            self.height = 3
            self.grid = [[0 for x in range(self.height)] for y in range(self.width)]
            self.grid[1][1] = 1
            self.grid[0][2] = 1
            self.grid[1][2] = 1
            self.grid[2][2] = 1
            self.color = Color.Byzantine
        elif shape_num == 7:
            self.width = 3
            self.height = 3
            self.grid = [[0 for x in range(self.height)] for y in range(self.width)]
            self.grid[0][0] = 1
            self.grid[1][0] = 1
            self.grid[1][1] = 1
            self.grid[2][1] = 1
            self.color = Color.Coquelicot
        self.top_space = self.get_top_space()
        self.bottom_space = self.get_bottom_space()
        self.x = int((12 - self.width) / 2)
        self.y = 1 - self.top_space
        self.last_drop_time = perf_counter()

    def get_top_space(self):
        """Returns space above brick."""
        top_space = 0
        for y in range(0, self.height):
            empty = True
            for x in range(0, self.width):
                if self.grid[x][y] == 1:
                    empty = False
            if empty:
                top_space += 1
            else:
                break
        return top_space

    def get_bottom_space(self):
        """Returns space below brick."""
        bottom_space = 0
        for y in reversed(range(0, self.height)):
            empty = True
            for x in range(0, self.width):
                if self.grid[x][y] == 1:
                    empty = False
            if empty:
                bottom_space += 1
            else:
                break
        return bottom_space

    def collision(self, matrix):
        """Returns true on brick collision."""
        for x in range(0, self.width):
            for y in range(0, self.height):
                matrix_x = x + self.x
                matrix_y = y + self.y
                if (self.grid[x][y] == 1) and (matrix[matrix_x][matrix_y] == 1):
                    return True
        return False

    def move_left(self, matrix):
        """Moves brick left, prevents collision."""
        self.x -= 1
        if self.collision(matrix):
            self.x += 1

    def move_right(self, matrix):
        """Moves brick right, prevents collision."""
        self.x += 1
        if self.collision(matrix):
            self.x -= 1

    def move_down(self, matrix):
        """Moves brick down, prevents collision."""
        self.last_drop_time = perf_counter()
        self.y += 1
        if self.collision(matrix):
            self.y -= 1
            return True
        return False

    def is_drop_time(self, interval):
        """Returns true if its time to drop brick (gravity)."""
        now = perf_counter()
        elapsed = now - self.last_drop_time
        drop_time = elapsed >= interval
        return drop_time

    def rotate(self, matrix):
        """Rotates brick."""

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
