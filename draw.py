import pygame
from color import Color


class Draw:
    """ Handles surface drawing, blitting, rendering. """

    def __init__(self, screen_size, screen, clock):
        """ Class constructor.  Draws one-time surfaces. """
        self.screen_size = screen_size
        self.screen = screen
        self.clock = clock
        self.font_title = pygame.font.Font("zorque.ttf", 64)
        self.font_large = pygame.font.Font("zorque.ttf", 42)
        self.font_med = pygame.font.Font("zorque.ttf", 28)
        self.font_small = pygame.font.Font("zorque.ttf", 18)
        self.blank_grid_surface = self.draw_blank_grid()
        self.title_surface = self.draw_title()
        self.error = False
        self.debug = False

    @staticmethod
    def event_pump():
        """ Pumps the event queue, allowing frames to be rendered outside primary event loop. """
        pygame.event.pump()

    def draw_frame(self, matrix):
        """ Draws and flips the entire screen frame. """
        # vars
        side_width = int((self.screen_size[0] - 333) / 2)
        left_x = int((side_width - 250) / 2)
        right_x = side_width + 333 + left_x + 5

        # create new frame
        frame = pygame.Surface(self.screen_size)
        frame = frame.convert(frame)
        frame.fill(Color.Black)
        if self.error:
            frame.fill(Color.ErrorBlack)

        # game matrix
        matrix_surface = self.draw_matrix(matrix)
        frame.blit(matrix_surface, (side_width, int((self.screen_size[1] - 663) / 2)))

        # title
        frame.blit(self.title_surface, (left_x, 30))

        # controls
        controls_surface = self.draw_controls()
        frame.blit(controls_surface, (left_x, 230))

        # next
        next_surface = self.draw_next(matrix)
        frame.blit(next_surface, (left_x, 480))

        # lines
        lines_surface = self.draw_lines(matrix.stats)
        frame.blit(lines_surface, (right_x, 36))

        # current score
        current_score_surface = self.draw_current_score(matrix.stats)
        frame.blit(current_score_surface, (right_x, 180))

        # high scores
        high_scores_surface = self.draw_high_scores(matrix.stats)
        frame.blit(high_scores_surface, (right_x, 320))

        # draw fps?
        if self.debug:
            fps_surface = self.font_small.render("fps: {0:.2f}".format(self.clock.get_fps()), True, Color.White)
            frame.blit(fps_surface, (20, (self.screen_size[1] - fps_surface.get_height()) - 15))

        # blit & flip screen
        self.screen.blit(frame, (0, 0))
        pygame.display.flip()

    @staticmethod
    def draw_blank_grid():
        """ Draws the blank game matrix grid surface. """
        grid = pygame.Surface((333, 663))
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
        """ Draws the title surface. """
        title_surface = self.font_title.render("bricker", True, Color.White)
        version_surface = self.font_small.render("v1.0", True, Color.White)
        surface = pygame.Surface((title_surface.get_width(),
                                 (title_surface.get_height() + version_surface.get_height())))
        # surface.fill(Color.TestBack)
        surface.blit(title_surface, (0, 0))
        surface.blit(version_surface, (surface.get_width() - version_surface.get_width() - 5,
                                       title_surface.get_height() - 10))
        return surface

    def draw_controls(self):
        """ Draw controls surface. """
        width = 240
        space = 18
        title_surface = self.font_med.render("controls", True, Color.White)
        left_1 = self.font_small.render("left", True, Color.White)
        left_2 = self.font_small.render("right", True, Color.White)
        left_3 = self.font_small.render("down", True, Color.White)
        left_4 = self.font_small.render("rotate", True, Color.White)
        left_5 = self.font_small.render("drop", True, Color.White)
        left_6 = self.font_small.render("pause", True, Color.White)
        left_7 = self.font_small.render("quit", True, Color.White)
        right_1 = self.font_small.render("left", True, Color.White)
        right_2 = self.font_small.render("right", True, Color.White)
        right_3 = self.font_small.render("down", True, Color.White)
        right_4 = self.font_small.render("up", True, Color.White)
        right_5 = self.font_small.render("space", True, Color.White)
        right_6 = self.font_small.render("p", True, Color.White)
        right_7 = self.font_small.render("q", True, Color.White)
        line_height = left_1.get_height()
        surface = pygame.Surface((width, title_surface.get_height() + (line_height * 7) + space))
        # surface.fill(Color.TestBack)
        surface.blit(title_surface, (0, 0))
        surface.blit(left_1, (10, (title_surface.get_height() + (line_height * 0)) + space))
        surface.blit(left_2, (10, (title_surface.get_height() + (line_height * 1)) + space))
        surface.blit(left_3, (10, (title_surface.get_height() + (line_height * 2)) + space))
        surface.blit(left_4, (10, (title_surface.get_height() + (line_height * 3)) + space))
        surface.blit(left_5, (10, (title_surface.get_height() + (line_height * 4)) + space))
        surface.blit(left_6, (10, (title_surface.get_height() + (line_height * 5)) + space))
        surface.blit(left_7, (10, (title_surface.get_height() + (line_height * 6)) + space))
        surface.blit(right_1, ((width - right_1.get_width() - 10), (title_surface.get_height() + (line_height * 0)) + space))
        surface.blit(right_2, ((width - right_2.get_width() - 10), (title_surface.get_height() + (line_height * 1)) + space))
        surface.blit(right_3, ((width - right_3.get_width() - 10), (title_surface.get_height() + (line_height * 2)) + space))
        surface.blit(right_4, ((width - right_4.get_width() - 10), (title_surface.get_height() + (line_height * 3)) + space))
        surface.blit(right_5, ((width - right_5.get_width() - 10), (title_surface.get_height() + (line_height * 4)) + space))
        surface.blit(right_6, ((width - right_6.get_width() - 10), (title_surface.get_height() + (line_height * 5)) + space))
        surface.blit(right_7, ((width - right_7.get_width() - 10), (title_surface.get_height() + (line_height * 6)) + space))
        return surface

    def draw_next(self, matrix):
        """ Draw next brick surface. """
        width = 240
        next_brick = matrix.next_brick
        size = (next_brick.width * 32) + (next_brick.width - 1)
        title_surface = self.font_med.render("next", True, Color.White)
        brick_surface = pygame.Surface((size, size))
        for x in range(0, next_brick.width):
            for y in range(0, next_brick.height):
                if next_brick.grid[x][y] == 1:
                    rect = (x * 33), (y * 33), 32, 32
                    pygame.draw.rect(brick_surface, next_brick.color, rect)
        surface = pygame.Surface((width, 135 + title_surface.get_height()))
        # surface.fill(Color.TestBack)
        surface.blit(brick_surface, ((width - size) // 2,
                                     title_surface.get_height() - (next_brick.top_space * 33) + 24))
        surface.blit(title_surface, (0, 0))
        return surface

    def draw_high_scores(self, stats):
        """ Draw high score surface. """
        width = 240
        space = 14
        title_surface = self.font_med.render("high scores", True, Color.White)
        line_height = self.font_small.get_height()
        height = title_surface.get_height() + space + (line_height * 10)
        surface = pygame.Surface((width, height))
        surface.blit(title_surface, (0, 0))
        line = 0
        for score in stats.high_scores:
            left = self.font_small.render(score.initials, True, Color.White)
            right = self.font_small.render("{:,}".format(score.score), True, Color.White)
            surface.blit(left, (10, (title_surface.get_height() + space + (line * line_height))))
            surface.blit(right, (width - right.get_width(), (title_surface.get_height() + space + (line * line_height))))
            line += 1
        return surface

    def draw_current_score(self, stats):
        """ Draw current score surface. """
        width = 240
        space = 14
        title_surface = self.font_med.render("score", True, Color.White)
        score_surface = self.font_large.render("{:,}".format(stats.current_score), True, Color.White)
        surface = pygame.Surface((width, title_surface.get_height() + space + score_surface.get_height()))
        surface.blit(title_surface, (0, 0))
        surface.blit(score_surface, ((width - score_surface.get_width()),
                                     (title_surface.get_height() + space)))
        return surface

    def draw_lines(self, stats):
        """ Draw lines surface. """
        width = 240
        space = 14
        title_surface = self.font_med.render("lines", True, Color.White)
        score_surface = self.font_large.render("{:,}".format(stats.lines), True, Color.White)
        surface = pygame.Surface((width, title_surface.get_height() + space + score_surface.get_height()))
        surface.blit(title_surface, (0, 0))
        surface.blit(score_surface, ((width - score_surface.get_width()),
                                     (title_surface.get_height() + space)))
        return surface

    def draw_matrix(self, matrix):
        """ Draws the game matrix, once per frame. """
        matrix_surface = pygame.Surface((333, 663))
        matrix_surface.blit(self.blank_grid_surface, (0, 0))

        for x in range(1, matrix.width - 1):
            for y in range(1, matrix.height - 1):
                color = matrix.color[x][y]
                if color != (0, 0, 0):
                    rect = ((x - 1) * 33) + 2, ((y - 1) * 33) + 2, 32, 32
                    pygame.draw.rect(matrix_surface, color, rect)
                if self.debug and (matrix.matrix[x][y] == 1):
                    rect = ((x - 1) * 33) + 17, ((y - 1) * 33) + 17, 2, 2
                    pygame.draw.rect(matrix_surface, Color.White, rect)

        if matrix.brick is not None:
            for x in range(0, matrix.brick.width):
                for y in range(0, matrix.brick.height):
                    if matrix.brick.grid[x][y] == 1:
                        rect = (((matrix.brick.x - 1) + x) * 33) + 2, (((matrix.brick.y - 1) + y) * 33) + 2, 32, 32
                        pygame.draw.rect(matrix_surface, matrix.brick.color, rect)
                    elif self.debug:
                        rect = (((matrix.brick.x - 1) + x) * 33) + 17, (((matrix.brick.y - 1) + y) * 33) + 17, 2, 2
                        pygame.draw.rect(matrix_surface, Color.White, rect)

        return matrix_surface

