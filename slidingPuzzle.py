import pygame
import sys
import os
import random
import time
from queue import PriorityQueue

game_caption = 'Slide Puzzle'
background_image = 'cropped-background-image.png'

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
GAME_BACKGROUND = WHITE
FONT_COLOR = WHITE
FONT_SIZE = 40
BUTTON_COLOR = GREEN
game_start = False
is_solved = False
score_list = PriorityQueue()
score_copy = []
updated = False

class SlidePuzzle:
    prev = None
    speed = 2000
    is_random = False

    def __init__(self, gs, ts, ms):  # grid size, tile size, margin size
        self.gs, self.ts, self.ms = gs, ts, ms

        self.tiles_len = gs[0]*gs[1]-1  # Banyak tiles (kurangi 1)

        self.tiles = [(x, y) for y in range(gs[1]) for x in range(gs[0])]

        self.tilepos = [(x*(ts+ms)+ms, y*(ts+ms)+ms)
                        for y in range(gs[1]) for x in range(gs[0])]
        # actual position on screen

        self.tilePOS = {(x, y): (x*(ts+ms)+ms, y*(ts+ms)+ms)
                        for y in range(gs[1]) for x in range(gs[0])}
        # position the tiles slide into

        self.rect = pygame.Rect(0, 0, gs[0]*(ts+ms)+ms, gs[1]*(ts+ms)+ms)
        pic = pygame.image.load(background_image)
        pic = pygame.transform.smoothscale(pic, self.rect.size)

        self.images = []
        font = pygame.font.Font(None, FONT_SIZE)

        for i in range(self.tiles_len):
            # image = pygame.Surface((ts,ts))
            # image.fill(GREEN)

            x, y = self.tilepos[i]
            image = pic.subsurface(x, y, ts, ts)

            text = font.render(str(i+1), 2, FONT_COLOR)
            w, h = text.get_size()

            # image.blit(text, ((ts-w)/2,(ts-h)/2)) # text at center of grid
            image.blit(text, (0, 0))  # text at top left of grid
            self.images += [image]

    def getBlank(self): return self.tiles[-1]
    def setBlank(self, pos): self.tiles[-1] = pos
    opentile = property(getBlank, setBlank)

    def sliding(self):
        for i in range(self.tiles_len):
            x, y = self.tilepos[i]
            X, Y = self.tilePOS[self.tiles[i]]
            if x != X or y != Y:
                return True

    def switch(self, tile):  # Swap blank tile with position
        if self.sliding() and not self.is_random:
            return
        # prevent add other slide before each tile in their pos
        # but allow it when we want to random it

        # print('tile:',tile,'blank tile:', self.opentile)
        n = self.tiles.index(tile)
        self.tiles[n], self.opentile = self.opentile, self.tiles[n]
        self.prev = self.opentile

    def in_grid(self, tile):
        return tile[0] >= 0 and tile[0] < self.gs[0] and tile[1] >= 0 and tile[1] < self.gs[1]
        # to keep mouse click out of bound

    def adjacent(self):
        x, y = self.opentile
        return (x-1, y), (x+1, y), (x, y-1), (x, y+1)

    def random(self):
        self.is_random = True
        for i in range(300):
            adj = self.adjacent()
            adj = [pos for pos in adj if self.in_grid(
                pos) and pos != self.prev]
            self.switch(random.choice(adj))

    def update(self, dt):
        global game_start, is_solved, current_times, updated
        game_start = True
        mouse = pygame.mouse.get_pressed()
        mouse_pos = pygame.mouse.get_pos()

        if(mouse[0]):
            x, y = mouse_pos[0] % (
                self.ts+self.ms), mouse_pos[1] % (self.ts+self.ms)

            # print(mouse_pos)
            if RESET_RECT.collidepoint(mouse_pos):
                print('reset button')
            if RANDOM_RECT.collidepoint(mouse_pos):
                is_solved = False
                game_start = False
                main()
            if SOLVE_RECT.collidepoint(mouse_pos):
                print('solve button')

            if x > self.ms and y > self.ms:
                tile = mouse_pos[0]//self.ts, mouse_pos[1]//self.ts
                # tile is equals to clicked tiles
                # check if tile is adjacent with blank tile
                if self.in_grid(tile) and tile in self.adjacent() and not is_solved:
                    self.switch(tile)  # switch clicked with blank

        s = self.speed*dt
        for i in range(self.tiles_len):
            x, y = self.tilepos[i]   # current position
            X, Y = self.tilePOS[self.tiles[i]]   # target pos
            dx, dy = X-x, Y-y

            # if dx>0: x+=s
            # elif dx<0: x-=s
            # else: x = X
            x = X if abs(dx) < s else x+s if dx > 0 else x-s
            y = Y if abs(dy) < s else y+s if dy > 0 else y-s

            self.tilepos[i] = x, y

        if is_solved and not updated:
            updated = True
            score_list.put(current_times - start_time)

            for i in score_copy:
                print('kok double',i)
                score_list.put(i)
            i = 0
            score_copy.clear()
            while score_list.qsize() > 0:
                before = i
                i = score_list.get()
                print('ini i', i)
                if i < 1:
                    continue
                if before != i:
                    score_copy.append(i)
            print()
            for i in range(5 - len(score_copy)):
                score_copy.append(0)
            
            file = open('highscore.txt', 'w')
            for i in range(5):
                file.write(str(score_copy[i]) + '\n')
            
            file.close()

    def draw(self, screen):
        global game_start, is_solved
        for i in range(self.tiles_len):
            x, y = self.tilepos[i]
            screen.blit(self.images[i], (x, y))
            screen.blit(RESET_SURF, RESET_RECT)
            screen.blit(RANDOM_SURF, RANDOM_RECT)
            screen.blit(SOLVE_SURF, SOLVE_RECT)
            screen.blit(TIMER_SURF, TIMER_RECT)
            for a,b in SCORES_SCREEN:
                screen.blit(a,b)

            if solvedPuzzle.tiles == self.tiles:
                is_solved = True
                screen.blit(SOLVED_SURF, SOLVED_RECT)
            # pygame.draw.rect(screen, GREEN, (x,y,self.ts,self.ts))  # show grid in console

    def events(self, event):
        global game_start, is_solved
        if event.type == pygame.KEYDOWN:
            game_start = True
            self.is_random = False
            # for key, dx, dy in ((pygame.K_w,0,-1), (pygame.K_s,0,1), (pygame.K_a,-1,0), (pygame.K_d,1,0)):
            for key, dx, dy in ((pygame.K_w, 0, 1), (pygame.K_s, 0, -1), (pygame.K_a, 1, 0), (pygame.K_d, -1, 0)):
                # wasd
                if event.key == key:
                    x, y = self.opentile
                    tile = x+dx, y+dy
                    if self.in_grid(tile) and not is_solved:
                        self.switch(tile)

            # for key, dx, dy in ((pygame.K_UP,0,-1), (pygame.K_DOWN,0,1), (pygame.K_LEFT,-1,0), (pygame.K_RIGHT,1,0)):
            for key, dx, dy in ((pygame.K_UP, 0, 1), (pygame.K_DOWN, 0, -1), (pygame.K_LEFT, 1, 0), (pygame.K_RIGHT, -1, 0)):
                # arrow control
                if event.key == key:
                    x, y = self.opentile
                    tile = x+dx, y+dy
                    if self.in_grid(tile) and not is_solved:
                        self.switch(tile)

            if event.key == pygame.K_SPACE:
                is_solved = False
                game_start = False
                main()

