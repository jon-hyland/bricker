import pygame


class Draw:
    """ Handles surface drawing, blitting, rendering. """

    def __init__(self, screen_size, screen, clock):
        """ Class constructor.  Draws one-time surfaces. """
        self.screen_size = screen_size
        self.screen = screen
        self.clock = clock
        self.blank_grid_surface = self.draw_blank_grid()
        self.error = False
        self.debug = False

    @staticmethod
    def event_pump():
        """ Pumps the event queue, allowing frames to be rendered outside primary event loop. """
        pygame.event.pump()

    def draw_frame(self, matrix):
        """ Draws and flips the entire screen frame. """
        # draw game matrix
        matrix_surface = self.draw_matrix(matrix)

        # create new frame
        frame = pygame.Surface(self.screen_size)
        frame = frame.convert(frame)

        # fill background color
        back_color = 0, 0, 0
        if self.error:
            back_color = 100, 0, 0
        frame.fill(back_color)

        # blit surfaces
        frame.blit(matrix_surface, (int((self.screen_size[0] - 333) / 2), int((self.screen_size[1] - 663) / 2)))

        # draw fps?
        if self.debug:
            font = pygame.font.Font(None, 36)
            fps_surface = font.render("fps={0:.2f}".format(self.clock.get_fps()), True, (150, 150, 150))
            frame.blit(fps_surface, (20, (self.screen_size[1] - fps_surface.get_height()) - 15))

        # blit & flip screen
        self.screen.blit(frame, (0, 0))
        pygame.display.flip()

    @staticmethod
    def draw_blank_grid():
        """ Draws the blank game matrix grid surface. """
        draw = pygame.draw
        white = 150, 150, 150
        gray = 25, 25, 25
        black = 0, 0, 0
        grid = pygame.Surface((333, 663))
        grid = grid.convert(grid)
        grid.fill(black)

        draw.line(grid, white, (0, 0), (332, 0))
        draw.line(grid, white, (0, 1), (332, 1))
        draw.line(grid, white, (0, 0), (0, 662))
        draw.line(grid, white, (1, 0), (1, 662))
        draw.line(grid, white, (0, 662), (332, 662))
        draw.line(grid, white, (0, 661), (332, 661))
        draw.line(grid, white, (332, 0), (332, 662))
        draw.line(grid, white, (331, 0), (331, 662))

        for i in range(1, 10):
            x = (i * 33) + 1
            draw.line(grid, gray, (x, 2), (x, 660))

        for i in range(1, 20):
            y = (i * 33) + 1
            draw.line(grid, gray, (2, y), (330, y))

        return grid

    def draw_matrix(self, matrix):
        """ Draws the game matrix, once per frame. """
        draw = pygame.draw
        matrix_surface = pygame.Surface((333, 663))
        matrix_surface.blit(self.blank_grid_surface, (0, 0))

        for x in range(1, matrix.width - 1):
            for y in range(1, matrix.height - 1):
                color = matrix.color[x][y]
                if color != (0, 0, 0):
                    rect = ((x - 1) * 33) + 2, ((y - 1) * 33) + 2, 32, 32
                    draw.rect(matrix_surface, color, rect)
                if self.debug and (matrix.matrix[x][y] == 1):
                    rect = ((x - 1) * 33) + 17, ((y - 1) * 33) + 17, 2, 2
                    draw.rect(matrix_surface, (255, 255, 255), rect)

        if matrix.brick is not None:
            for x in range(0, matrix.brick.width):
                for y in range(0, matrix.brick.height):
                    if matrix.brick.grid[x][y] == 1:
                        rect = (((matrix.brick.x - 1) + x) * 33) + 2, (((matrix.brick.y - 1) + y) * 33) + 2, 32, 32
                        draw.rect(matrix_surface, matrix.brick.color, rect)
                    elif self.debug:
                        rect = (((matrix.brick.x - 1) + x) * 33) + 18, (((matrix.brick.y - 1) + y) * 33) + 18, 1, 1
                        draw.rect(matrix_surface, (255, 255, 255), rect)

        return matrix_surface

