import pygame
import sys
from matrix import Matrix
from draw import Draw


def main():
    """ Main program entry point. """

    # init
    pygame.init()
    screen_size = 1000, 700
    screen = pygame.display.set_mode(screen_size)
    clock = pygame.time.Clock()
    draw = Draw(screen_size, screen, clock)
    matrix = Matrix(draw)
    drop_interval = 1.0

    # event loop
    while 1:
        draw.error = False
        hit = False
        try:
            # limit fps
            clock.tick(60)

            # handle user events
            for event in pygame.event.get():
                # quit
                if (event.type == pygame.QUIT) \
                        or (event.type == pygame.KEYDOWN and event.key == pygame.K_q):
                    sys.exit()

                # left
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
                    matrix.move_brick_left()

                # right
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
                    matrix.move_brick_right()

                # down
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
                    matrix.move_brick_down()

                # rotate
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
                    matrix.rotate_brick()

                # drop
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    hit = matrix.drop_brick_to_bottom()

                # debug toggle
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_d:
                    draw.debug = not draw.debug

            # drop brick timer?
            if matrix.is_drop_time(drop_interval):
                hit = matrix.move_brick_down()

            # brick hit bottom?
            if hit:
                matrix.brick_hit()

        # handle error
        except Exception as ex:
            print(ex)
            draw.error = True

        # draw frame
        draw.draw_frame(matrix)


# start main function
if __name__ == "__main__":
    main()
