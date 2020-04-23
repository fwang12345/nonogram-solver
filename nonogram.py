from pygame import *
from tkinter import Tk
from tkinter.filedialog import askopenfilename
from solver import read, solve
from parse import preprocess, get_patterns

BLACK = (0, 0, 0)
BLUE = (21, 34, 110)
LIGHT_BLUE = (212, 224, 248)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
SCREEN = 800                                                # size of screen
OFFSET = SCREEN / 7.5                                       # offset, think border
FONT_SIZE = int(OFFSET / 5.5)                               # font size
fname = 'images/10g_1.png'

def draw_nonogram():
    ref, row_cnts, col_cnts = 0, 0, 0
    N, rows, cols = 0, [], []
    puzzle = []

    title_pos = (SCREEN / 2, SCREEN / 4)
    button_offset = (SCREEN / (7.5), SCREEN / (10 * 2))

    # x and y is the center of the button
    x, y = SCREEN / 2, SCREEN / 2
    button_pos = (x - button_offset[0], y - button_offset[1], button_offset[0] * 2, button_offset[1] * 2)
    font_pos =  (x, y)

    # draw title screen
    loop = True
    while loop:
        for e in event.get():
            if e.type == QUIT:
                quit()
                return False
            elif e.type == MOUSEBUTTONDOWN:
                x_bounds = e.pos[0] > button_pos[0] and e.pos[0] < button_pos[0] + button_pos[2]
                y_bounds = e.pos[1] > button_pos[1] and e.pos[1] < button_pos[1] + button_pos[3]
                if (x_bounds and y_bounds and e.button == 1):
                    Tk().withdraw()
                    fname = askopenfilename()
                    print('Loading %s' %(fname))
                    try:
                        ref, row_cnts, col_cnts = preprocess(fname)
                        print('Loading pattern data')
                        N, rows, cols = get_patterns(ref, row_cnts, col_cnts)
                    except:
                        print('Non-image file detected')
                        N, rows, cols = read(fname)      
                    loop = False

        # draw background
        screen.fill(WHITE)

        # draw title
        draw_title(screen, FONT_SIZE, title_pos)

        #draw solve button
        draw_button(screen, SCREEN, OFFSET, FONT_SIZE, button_pos, font_pos, 'Choose')
        
        display.update()


    SEC = N // 5                                                # number of sections
    SLICE = 2 if N < 10 else 1.5                                # proportional size of the data blocks
    BLK = (SCREEN - 2 * OFFSET) / (N * (SEC + 1 / SLICE) / SEC) # size of one block
    DATA = N / SLICE / SEC * BLK                                # size of where the given data is


    # x and y is the center of the button
    x, y = SCREEN / 2, SCREEN - OFFSET / 2
    button_pos = (x - button_offset[0], y - button_offset[1], button_offset[0] * 2, button_offset[1] * 2)
    font_pos = (x, y)

    # draw unsolved puzzle
    loop = True
    while loop:
        for e in event.get():
            if e.type == QUIT:
                quit()
                return False
            elif e.type == MOUSEBUTTONDOWN:
                x_bounds = e.pos[0] > button_pos[0] and e.pos[0] < button_pos[0] + button_pos[2]
                y_bounds = e.pos[1] > button_pos[1] and e.pos[1] < button_pos[1] + button_pos[3]
                if (x_bounds and y_bounds and e.button == 1):
                    print('Solving puzzle')
                    puzzle = solve(N, rows, cols)
                    loop = False

        draw_one(screen, SCREEN, N, SEC, OFFSET, DATA, BLK, FONT, FONT_SIZE, rows, cols)
        draw_button(screen, SCREEN, OFFSET, FONT_SIZE, button_pos, font_pos, 'Solve')

        display.update()
    loop = True
    while loop:

        for e in event.get():
            if e.type == QUIT:
                quit()
                return False
            elif e.type == MOUSEBUTTONDOWN:
                    x_bounds = e.pos[0] > button_pos[0] and e.pos[0] < button_pos[0] + button_pos[2]
                    y_bounds = e.pos[1] > button_pos[1] and e.pos[1] < button_pos[1] + button_pos[3]
                    if (x_bounds and y_bounds and e.button == 1):
                        loop = False
        draw_one(screen, SCREEN, N, SEC, OFFSET, DATA, BLK, FONT, FONT_SIZE, rows, cols)

        # fill in correct squares
        for i in range(len(puzzle)):
            for j in range(len(puzzle[i])):
                if puzzle[i][j] != 0:
                    x = OFFSET + DATA + i * BLK
                    y = OFFSET + DATA + j * BLK
                    draw.rect(screen, BLUE, (y , x, BLK + 1, BLK + 1))
                    
        draw_button(screen, SCREEN, OFFSET, FONT_SIZE, button_pos, font_pos, 'New Puzzle')
        display.update()
    return True

def draw_button(screen, SCREEN, OFFSET, FONT_SIZE, button_pos, font_pos, text):
    TITLE_FONT = font.SysFont('comicsansms', FONT_SIZE * 2)
    button = draw.rect(screen, LIGHT_BLUE, button_pos)
    solve_text = TITLE_FONT.render(text, True, BLACK)
    position = solve_text.get_rect(center=font_pos)
    screen.blit(solve_text, position)

def draw_title(screen, FONT_SIZE, title_pos):
    TITLE_FONT = font.SysFont('comicsansms', FONT_SIZE * 2)
    title = TITLE_FONT.render('Nongram Solver', True, BLACK)
    position = title.get_rect(center=title_pos)
    screen.blit(title, position)

def draw_one(screen, SCREEN, N, SEC, OFFSET, DATA, BLK, FONT, FONT_SIZE, rows, cols):
    # draw background
    screen.fill(WHITE)

    pos = (SCREEN / 2, OFFSET / 2)
    draw_title(screen, FONT_SIZE, pos)

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

            x = OFFSET + DATA - BLK / 2 - j * BLK / 2
            y = OFFSET + DATA + BLK / 2 + i * BLK

            position = number.get_rect(center=(x, y))

            screen.blit(number, position)

    # fill in numerical col data
    for i, col in enumerate(cols):
        for j, num in enumerate(col[::-1]):
            number = FONT.render(str(num), True, BLACK)

            x = OFFSET + DATA + BLK / 2 + i * BLK
            y = OFFSET + DATA - BLK / 2 - j * BLK / 2

            position = number.get_rect(center=(x, y))

            screen.blit(number, position)

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

# initial pygame data
init()
screen = display.set_mode((SCREEN, SCREEN))
display.set_caption('Nongram Solver')
FONT = font.SysFont('comicsansms', FONT_SIZE)
cont = True
while cont:
    cont = draw_nonogram()