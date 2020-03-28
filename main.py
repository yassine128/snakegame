import curses

from curses import KEY_RIGHT, KEY_LEFT, KEY_DOWN, KEY_UP
from curses import wrapper
from random import randint
from time import sleep

def main(stdscr):
    # Taking off the cursor
    curses.curs_set(0)
    # Not showing the input characters
    curses.noecho()

    y, x = stdscr.getmaxyx()
    # game window at max resolution
    main_win = curses.newwin(y, x, 0, 0)
    # adding borders to the game window
    main_win.border()
    # making the getch() function non-blocking
    main_win.nodelay(1)
    # making the arrow keys available
    main_win.keypad(1)

    inp = KEY_RIGHT
    valid_inputs = [KEY_RIGHT, KEY_LEFT, KEY_DOWN, KEY_UP, ord('q')]

    # Generating random 'x' and 'y' coordenates for the snake body
    snakey_gen = randint(1, y-2)
    snakex_gen = randint(1, x-2)
    snake = [[snakey_gen, snakex_gen],
            [snakey_gen, snakex_gen - 1],
            [snakey_gen, snakex_gen - 2],
            [snakey_gen, snakex_gen - 3],
            [snakey_gen, snakex_gen - 4]]

    """
    0 = right
    1 = left
    2 = up
    3 = down
    """
    snake_dir = 0
    rev_dir = {KEY_RIGHT: KEY_LEFT, KEY_LEFT: KEY_RIGHT, KEY_UP: KEY_DOWN, KEY_DOWN: KEY_UP}

    food = [randint(1, y-2), randint(1, x-2)]

    inp = KEY_RIGHT

    prev_inp = None

    while inp != ord('q') :

        if rev_dir[inp] != prev_inp:
            prev_inp = inp

        # geting the input
        inp = main_win.getch()

        # drawing the snake on the screen
        for i in snake:
            main_win.addstr(i[0], i[1], "■")

        if inp not in valid_inputs:
            inp = prev_inp

        if inp == -1:
            inp = prev_inp

        if inp == KEY_RIGHT and prev_inp != KEY_LEFT:
            snake_dir = 0
        elif inp == KEY_LEFT and prev_inp != KEY_RIGHT : 
            snake_dir = 1
        elif inp == KEY_UP and prev_inp != KEY_DOWN:
            snake_dir = 2
        elif inp == KEY_DOWN and prev_inp != KEY_UP:
            snake_dir = 3

        if snake_dir == 0:
            snake.insert(0, [snake[0][0], snake[0][1] + (1)])
        elif snake_dir == 1:
            snake.insert(0, [snake[0][0], snake[0][1] - (1)])
        elif snake_dir == 2:
            snake.insert(0, [snake[0][0] - (1), snake[0][1]])
        elif snake_dir == 3:
            snake.insert(0, [snake[0][0] + (1), snake[0][1]])
        

        main_win.addstr(food[0], food[1], "&")

        if (snake[0][1] == food[1]) and (snake[0][0] == food[0]):
            food = [randint(1, y-2), randint(1, x-2)]
            snake.append(food)
        else:
            tail = snake.pop()
            main_win.addstr(tail[0], tail[1], ' ')

        for i in snake:
            if i[1] == x - 1: 
                i[1] = 1
                
            elif i[1] == 0:
                i[1] = x - 2

            elif i[0] == y - 1:
                i[0] = 1

            elif i[0] == 0:
                i[0] = y - 2

        if snake[0] in snake[1:]:
            inp = ord('q')

        # controling the refresh rate on the game
        main_win.timeout(int(100))

wrapper(main)
