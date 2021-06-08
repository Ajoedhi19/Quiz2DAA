import pygame
import sys
import os
import random

game_caption = 'Slide Puzzle'
background_image = 'cropped-background-image.png'

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
GAME_BACKGROUND = WHITE
FONT_COLOR = WHITE
FONT_SIZE = 40


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
        adj = self.adjacent()
        adj = [pos for pos in adj if self.in_grid(pos) and pos != self.prev]
        self.switch(random.choice(adj))

    def update(self, dt):
        mouse = pygame.mouse.get_pressed()
        mouse_pos = pygame.mouse.get_pos()

        if(mouse[0]):
            x, y = mouse_pos[0] % (
                self.ts+self.ms), mouse_pos[1] % (self.ts+self.ms)

            if x > self.ms and y > self.ms:
                tile = mouse_pos[0]//self.ts, mouse_pos[1]//self.ts
                # tile is equals to clicked tiles
                # check if tile is adjacent with blank tile
                if self.in_grid(tile) and tile in self.adjacent():
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

    def draw(self, screen):
        for i in range(self.tiles_len):
            x, y = self.tilepos[i]
            screen.blit(self.images[i], (x, y))
            # pygame.draw.rect(screen, GREEN, (x,y,self.ts,self.ts))  # show grid in console

    def events(self, event):
        if event.type == pygame.KEYDOWN:
            self.is_random = False
            # for key, dx, dy in ((pygame.K_w,0,-1), (pygame.K_s,0,1), (pygame.K_a,-1,0), (pygame.K_d,1,0)):
            for key, dx, dy in ((pygame.K_w, 0, 1), (pygame.K_s, 0, -1), (pygame.K_a, 1, 0), (pygame.K_d, -1, 0)):
                # wasd
                if event.key == key:
                    x, y = self.opentile
                    tile = x+dx, y+dy
                    if self.in_grid(tile):
                        self.switch(tile)

            # for key, dx, dy in ((pygame.K_UP,0,-1), (pygame.K_DOWN,0,1), (pygame.K_LEFT,-1,0), (pygame.K_RIGHT,1,0)):
            for key, dx, dy in ((pygame.K_UP, 0, 1), (pygame.K_DOWN, 0, -1), (pygame.K_LEFT, 1, 0), (pygame.K_RIGHT, -1, 0)):
                # arrow control
                if event.key == key:
                    x, y = self.opentile
                    tile = x+dx, y+dy
                    if self.in_grid(tile):
                        self.switch(tile)

            if event.key == pygame.K_SPACE:
                for i in range(300):
                    self.random()


def main():
    tile_size = 160
    PuzzleSize = (3, 3)
    grid_margin = 5
    game_height = tile_size*(PuzzleSize[0])+grid_margin*(PuzzleSize[0]+1)
    game_width = tile_size*(PuzzleSize[1])+grid_margin*(PuzzleSize[1]+1)

    pygame.init()
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    pygame.display.set_caption(game_caption)
    screen = pygame.display.set_mode((game_width, game_height))
    fpsclock = pygame.time.Clock()
    program = SlidePuzzle(PuzzleSize, tile_size, grid_margin)

    while True:
        dt = fpsclock.tick()/1000

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