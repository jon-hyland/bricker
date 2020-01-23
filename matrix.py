from typing import List
from random import randint
from brick import Brick
from game_stats import GameStats
from renderer import Renderer


class Matrix:
    """Stores the 10x20 game matrix.  Contains matrix-related game logic."""

    def __init__(self, renderer: Renderer) -> None:
        """Class constructor."""
        self.__renderer: Renderer = renderer
        self.__width: int = 12     # 10 visible slots, plus border for collision detection
        self.__height: int = 22    # 20 visible slots, plus border for collision detection
        self.__matrix: List[List[int]] = [[0 for x in range(self.__height)] for y in range(self.__width)]
        self.color = [[(0, 0, 0) for x in range(self.__height)] for y in range(self.__width)]
        for x in range(0, 12):
            self.__matrix[x][0] = 1
            self.__matrix[x][21] = 1
        for y in range(0, 22):
            self.__matrix[0][y] = 1
            self.__matrix[11][y] = 1
        self.stats = GameStats()
        self.brick = None
        self.next_brick = None
        self.level_drop_intervals = []
        interval = 2.0
        for _ in range(0, 10):
            interval *= 0.8
            self.level_drop_intervals.append(interval)

    @property
    def width(self) -> int:
        """Returns width of game matrix."""
        return self.__width

    @property
    def height(self) -> int:
        """Returns height of game matrix."""
        return self.__height

    @property
    def matrix(self) -> List[List[int]]:
        """Returns game matrix."""
        return self.__matrix

    def new_game(self):
        """Reset entire game over."""
        self.brick = None
        self.next_brick = None
        self.__matrix = [[0 for x in range(self.__height)] for y in range(self.__width)]
        self.color = [[(0, 0, 0) for x in range(self.__height)] for y in range(self.__width)]
        for x in range(0, 12):
            self.__matrix[x][0] = 1
            self.__matrix[x][21] = 1
        for y in range(0, 22):
            self.__matrix[0][y] = 1
            self.__matrix[11][y] = 1
        self.stats = GameStats()
        self.spawn_brick()

    def spawn_brick(self):
        """Spawns a new (random) brick."""
        if self.next_brick is None:
            shape_num = randint(1, 7)
            self.next_brick = Brick(shape_num)
        self.brick = self.next_brick
        shape_num = randint(1, 7)
        self.next_brick = Brick(shape_num)
        collision = self.brick.collision(self.__matrix)
        return collision

    def add_brick_to_matrix(self):
        """Moves resting brick to matrix."""
        if self.brick is not None:
            for x in range(0, self.brick.width):
                for y in range(0, self.brick.height):
                    if self.brick.grid[x][y] == 1:
                        self.__matrix[x + self.brick.x][y + self.brick.y] = 1
                        self.color[x + self.brick.x][y + self.brick.y] = self.brick.color
        self.brick = None

    def move_brick_left(self):
        """Moves brick to the left."""
        if self.brick is not None:
            self.brick.move_left(self.__matrix)

    def move_brick_right(self):
        """ Moves brick to the right. """
        if self.brick is not None:
            self.brick.move_right(self.__matrix)

    def move_brick_down(self):
        """Moves brick to down."""
        hit = False
        if self.brick is not None:
            hit = self.brick.move_down(self.__matrix)
        if hit:
            self.stats.increment_score(1)
        return hit

    def rotate_brick(self):
        """Rotates brick."""
        if self.brick is not None:
            self.brick.rotate(self.__matrix)

    def brick_hit(self):
        """Executed when brick hits bottom and comes to rest."""
        self.add_brick_to_matrix()
        rows_to_erase = self.identify_solid_rows()
        if len(rows_to_erase) > 0:
            rows = len(rows_to_erase)
            self.stats.add_lines(rows)
            points = 40
            if rows == 2:
                points = 100
            elif rows == 3:
                points = 300
            elif rows == 4:
                points = 1200
            self.stats.increment_score(points)
            self.erase_filled_rows(rows_to_erase)
            self.drop_grid()
            self.__renderer.event_pump()
            self.__renderer.update_frame(self, None)
        collision = self.spawn_brick()
        return collision

    def identify_solid_rows(self):
        """Checks matrix for solid rows, returns list of rows (to erase)."""
        rows_to_erase = []
        for y in range(1, 21):
            solid = True
            for x in range(1, 11):
                if self.__matrix[x][y] != 1:
                    solid = False
            if solid:
                rows_to_erase.append(y)
        return rows_to_erase

    def is_drop_time(self):
        """Returns true if it's time for brick to drop (by timer)."""
        if self.brick is not None:
            drop_interval = self.level_drop_intervals[self.stats.level - 1]
            return self.brick.is_drop_time(drop_interval)
        return False

    def drop_brick_to_bottom(self):
        """Animates a brick dropping to bottom of screen."""
        hit = False
        while not hit:
            self.__renderer.clock.tick(30)
            for _ in range(0, 3):
                hit = self.move_brick_down()
                if hit:
                    break
            self.__renderer.event_pump()
            self.__renderer.update_frame(self, None)
        self.stats.increment_score(2)
        return True

    def erase_filled_rows(self, rows_to_erase):
        """Animates erasure of filled rows."""
        for x in range(1, 11):
            for y in rows_to_erase:
                self.__matrix[x][y] = 0
                self.color[x][y] = 0, 0, 0
            if (x % 2) == 0:
                self.__renderer.event_pump()
                self.__renderer.update_frame(self, None)

    def drop_grid(self):
        """Drops hanging pieces to resting place."""
        while self.drop_grid_once():
            pass

    def drop_grid_once(self):
        """Drops hanging pieces, bottom-most row."""
        top_filled_row = 0
        for row in range(1, 21):
            empty = True
            for x in range(1, 11):
                if self.__matrix[x][row] == 1:
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
                if self.__matrix[x][row] == 1:
                    empty = False
                    break
            if empty:
                bottom_empty_row = row
                break
        if bottom_empty_row == 0:
            return False
        for y in range(bottom_empty_row, 1, -1):
            for x in range(1, 11):
                self.__matrix[x][y] = self.__matrix[x][y - 1]
                self.color[x][y] = self.color[x][y - 1]
        for x in range(1, 11):
            self.__matrix[x][1] = 0
            self.color[x][1] = 0, 0, 0
        return True
