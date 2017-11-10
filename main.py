import pygame
from matrix import Matrix
from draw import Draw
from explode import Explode


def main():
    """ Main program entry point. """

    # init
    pygame.init()
    screen_size = 1000, 700
    screen = pygame.display.set_mode(screen_size)
    clock = pygame.time.Clock()
    draw = Draw(screen_size, screen, clock)
    matrix = Matrix(draw)
    menu_selection = 0
    in_game = False

    # menu loop
    while menu_selection != 3:
        menu_selection = menu_loop(clock, draw, matrix, in_game)
        if menu_selection == 1:
            in_game = game_loop(clock, draw, matrix)
        elif menu_selection == 2:
            matrix.new_game()
            in_game = game_loop(clock, draw, matrix)
        elif menu_selection == 3:
            pass


def menu_loop(clock, draw, matrix, in_game):
    """ The main menu loop. """
    # vars
    menu_selection = 1
    if not in_game:
        menu_selection = 2

    # loop until selection
    while 1:
        # limit fps
        clock.tick(60)

        # handle user events
        for event in pygame.event.get():
            # up
            if event.type == pygame.KEYDOWN \
                    and (event.key == pygame.K_LEFT or event.key == pygame.K_UP):
                menu_selection -= 1
                if in_game:
                    if menu_selection < 1:
                        menu_selection = 3
                else:
                    if menu_selection < 2:
                        menu_selection = 3

            # down
            elif event.type == pygame.KEYDOWN \
                    and (event.key == pygame.K_RIGHT or event.key == pygame.K_DOWN):
                menu_selection += 1
                if in_game:
                    if menu_selection > 3:
                        menu_selection = 1
                else:
                    if menu_selection > 3:
                        menu_selection = 2

            # enter
            elif event.type == pygame.KEYDOWN \
                    and (event.key == pygame.K_SPACE or event.key == pygame.K_RETURN):
                return menu_selection

        # draw menu
        draw.draw_menu(matrix, menu_selection, in_game)


def high_score_loop(clock, draw, matrix):
    """ The main menu loop. """
    # vars
    chars = list("   ")
    pos = 0
    numbers = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j',
               'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
               'u', 'v', 'w', 'x', 'y', 'z']
    done = False

    # loop
    while not done:
        # limit fps
        clock.tick(60)

        # handle user events
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if str(pygame.key.name(event.key)) in letters + numbers:
                    if pos < 3:
                        char = str(pygame.key.name(event.key))
                        chars[pos] = char
                        pos += 1
                        if pos > 3:
                            pos = 3
                elif event.key == pygame.K_BACKSPACE:
                    pos -= 1
                    if pos < 0:
                        pos = 0
                    if pos <= 2:
                        chars[pos] = " "
                elif event.key == pygame.K_RETURN:
                    if len("".join(chars).strip()) == 3:
                        done = True

        # draw frame
        draw.draw_initials_input(matrix, chars)

    initials = "".join(chars).lower()
    matrix.stats.add_high_score(initials)


def game_loop(clock, draw, matrix):
    """ The game loop. """
    # vars
    game_over = False

    # event loop
    while not game_over:
        draw.error = False
        hit = False
        try:
            # limit fps
            clock.tick(60)

            # handle user events
            for event in pygame.event.get():
                # left
                if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
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

                # menu
                elif event.type == pygame.KEYDOWN and (event.key == pygame.K_ESCAPE or event.key == pygame.K_q):
                    return True

                # level up
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_PAGEUP:
                    if draw.debug:
                        matrix.stats.level += 1
                        if matrix.stats.level > 10:
                            matrix.stats.level = 10

                # level down
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_PAGEDOWN:
                    if draw.debug:
                        matrix.stats.level -= 1
                        if matrix.stats.level < 1:
                            matrix.stats.level = 1

                # debug toggle
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_d:
                    draw.debug = not draw.debug

            # drop brick timer?
            if matrix.is_drop_time():    # add drop interval
                hit = matrix.move_brick_down()

            # brick hit bottom?
            if hit:
                game_over = matrix.brick_hit()

        # handle error
        except Exception as ex:
            print(str(ex))
            draw.error = True

        # draw frame
        draw.update_frame(matrix, None)

    # game over
    matrix.add_brick_to_matrix()
    explode = Explode(clock, draw)
    explode.explode_spaces(matrix)
    if matrix.stats.is_high_score():
        high_score_loop(clock, draw, matrix)
    return False


# start main function
if __name__ == "__main__":
    main()