def makeText(text, color, bgcolor, top, left):
    # create the Surface and Rect objects for some text.
    font = pygame.font.Font(None, FONT_SIZE)
    textSurf = font.render(text, True, color, bgcolor)
    textRect = textSurf.get_rect()
    textRect.topleft = (top, left)
    return (textSurf, textRect)

def second_to_str(seconds):
    hours = (seconds//3600)
    minutes = (seconds//60)
    seconds %= 60

    res = ""
    if hours < 10:
        res += "0"
    res = res + "{:.0f}".format(hours) + ":"

    if minutes < 10:
        res += "0"
    res = res + "{:.0f}".format(minutes) + ":"

    if seconds < 10:
        res += "0"
    seconds = "{:.2f}".format(seconds)

    res += seconds
    return res

def highscores():
    global start_time, is_solved, current_times, SCORES_SCREEN

    SCORES_SCREEN = []
    file = open('highscore.txt', 'r')

    for highscore in file:
        score_list.put(float(highscore))

    while score_list.qsize() > 0:
        i = score_list.get()
        if i < 1:
            continue
        score_copy.append(i)
    for i in range(5 - len(score_copy)):
        score_copy.append(0)

    for i in range(5):
        SCORES_SCREEN.append(makeText(
                second_to_str(score_copy[i]), BLACK, WHITE, game_width - right_button*1.75, 70 + 30 * i))
    file.close()

def main():
    global RESET_SURF, RESET_RECT, RANDOM_SURF, RANDOM_RECT, SOLVE_SURF, SOLVE_RECT, SOLVED_SURF, SOLVED_RECT
    global TIMER_SURF, TIMER_RECT, SCORES_SCREEN
    global tile_size, PuzzleSize, grid_margin, right_button, game_height, game_width
    global solvedPuzzle, current_times, start_time, updated

    tile_size = 160
    PuzzleSize = (4, 4)
    grid_margin = 5
    right_button = 120
    game_height = tile_size*(PuzzleSize[0])+grid_margin*(PuzzleSize[0]+1)
    game_width = tile_size * \
        (PuzzleSize[1])+grid_margin*(PuzzleSize[1]+1) + 2*right_button
    updated = False

    pygame.init()
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    pygame.display.set_caption(game_caption)
    
    screen = pygame.display.set_mode((game_width, game_height))
    fpsclock = pygame.time.Clock()
    program = SlidePuzzle(PuzzleSize, tile_size, grid_margin)
    program.random()
    solvedPuzzle = SlidePuzzle(PuzzleSize, tile_size, grid_margin)
    
    RANDOM_SURF, RANDOM_RECT = makeText(
        'Random', FONT_COLOR, BUTTON_COLOR, game_width - right_button*1.5, game_height - 60)
    SOLVE_SURF,  SOLVE_RECT = makeText(
        'Solve',    FONT_COLOR, BUTTON_COLOR, game_width - right_button*1.5, game_height - 30)
    RESET_SURF,  RESET_RECT = makeText(
        'Reset',    FONT_COLOR, BUTTON_COLOR, game_width - right_button*1.5, game_height - 90)
    SOLVED_SURF, SOLVED_RECT = makeText(
        'SOLVED', FONT_COLOR, BUTTON_COLOR, game_width - right_button*1.5, 35)
    start_time = time.time()
    highscores()
    
    while True:
        dt = fpsclock.tick()/1000
        if not is_solved:
            current_times = time.time()
        
        TIMER_SURF, TIMER_RECT = makeText(
                second_to_str(current_times - start_time), BLACK, WHITE, game_width - right_button*1.75, 5)
        
        screen.fill(GAME_BACKGROUND)
        program.draw(screen)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            program.events(event)

        program.update(dt)


if __name__ == '__main__':
    main()
