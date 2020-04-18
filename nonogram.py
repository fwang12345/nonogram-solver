from pygame import *
from pygame_gui import *
from solver import read, solve
from parse import preprocess, get_patterns

BLACK = (0, 0, 0)
BLUE = (21, 34, 110)
LIGHT_BLUE = (212, 224, 248)
WHITE = (255, 255, 255)
fname = 'images/test4.png'

def draw_nonogram(size):
    SCREEN = size                                               # size of screen
    OFFSET = SCREEN / 10                                        # offset, think border
    FONT_SIZE = int(OFFSET / 5)                                 # font size
    init()
    screen = display.set_mode((SCREEN, SCREEN))
    manager = UIManager((SCREEN, SCREEN))
    display.set_caption('Nongram Solver')
    FONT = font.SysFont('comicsansms', FONT_SIZE)

    hello_button = elements.UIButton(relative_rect=pygame.Rect((350, 275), (100, 50)), text='Say Hello', manager=manager)

    # Get contours for image
    ref, row_cnts, col_cnts = preprocess(fname)
    # Get patterns from contours
    N, rows, cols = get_patterns(ref, row_cnts, col_cnts)
    SEC = N // 5
    print('Loaded %d x %d puzzle' %(N, N))
    print('Rows')
    for i in rows:
        print(i)
    print('Columns')
    for i in cols:
        print(i)
    puzzle = solve(N, rows, cols)

    SLICE = 2 if N < 10 else 1.5                                # proportional size of the data blocks
    BLK = (SCREEN - 2 * OFFSET) / (N * (SEC + 1 / SLICE) / SEC) # size of one block
    DATA = N / SLICE / SEC * BLK                                # size of where the given data is

    while True:

        for e in event.get():
            if e.type == QUIT:
                quit()

        # draw background
        screen.fill(WHITE)

        # draw rectangles for were the given rows and columns will be drawn
        draw.rect(screen, LIGHT_BLUE, (OFFSET, OFFSET + DATA, DATA - 4, BLK * N))
        draw.rect(screen, LIGHT_BLUE, (OFFSET + DATA, OFFSET, BLK * N, DATA - 4))

        # slice rectangles
        for i in range(1, N):
            sta = OFFSET + DATA
            inc = i * BLK + sta
            end = OFFSET
            draw.lines(screen, WHITE, False, [(sta, inc), (end, inc)])
            draw.lines(screen, WHITE, False, [(inc, sta), (inc, end)])

        # fill in numerical row data
        for i, row in enumerate(rows):
            for j, num in enumerate(row[::-1]):
                number = FONT.render(str(num), True, BLACK)

                x = OFFSET + DATA - BLK / 2 - j * BLK / 3
                y = OFFSET + DATA + BLK / 2 + i * BLK

                position = number.get_rect(center=(x, y))

                screen.blit(number, position)

        # fill in numerical col data
        for i, col in enumerate(cols):
            for j, num in enumerate(col[::-1]):
                number = FONT.render(str(num), True, BLACK)

                x = OFFSET + DATA + BLK / 2 + i * BLK
                y = OFFSET + DATA - BLK / 2 - j * BLK / 2.4

                position = number.get_rect(center=(x, y))

                screen.blit(number, position)

        # fill in correct squares
        for i in range(len(puzzle)):
            for j in range(len(puzzle[i])):
                if puzzle[i][j] != 0:
                    x = OFFSET + DATA + i * BLK
                    y = OFFSET + DATA + j * BLK
                    draw.rect(screen, BLUE, (y , x, BLK + 1, BLK + 1))

        # draw grid lines
        for i in range(0, N + 1):
            sta = OFFSET + DATA
            inc = i * BLK + sta
            end = SCREEN - OFFSET
            
            if i == 0 or i == N:
                thickness = 5
            elif i % (N / SEC) == 0:
                thickness = 3
            else:
                thickness = 1
            
            draw.lines(screen, BLACK, False, [(sta, inc), (end, inc)], thickness)
            draw.lines(screen, BLACK, False, [(inc, sta), (inc, end)], thickness)

        display.update()

draw_nonogram(700)