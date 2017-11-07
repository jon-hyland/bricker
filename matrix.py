from random import randint
from brick import Brick
from stats import Stats


class Matrix:
    """ Stores the 10x20 game matrix.  Contains game logic. """

    def __init__(self, draw):
        """ Class constructor. """
        self.draw = draw
        self.width = 12     # 10 visible slots, plus border for collision detection
        self.height = 22    # 20 visible slots, plus border for collision detection
        self.matrix = [[0 for x in range(self.height)] for y in range(self.width)]
        self.color = [[(0, 0, 0) for x in range(self.height)] for y in range(self.width)]
        for x in range(0, 12):
            self.matrix[x][0] = 1
            self.matrix[x][21] = 1
        for y in range(0, 22):
            self.matrix[0][y] = 1
            self.matrix[11][y] = 1
        self.stats = Stats()
        self.brick = None
        self.spawn_brick()

    def spawn_brick(self):
        """ Spawns a new (random) brick. """
        shape_num = randint(1, 7)
        self.brick = Brick(shape_num)

    def add_brick_to_matrix(self):
        """ Moves resting brick to matrix. """
        if self.brick is not None:
            for x in range(0, self.brick.width):
                for y in range(0, self.brick.height):
                    if self.brick.grid[x][y] == 1:
                        self.matrix[x + self.brick.x][y + self.brick.y] = 1
                        self.color[x + self.brick.x][y + self.brick.y] = self.brick.color
        self.brick = None

    def move_brick_left(self):
        """ Moves brick to the left. """
        if self.brick is not None:
            self.brick.move_left(self.matrix)

    def move_brick_right(self):
        """ Moves brick to the right. """
        if self.brick is not None:
            self.brick.move_right(self.matrix)

    def move_brick_down(self):
        """ Moves brick to down. """
        if self.brick is not None:
            return self.brick.move_down(self.matrix)
        return False

    def rotate_brick(self):
        """ Rotates brick. """
        if self.brick is not None:
            self.brick.rotate(self.matrix)

    def brick_hit(self):
        """ Executed when brick hits bottom and comes to rest. """
        self.add_brick_to_matrix()
        rows_to_erase = self.identify_solid_rows()
        if len(rows_to_erase) > 0:
            self.erase_filled_rows(rows_to_erase)
            self.stats.score += len(rows_to_erase) ^ 2
            self.drop_grid()
            self.draw.event_pump()
            self.draw.draw_frame(self)
        self.spawn_brick()

    def identify_solid_rows(self):
        """ Checks matrix for solid rows, returns list of rows (to erase). """
        rows_to_erase = []
        for y in range(1, 21):
            solid = True
            for x in range(1, 11):
                if self.matrix[x][y] != 1:
                    solid = False
            if solid:
                rows_to_erase.append(y)
        return rows_to_erase

    def is_drop_time(self, interval):
        """ Returns true if it's time for brick to drop (by timer). """
        if self.brick is not None:
            return self.brick.is_drop_time(interval)
        return False

    def drop_brick_to_bottom(self):
        """ Animates a brick dropping to bottom of screen, one motion """
        hit = False
        while not hit:
            for i in range(0, 3):
                hit = self.move_brick_down()
                if hit:
                    break
            self.draw.event_pump()
            self.draw.draw_frame(self)
        return hit

    def erase_filled_rows(self, rows_to_erase):
        """ Animates erasure of filled rows. """
        for x in range(1, 11):
            for y in rows_to_erase:
                self.matrix[x][y] = 0
                self.color[x][y] = 0, 0, 0
            if (x % 2) == 0:
                self.draw.event_pump()
                self.draw.draw_frame(self)

    def drop_grid(self):
        """ Drops hanging pieces to resting place. """
        while self.drop_grid_once():
            pass

    def drop_grid_once(self):
        """ Drops hanging pieces, bottom-most row. """
        top_filled_row = 0
        for row in range(1, 21):
            empty = True
            for x in range(1, 11):
                if self.matrix[x][row] == 1:
                    empty = False
                    break
            if not empty:
                top_filled_row = row
                break

        if top_filled_row == 0:
            return False

        bottom_empty_row = 0
        for row in range(20, (top_filled_row - 1), -1):
            empty = True
            for x in range(1, 11):
                if self.matrix[x][row] == 1:
                    empty = False
                    break
            if empty:
                bottom_empty_row = row
                break

        if bottom_empty_row == 0:
            return False

        for y in range(bottom_empty_row, 1, -1):
            for x in range(1, 11):
                self.matrix[x][y] = self.matrix[x][y - 1]
                self.color[x][y] = self.color[x][y - 1]
        for x in range(1, 11):
            self.matrix[x][1] = 0
            self.color[x][1] = 0, 0, 0

        return True
