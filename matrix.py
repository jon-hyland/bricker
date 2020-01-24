from typing import List, Optional
from random import randint
from brick import Brick
from color import Color


class Matrix:
    """Stores the 10x20 game matrix.  Contains matrix-related game logic."""

    def __init__(self) -> None:
        """Class constructor."""
        self.__width: int = 12     # 10 visible slots, plus border for collision detection
        self.__height: int = 22    # 20 visible slots, plus border for collision detection
        self.__matrix: List[List[int]] = [[0 for x in range(self.__height)] for y in range(self.__width)]
        self.__color: List[List[Color]] = [[(0, 0, 0) for x in range(self.__height)] for y in range(self.__width)]
        for x in range(0, 12):
            self.__matrix[x][0] = 1
            self.__matrix[x][21] = 1
        for y in range(0, 22):
            self.__matrix[0][y] = 1
            self.__matrix[11][y] = 1
        self.__brick: Optional[Brick] = None
        self.__next_brick: Optional[Brick] = None

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

    @property
    def color(self) -> List[List[Color]]:
        """Returns color matrix."""
        return self.__color

    @property
    def brick(self) -> Brick:
        """Returns current live brick."""
        return self.__brick

    @property
    def next_brick(self) -> Brick:
        """Returns next brick."""
        return self.__next_brick

    def new_game(self) -> None:
        """Resets the game."""
        self.__brick = None
        self.__next_brick = None
        self.__matrix = [[0 for x in range(self.__height)] for y in range(self.__width)]
        self.__color = [[(0, 0, 0) for x in range(self.__height)] for y in range(self.__width)]
        for x in range(0, 12):
            self.__matrix[x][0] = 1
            self.__matrix[x][21] = 1
        for y in range(0, 22):
            self.__matrix[0][y] = 1
            self.__matrix[11][y] = 1
        self.spawn_brick()

    def spawn_brick(self) -> bool:
        """Spawns a random new brick.  Returns true on collision (game over)."""
        if self.__next_brick is None:
            shape_num = randint(1, 7)
            self.__next_brick = Brick(shape_num)
        self.__brick = self.__next_brick
        shape_num = randint(1, 7)
        self.__next_brick = Brick(shape_num)
        collision = self.__brick.collision(self.__matrix)
        return collision

    def add_brick_to_matrix(self) -> None:
        """Moves resting brick to matrix."""
        if self.__brick is not None:
            for x in range(0, self.__brick.width):
                for y in range(0, self.__brick.height):
                    if self.__brick.grid[x][y] == 1:
                        self.__matrix[x + self.__brick.x][y + self.__brick.y] = 1
                        self.__color[x + self.__brick.x][y + self.__brick.y] = self.__brick.color
        self.__brick = None

    def move_brick_left(self) -> None:
        """Moves brick to the left."""
        if self.__brick is not None:
            self.__brick.move_left(self.__matrix)

    def move_brick_right(self) -> None:
        """ Moves brick to the right. """
        if self.__brick is not None:
            self.__brick.move_right(self.__matrix)

    def move_brick_down(self) -> bool:
        """Moves brick down.  Returns true if brick hits bottom."""
        hit = False
        if self.__brick is not None:
            hit = self.__brick.move_down(self.__matrix)
        return hit

    def rotate_brick(self) -> None:
        """Rotates brick."""
        if self.__brick is not None:
            self.__brick.rotate(self.__matrix)

    # def brick_hit(self):
    #     """Executed when brick hits bottom and comes to rest.  Spawns new brick.  Returns true on new brick collision (game over)."""
    #     self.add_brick_to_matrix()
    #     rows_to_erase = self.identify_solid_rows()
    #     if len(rows_to_erase) > 0:
    #         rows = len(rows_to_erase)
    #         self.stats.add_lines(rows)
    #         points = 40
    #         if rows == 2:
    #             points = 100
    #         elif rows == 3:
    #             points = 300
    #         elif rows == 4:
    #             points = 1200
    #         self.stats.increment_score(points)
    #         self.erase_filled_rows(rows_to_erase)
    #         self.drop_grid()
    #         self.__renderer.event_pump()
    #         self.__renderer.update_frame(self, None)
    #     collision = self.spawn_brick()
    #     return collision

    def identify_solid_rows(self) -> List[int]:
        """Checks matrix for solid rows, returns list of solid rows to erase."""
        rows_to_erase = []
        for y in range(1, 21):
            solid = True
            for x in range(1, 11):
                if self.__matrix[x][y] != 1:
                    solid = False
            if solid:
                rows_to_erase.append(y)
        return rows_to_erase

    # def is_drop_time(self) -> bool:
    #     """Returns true if it's time for brick to drop."""
    #     if self.__brick is not None:
    #         drop_interval = self.__level_drop_intervals[self.stats.level - 1]
    #         return self.__brick.is_drop_time(drop_interval)
    #     return False

    # def drop_brick_to_bottom(self) -> None:
    #     """Animates a brick dropping to bottom of screen."""
    #     hit = False
    #     while not hit:
    #         self.__renderer.clock.tick(30)
    #         for _ in range(0, 3):
    #             hit = self.move_brick_down()
    #             if hit:
    #                 break
    #         self.__renderer.event_pump()
    #         self.__renderer.update_frame(self, None)
    #     self.stats.increment_score(2)

    # def erase_filled_rows(self, rows_to_erase: List[int]) -> None:
    #     """Animates erasure of filled rows."""
    #     for x in range(1, 11):
    #         for y in rows_to_erase:
    #             self.__matrix[x][y] = 0
    #             self.__color[x][y] = 0, 0, 0
    #         if (x % 2) == 0:
    #             self.__renderer.event_pump()
    #             self.__renderer.update_frame(self, None)

    # def drop_grid(self) -> None:
    #     """Drops hanging pieces to resting place."""
    #     while self.drop_grid_once():
    #         pass

    # def drop_grid_once(self) -> bool:
    #     """Drops hanging pieces, bottom-most row."""
    #     top_filled_row = 0
    #     for row in range(1, 21):
    #         empty = True
    #         for x in range(1, 11):
    #             if self.__matrix[x][row] == 1:
    #                 empty = False
    #                 break
    #         if not empty:
    #             top_filled_row = row
    #             break
    #     if top_filled_row == 0:
    #         return False
    #     bottom_empty_row = 0
    #     for row in range(20, (top_filled_row - 1), -1):
    #         empty = True
    #         for x in range(1, 11):
    #             if self.__matrix[x][row] == 1:
    #                 empty = False
    #                 break
    #         if empty:
    #             bottom_empty_row = row
    #             break
    #     if bottom_empty_row == 0:
    #         return False
    #     for y in range(bottom_empty_row, 1, -1):
    #         for x in range(1, 11):
    #             self.__matrix[x][y] = self.__matrix[x][y - 1]
    #             self.__color[x][y] = self.__color[x][y - 1]
    #     for x in range(1, 11):
    #         self.__matrix[x][1] = 0
    #         self.__color[x][1] = 0, 0, 0
    #     return True
