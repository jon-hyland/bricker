from typing import List
from random import randint
from time import perf_counter
from pygame.time import Clock
from renderer import Renderer
from matrix import Matrix


class Explode:
    """Explodes matrix spaces outwards on game over."""
    def __init__(self, clock: Clock, renderer: Renderer):
        self.__clock = clock
        self.__renderer = renderer

    def explode_spaces(self, matrix: Matrix):
        """Explodes matrix spaces outwards on game over."""
        spaces: List[ExplodingSpace] = []
        for x in range(1, 11):
            for y in range(1, 21):
                if matrix.matrix[x][y] == 1:
                    space_x = (((x - 1) * 33) + 2) + ((self.__renderer.screen_size[0] - 333) // 2) - 1
                    space_y = (((y - 1) * 33) + 2) + ((self.__renderer.screen_size[1] - 663) // 2) - 1
                    spaces.append(ExplodingSpace(space_x, space_y, matrix.color[x][y]))
                    matrix.matrix[x][y] = 0
                    matrix.color[x][y] = 0, 0, 0
        start_time = perf_counter()
        have_spaces = True
        while have_spaces:
            self.__clock.tick(30)
            self.__renderer.update_frame(matrix, spaces)
            seconds = perf_counter() - start_time
            have_spaces = False
            for space in spaces:
                space.x += space.x_motion * seconds
                space.y += space.y_motion * seconds
                if (space.x > 0) and (space.x < 1000) and (space.y > 0) and (space.y < 700):
                    have_spaces = True


class ExplodingSpace:
    """Represents an exploding matrix space, used on game over."""
    def __init__(self, x, y, color):
        self.x = float(x)
        self.y = float(y)
        self.color = color
        self.x_motion = (randint(0, 3000) / 10) + 10
        self.y_motion = (randint(0, 3000) / 10) + 10
        if randint(0, 1) == 1:
            self.x_motion = -self.x_motion
        if randint(0, 1) == 1:
            self.y_motion = -self.y_motion
