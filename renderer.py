from typing import Tuple, List, Optional
import pygame
from pygame import Surface
from pygame.font import Font
from pygame.time import Clock
from color import Color
from matrix import Matrix
from explode import ExplodingSpace


class Renderer:
    """Handles surface drawing, blitting, rendering."""

    def __init__(self, screen_size: Tuple[int, int], screen: Surface, clock: Clock) -> None:
        """Class constructor."""
        self.__screen_size: Tuple[int, int] = screen_size
        self.__screen: Surface = screen
        self.__clock: Clock = clock
        self.__font_title: Font = Font("zorque.ttf", 64)
        self.__font_large: Font = Font("zorque.ttf", 42)
        self.__font_med: Font = Font("zorque.ttf", 28)
        self.__font_small: Font = Font("zorque.ttf", 18)
        self.__blank_grid_surface: Surface = self.draw_blank_grid()
        self.__debug: bool = False

    @property
    def screen_size(self) -> Tuple[int, int]:
        """Returns width/height of screen surface size."""
        return self.__screen_size

    @property
    def clock(self) -> Clock:
        """Returns clock instance."""
        return self.__clock

    @property
    def debug(self) -> bool:
        """Returns debug flag."""
        return self.__debug

    @debug.setter
    def debug(self, value: bool) -> None:
        """Sets debug flag."""
        self.__debug = value

    @staticmethod
    def __create_surface(size: Tuple[int, int]) -> Surface:
        """Returns a new Surface instance."""
        surface = Surface(size, pygame.SRCALPHA, 32)
        surface = surface.convert_alpha(surface)
        return surface

    @staticmethod
    def event_pump() -> None:
        """Pumps the event queue, allowing frames to be rendered outside primary event loop."""
        pygame.event.pump()

    def update_frame(self, matrix: Matrix, spaces: Optional[List[ExplodingSpace]] = None):
        """Draws and flips the entire screen frame."""
        frame = self.draw_frame(matrix, spaces)
        self.__screen.blit(frame, (0, 0))
        pygame.display.flip()

    def draw_frame(self, matrix, spaces: Optional[List[ExplodingSpace]] = None):
        """Draws the primary game screen surface."""
        
        # vars
        side_width = (self.__screen_size[0] - 333) // 2
        left_x = ((side_width - 250) // 2) + 5
        right_x = side_width + 333 + left_x

        # create new frame
        frame = pygame.Surface(self.__screen_size)
        frame = frame.convert(frame)
        frame.fill(Color.Black)

        # game matrix
        matrix_surface = self.draw_matrix(matrix)
        frame.blit(matrix_surface, (side_width, (self.__screen_size[1] - 663) // 2))

        # spaces
        if spaces is not None:
            for space in spaces:
                x = int(space.x)
                y = int(space.y)
                rect = x, y, 34, 34
                pygame.draw.rect(frame, space.color, rect)
                pygame.draw.line(frame, Color.Black, (x, y), (x + 34, y))
                pygame.draw.line(frame, Color.Black, (x, y + 34), (x + 34, y + 34))
                pygame.draw.line(frame, Color.Black, (x, y), (x, y + 34))
                pygame.draw.line(frame, Color.Black, (x + 34, y), (x + 34, y + 34))

        # title
        title_surface = self.draw_title()
        frame.blit(title_surface, ((side_width - title_surface.get_width()) // 2, 30))

        # controls
        controls_surface = self.draw_controls()
        frame.blit(controls_surface, (left_x, 210))

        # next
        next_surface = self.draw_next(matrix)
        frame.blit(next_surface, (left_x, 480))

        # level
        level_surface = self.draw_level(matrix.stats)
        frame.blit(level_surface, (right_x, 36))

        # lines
        lines_surface = self.draw_lines(matrix.stats)
        frame.blit(lines_surface, (right_x, 156))

        # current score
        current_score_surface = self.draw_current_score(matrix.stats)
        frame.blit(current_score_surface, (right_x, 276))

        # high scores
        high_scores_surface = self.draw_high_scores(matrix.stats)
        frame.blit(high_scores_surface, (right_x, 396))

        # draw fps?
        if self.__debug:
            fps_surface = self.__font_small.render("fps: {0:.2f}".format(self.clock.get_fps()), True, Color.White)
            frame.blit(fps_surface, (left_x, (self.__screen_size[1] - fps_surface.get_height()) - 15))

        # return
        return frame

    @staticmethod
    def draw_blank_grid() -> Surface:
        """Draws the blank game matrix grid surface."""
        grid = Surface((333, 663))
        grid = grid.convert(grid)
        grid.fill(Color.Black)

        pygame.draw.line(grid, Color.White, (0, 0), (332, 0))
        pygame.draw.line(grid, Color.White, (0, 1), (332, 1))
        pygame.draw.line(grid, Color.White, (0, 0), (0, 662))
        pygame.draw.line(grid, Color.White, (1, 0), (1, 662))
        pygame.draw.line(grid, Color.White, (0, 662), (332, 662))
        pygame.draw.line(grid, Color.White, (0, 661), (332, 661))
        pygame.draw.line(grid, Color.White, (332, 0), (332, 662))
        pygame.draw.line(grid, Color.White, (331, 0), (331, 662))

        for i in range(1, 10):
            x = (i * 33) + 1
            pygame.draw.line(grid, Color.Gray, (x, 2), (x, 660))

        for i in range(1, 20):
            y = (i * 33) + 1
            pygame.draw.line(grid, Color.Gray, (2, y), (330, y))

        return grid

    def draw_title(self):
        """Draws the title surface."""
        title_surface = self.__font_title.render("bricker", True, Color.White)
        version_surface = self.__font_small.render("www.intsol.tech", True, Color.White)
        surface = self.__create_surface((title_surface.get_width(), (title_surface.get_height() + version_surface.get_height())))
        if self.__debug:
            surface.fill(Color.PortlandOrange)
        surface.blit(title_surface, (0, 0))
        surface.blit(version_surface, (surface.get_width() - version_surface.get_width() - 5, title_surface.get_height() - 10))
        return surface

    def draw_controls(self):
        """Draw controls surface."""
        width = 240
        space = 18
        title_surface = self.__font_med.render("controls", True, Color.White)
        left_1 = self.__font_small.render("left", True, Color.White)
        left_2 = self.__font_small.render("right", True, Color.White)
        left_3 = self.__font_small.render("down", True, Color.White)
        left_4 = self.__font_small.render("rotate", True, Color.White)
        left_5 = self.__font_small.render("drop", True, Color.White)
        left_6 = self.__font_small.render("pause", True, Color.White)
        right_1 = self.__font_small.render("left", True, Color.White)
        right_2 = self.__font_small.render("right", True, Color.White)
        right_3 = self.__font_small.render("down", True, Color.White)
        right_4 = self.__font_small.render("up", True, Color.White)
        right_5 = self.__font_small.render("space", True, Color.White)
        right_6 = self.__font_small.render("esc", True, Color.White)
        line_height = left_1.get_height()
        surface = self.__create_surface((width, title_surface.get_height() + (line_height * 6) + space))
        if self.__debug:
            surface.fill(Color.PortlandOrange)
        surface.blit(title_surface, (0, 0))
        surface.blit(left_1, (10, (title_surface.get_height() + (line_height * 0)) + space))
        surface.blit(left_2, (10, (title_surface.get_height() + (line_height * 1)) + space))
        surface.blit(left_3, (10, (title_surface.get_height() + (line_height * 2)) + space))
        surface.blit(left_4, (10, (title_surface.get_height() + (line_height * 3)) + space))
        surface.blit(left_5, (10, (title_surface.get_height() + (line_height * 4)) + space))
        surface.blit(left_6, (10, (title_surface.get_height() + (line_height * 5)) + space))
        surface.blit(right_1, ((width - right_1.get_width() - 10), (title_surface.get_height() + (line_height * 0)) + space))
        surface.blit(right_2, ((width - right_2.get_width() - 10), (title_surface.get_height() + (line_height * 1)) + space))
        surface.blit(right_3, ((width - right_3.get_width() - 10), (title_surface.get_height() + (line_height * 2)) + space))
        surface.blit(right_4, ((width - right_4.get_width() - 10), (title_surface.get_height() + (line_height * 3)) + space))
        surface.blit(right_5, ((width - right_5.get_width() - 10), (title_surface.get_height() + (line_height * 4)) + space))
        surface.blit(right_6, ((width - right_6.get_width() - 10), (title_surface.get_height() + (line_height * 5)) + space))
        return surface

    def draw_next(self, matrix):
        """Draw next brick surface."""
        width = 240
        title_surface = self.__font_med.render("next", True, Color.White)
        surface = self.__create_surface((width, 135 + title_surface.get_height()))
        if self.__debug:
            surface.fill(Color.PortlandOrange)
        if matrix.next_brick is not None:
            next_brick = matrix.next_brick
            size = (next_brick.width * 32) + (next_brick.width - 1)
            brick_surface = self.__create_surface((size, size))
            for x in range(0, next_brick.width):
                for y in range(0, next_brick.height):
                    if next_brick.grid[x][y] == 1:
                        rect = (x * 33), (y * 33), 32, 32
                        pygame.draw.rect(brick_surface, next_brick.color, rect)
            surface.blit(brick_surface, ((width - size) // 2,
                                         title_surface.get_height() - (next_brick.top_space * 33) + 24))
        surface.blit(title_surface, (0, 0))
        return surface

    def draw_level(self, stats):
        """Draw level surface."""
        width = 240
        space = 4
        title_surface = self.__font_med.render("level", True, Color.White)
        level_surface = self.__font_large.render("{:,}".format(stats.level), True, Color.White)
        surface = self.__create_surface((width, title_surface.get_height() + space + level_surface.get_height()))
        if self.__debug:
            surface.fill(Color.PortlandOrange)
        surface.blit(title_surface, (0, 0))
        surface.blit(level_surface, ((width - level_surface.get_width()),
                                     (title_surface.get_height() + space)))
        return surface

    def draw_lines(self, stats):
        """Draw lines surface."""
        width = 240
        space = 4
        title_surface = self.__font_med.render("lines", True, Color.White)
        lines_surface = self.__font_large.render("{:,}".format(stats.lines), True, Color.White)
        surface = self.__create_surface((width, title_surface.get_height() + space + lines_surface.get_height()))
        if self.__debug:
            surface.fill(Color.PortlandOrange)
        surface.blit(title_surface, (0, 0))
        surface.blit(lines_surface, ((width - lines_surface.get_width()), (title_surface.get_height() + space)))
        return surface

    def draw_current_score(self, stats):
        """Draw current score surface."""
        width = 240
        space = 4
        title_surface = self.__font_med.render("score", True, Color.White)
        score_surface = self.__font_large.render("{:,}".format(stats.current_score), True, Color.White)
        surface = self.__create_surface((width, title_surface.get_height() + space + score_surface.get_height()))
        if self.__debug:
            surface.fill(Color.PortlandOrange)
        surface.blit(title_surface, (0, 0))
        surface.blit(score_surface, ((width - score_surface.get_width()), (title_surface.get_height() + space)))
        return surface

    def draw_high_scores(self, stats):
        """Draw high score surface."""
        width = 240
        space = 10
        title_surface = self.__font_med.render("high scores", True, Color.White)
        line_height = self.__font_small.get_height()
        height = title_surface.get_height() + space + (line_height * 10)
        surface = self.__create_surface((width, height))
        if self.__debug:
            surface.fill(Color.PortlandOrange)
        surface.blit(title_surface, (0, 0))
        line = 0
        for score in stats.high_scores:
            left = self.__font_small.render(score.initials, True, Color.White)
            right = self.__font_small.render("{:,}".format(score.score), True, Color.White)
            surface.blit(left, (10, (title_surface.get_height() + space + (line * line_height))))
            surface.blit(right, (width - right.get_width(), (title_surface.get_height() + space + (line * line_height))))
            line += 1
        return surface

    def draw_matrix(self, matrix):
        """Draws the game matrix, once per frame."""
        matrix_surface = self.__create_surface((333, 663))
        matrix_surface.blit(self.__blank_grid_surface, (0, 0))

        for x in range(1, matrix.width - 1):
            for y in range(1, matrix.height - 1):
                color = matrix.color[x][y]
                if color != (0, 0, 0):
                    rect = ((x - 1) * 33) + 2, ((y - 1) * 33) + 2, 32, 32
                    pygame.draw.rect(matrix_surface, color, rect)
                if self.__debug and (matrix.matrix[x][y] == 1):
                    rect = ((x - 1) * 33) + 17, ((y - 1) * 33) + 17, 2, 2
                    pygame.draw.rect(matrix_surface, Color.White, rect)

        if matrix.brick is not None:
            for x in range(0, matrix.brick.width):
                for y in range(0, matrix.brick.height):
                    if matrix.brick.grid[x][y] == 1:
                        rect = (((matrix.brick.x - 1) + x) * 33) + 2, (((matrix.brick.y - 1) + y) * 33) + 2, 32, 32
                        pygame.draw.rect(matrix_surface, matrix.brick.color, rect)
                    elif self.__debug:
                        rect = (((matrix.brick.x - 1) + x) * 33) + 17, (((matrix.brick.y - 1) + y) * 33) + 17, 2, 2
                        pygame.draw.rect(matrix_surface, Color.White, rect)

        return matrix_surface

    def draw_menu(self, matrix, menu_selection, in_game):
        """Draws the main menu frame."""
        width = 400
        spacing = 25

        resume_color = Color.White
        if not in_game:
            resume_color = Color.Gray
        new_color = Color.White
        quit_color = Color.White
        if menu_selection == 1:
            resume_color = Color.FluorescentOrange
        elif menu_selection == 2:
            new_color = Color.FluorescentOrange
        elif menu_selection == 3:
            quit_color = Color.FluorescentOrange

        resume_surface = self.__font_large.render("resume", True, resume_color)
        new_surface = self.__font_large.render("new game", True, new_color)
        quit_surface = self.__font_large.render("quit", True, quit_color)

        surface = self.__create_surface((width, (resume_surface.get_height() * 3) + (spacing * 4) + 4))
        surface.fill(Color.Black)
        pygame.draw.line(surface, Color.White, (0, 0), (surface.get_width() - 1, 0), 1)
        pygame.draw.line(surface, Color.White, (0, 1), (surface.get_width() - 1, 1), 1)
        pygame.draw.line(surface, Color.White, (0, surface.get_height() - 2), (surface.get_width() - 1, surface.get_height() - 2), 1)
        pygame.draw.line(surface, Color.White, (0, surface.get_height() - 1), (surface.get_width() - 1, surface.get_height() - 1), 1)
        pygame.draw.line(surface, Color.White, (0, 0), (0, surface.get_height() - 1), 1)
        pygame.draw.line(surface, Color.White, (1, 0), (1, surface.get_height() - 1), 1)
        pygame.draw.line(surface, Color.White, (surface.get_width() - 2, 0), (surface.get_width() - 2, surface.get_height() - 1), 1)
        pygame.draw.line(surface, Color.White, (surface.get_width() - 1, 0), (surface.get_width() - 1, surface.get_height() - 1), 1)
        surface.blit(resume_surface, ((surface.get_width() - resume_surface.get_width()) // 2, spacing + 2))
        surface.blit(new_surface, ((surface.get_width() - new_surface.get_width()) // 2, (spacing * 2) + new_surface.get_height() + 2))
        surface.blit(quit_surface, ((surface.get_width() - quit_surface.get_width()) // 2, (spacing * 3) + (quit_surface.get_height() * 2) + 2))

        frame = self.draw_frame(matrix, None)
        frame.blit(surface, ((frame.get_width() - surface.get_width()) // 2, (frame.get_height() - surface.get_height()) // 2))

        self.event_pump()
        self.__screen.blit(frame, (0, 0))
        pygame.display.flip()

    def draw_initials_input(self, matrix, chars):
        """Draws the high score initials input frame."""
        width = 400
        spacing = 15
        char_width = 60
        char_height = 82

        line1 = self.__font_med.render("new high score!", True, Color.White)
        line2 = self.__font_med.render("enter initials:", True, Color.White)

        char1 = self.__font_title.render(chars[0], True, Color.FluorescentOrange)
        char2 = self.__font_title.render(chars[1], True, Color.FluorescentOrange)
        char3 = self.__font_title.render(chars[2], True, Color.FluorescentOrange)

        slot1 = self.__create_surface((char_width, char_height))
        slot2 = self.__create_surface((char_width, char_height))
        slot3 = self.__create_surface((char_width, char_height))
        slot1.blit(char1, (((char_width - char1.get_width()) // 2), ((char_height - char1.get_height()) // 2)))
        slot2.blit(char2, (((char_width - char2.get_width()) // 2), ((char_height - char2.get_height()) // 2)))
        slot3.blit(char3, (((char_width - char3.get_width()) // 2), ((char_height - char3.get_height()) // 2)))

        initials = self.__create_surface((char_width * 3, char_height))
        initials.blit(slot1, (0, 0))
        initials.blit(slot2, (char_width, 0))
        initials.blit(slot3, (char_width * 2, 0))

        surface = self.__create_surface((width, (spacing * 3) + line1.get_height() + line2.get_height() + char_height + 4))
        surface.fill(Color.Black)
        pygame.draw.line(surface, Color.White, (0, 0), (surface.get_width() - 1, 0), 1)
        pygame.draw.line(surface, Color.White, (0, 1), (surface.get_width() - 1, 1), 1)
        pygame.draw.line(surface, Color.White, (0, surface.get_height() - 2), (surface.get_width() - 1, surface.get_height() - 2), 1)
        pygame.draw.line(surface, Color.White, (0, surface.get_height() - 1), (surface.get_width() - 1, surface.get_height() - 1), 1)
        pygame.draw.line(surface, Color.White, (0, 0), (0, surface.get_height() - 1), 1)
        pygame.draw.line(surface, Color.White, (1, 0), (1, surface.get_height() - 1), 1)
        pygame.draw.line(surface, Color.White, (surface.get_width() - 2, 0), (surface.get_width() - 2, surface.get_height() - 1), 1)
        pygame.draw.line(surface, Color.White, (surface.get_width() - 1, 0), (surface.get_width() - 1, surface.get_height() - 1), 1)

        surface.blit(line1, ((surface.get_width() - line1.get_width()) // 2, spacing + 2))
        surface.blit(line2, ((surface.get_width() - line2.get_width()) // 2, spacing + line1.get_height() + 2))
        surface.blit(initials, ((surface.get_width() - initials.get_width()) // 2, (spacing * 2) + line1.get_height() + line2.get_height() + 2))

        frame = self.draw_frame(matrix, None)
        frame.blit(surface, ((frame.get_width() - surface.get_width()) // 2, (frame.get_height() - surface.get_height()) // 2))

        self.event_pump()
        self.__screen.blit(frame, (0, 0))
        pygame.display.flip()
