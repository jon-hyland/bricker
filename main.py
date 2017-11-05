import pygame
import sys
from matrix import Matrix
from random import randint
from brick import Brick

# globals
__screen_size = 1000, 700
__blank_grid_surface = None
__game_matrix = Matrix()
__brick = None


def main():
    """ Main program entry point. """
    # globals
    global __screen_size
    global __game_matrix
    global __brick

    # init game engine
    pygame.init()

    # init game vars
    screen = pygame.display.set_mode(__screen_size)
    clock = pygame.time.Clock()
    matrix = __game_matrix.matrix
    drop_interval = 1.0
    drop_to_bottom = False
    debug = False

    # draw one-time surfaces
    init_surfaces()

    # spawn first brick
    __brick = spawn_new_brick()

    # event loop
    while 1:
        error = False
        try:
            # limit to 30 fps
            clock.tick(30)

            # drop to bottom?
            if drop_to_bottom:
                hit = __brick.move_down(matrix)
                # if not hit:
                #     hit = __brick.move_down(matrix)
                if hit:
                    __game_matrix.add_brick(__brick)
                    __brick = spawn_new_brick()
                    drop_to_bottom = False
                pygame.event.pump()

            # no special event
            else:
                # handle user events
                for event in pygame.event.get():
                    if (event.type == pygame.QUIT) \
                            or (event.type == pygame.KEYDOWN and event.key == pygame.K_q):
                        sys.exit()
                    elif event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
                        __brick.move_left(matrix)
                    elif event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
                        __brick.move_right(matrix)
                    elif event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
                        __brick.move_down(matrix)
                    elif event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
                        __brick.rotate(matrix)
                    elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                        drop_to_bottom = True
                    elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                        __brick = spawn_new_brick()
                    elif event.type == pygame.KEYDOWN and event.key == pygame.K_d:
                        debug = not debug

                # drop brick?
                if __brick.is_drop_time(drop_interval):
                    hit = __brick.drop_down(matrix)
                    if hit:
                        __game_matrix.add_brick(__brick)
                        __brick = spawn_new_brick()

        # handle error
        except Exception as ex:
            print(ex)
            error = True

        # draw frame and refresh
        frame = draw_frame(error, debug)
        screen.blit(frame, (0, 0))
        pygame.display.flip()


def init_surfaces():
    """ Draws one-time, reusable surfaces. """
    global __blank_grid_surface
    __blank_grid_surface = draw_blank_grid()


def draw_blank_grid():
    """ Draws the blank game matrix grid surface. """
    draw = pygame.draw
    white = 150, 150, 150
    gray = 25, 25, 25
    grid = pygame.Surface((333, 663))
    grid = grid.convert(grid)
    grid.fill((0, 0, 0))

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


def draw_matrix(debug):
    """ Draws the game matrix, once per frame. """
    global __blank_grid_surface
    global __game_matrix
    global __brick

    # blit blank matrix grid
    draw = pygame.draw
    matrix = pygame.Surface((333, 663))
    matrix.blit(__blank_grid_surface, (0, 0))

    # draw filled matrix spaces (dead bricks)
    for x in range(1, __game_matrix.width - 1):
        for y in range(1, __game_matrix.height - 1):
            color = __game_matrix.color[x][y]
            if color != (0, 0, 0):
                rect = ((x - 1) * 33) + 2, ((y - 1) * 33) + 2, 32, 32
                draw.rect(matrix, color, rect)
            if debug and (__game_matrix.matrix[x][y] == 1):
                rect = ((x - 1) * 33) + 17, ((y - 1) * 33) + 17, 2, 2
                draw.rect(matrix, (255, 255, 255), rect)

    # draw current live brick
    if __brick is not None:
        for x in range(0, __brick.width):
            for y in range(0, __brick.height):
                if __brick.grid[x][y] == 1:
                    rect = (((__brick.x - 1) + x) * 33) + 2, (((__brick.y - 1) + y) * 33) + 2, 32, 32
                    draw.rect(matrix, __brick.color, rect)
                elif debug:
                    rect = (((__brick.x - 1) + x) * 33) + 18, (((__brick.y - 1) + y) * 33) + 18, 1, 1
                    draw.rect(matrix, (255, 255, 255), rect)

    # for x in range(0, 10):
    #     for y in range(0, 20):
    #         color = randint(0, 255), randint(0, 255), randint(0, 255)
    #         rect = (x * 33) + 2, (y * 33) + 2, 32, 32
    #         draw.rect(matrix, color, rect)

    return matrix


def draw_frame(error, debug):
    """ Draws the entire screen frame. """
    global __screen_size

    matrix = draw_matrix(debug)

    frame = pygame.Surface(__screen_size)
    frame = frame.convert(frame)

    if not error:
        frame.fill((0, 0, 0))
    else:
        frame.fill((50, 0, 0))

    frame.blit(matrix, (int((__screen_size[0] - 333) / 2), int((__screen_size[1] - 663) / 2)))

    return frame


def spawn_new_brick():
    """ Spawns a new (random) brick. """
    shape_num = randint(1, 7)
    brick = Brick(shape_num)
    return brick


# start main function
if __name__ == "__main__":
    main()
