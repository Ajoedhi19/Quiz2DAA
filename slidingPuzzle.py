import pygame, sys, os, random

game_height = 800
game_width = 800
PuzzleSize = (4,4)

game_caption = 'Slide Puzzle'
background_image = 'cropped-background-image.png'

BLACK = (0,0,0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
GAME_BACKGROUND = WHITE
FONT_COLOR = WHITE
FONT_SIZE = 40

class SlidePuzzle:
    def __init__(self, gs, ts, ms): # grid size, tile size, margin size
        self.gs, self.ts, self.ms = gs, ts, ms

        self.tiles_len = gs[0]*gs[1]-1  #  Banyak tiles (kurangi 1)

        self.tiles = [(x, y) for y in range(gs[1]) for x in range(gs[0])]

        self.tilepos = {(x, y):(x*(ts+ms)+ms,y*(ts+ms)+ms) 
            for y in range(gs[1]) for x in range(gs[0])}    # creating grid
        
        self.prev = None

        w,h = gs[0]*(ts+ms)+ms, gs[1]*(ts+ms)+ms
        pic = pygame.image.load(background_image)
        pic = pygame.transform.scale(pic, (w,h))

        self.images = []
        font = pygame.font.Font(None, FONT_SIZE)

        for i in range(self.tiles_len):
            # image = pygame.Surface((ts,ts))
            # image.fill(GREEN)

            x,y = self.tilepos[self.tiles[i]]
            image = pic.subsurface(x,y,ts,ts)

            text = font.render(str(i+1), 2, FONT_COLOR)
            w,h = text.get_size()

            # image.blit(text, ((ts-w)/2,(ts-h)/2)) # text at center of grid
            image.blit(text, (0,0)) # text at top left of grid
            self.images += [image]

    def getBlank(self): return self.tiles[-1]
    def setBlank(self, pos): self.tiles[-1] = pos
    opentile = property(getBlank, setBlank)

    def switch(self, tile): # Swap blank tile with position
        n = self.tiles.index(tile)
        self.tiles[n], self.opentile = self.opentile, self.tiles[n]
        self.prev = self.opentile
        
    def in_grid(self, tile):
        return tile[0]>=0 and tile[0]<self.gs[0] and tile[1]>=0 and tile[1]<self.gs[1]
        # to keep mouse click out of bound

    def adjacent(self):
        x,y = self.opentile
        return (x-1,y),(x+1,y),(x,y-1),(x,y+1)
        
    def random(self):
        adj = self.adjacent()
        adj = [pos for pos in adj if self.in_grid(pos) and pos != self.prev]
        self.switch(random.choice(adj))

    def update(self, dt):
        mouse = pygame.mouse.get_pressed()
        mouse_pos = pygame.mouse.get_pos()

        if(mouse[0]):
            x,y = mouse_pos[0]%(self.ts+self.ms), mouse_pos[1]%(self.ts+self.ms)

            if x>self.ms and y > self.ms:
                tile = mouse_pos[0]//self.ts, mouse_pos[1]//self.ts
                # tile is equals to clicked tiles
                if self.in_grid(tile) and tile in self.adjacent(): # check if tile is adjacent with blank tile
                    self.switch(tile)    #switch clicked with blank

    def draw(self, screen):
        for i in range(self.tiles_len):
            x,y = self.tilepos[self.tiles[i]]
            screen.blit(self.images[i], (x,y))
            # pygame.draw.rect(screen, GREEN, (x,y,self.ts,self.ts))  # show grid in console

    def events(self, event):
        if event.type == pygame.KEYDOWN:
            # for key, dx, dy in ((pygame.K_w,0,-1), (pygame.K_s,0,1), (pygame.K_a,-1,0), (pygame.K_d,1,0)):
            for key, dx, dy in ((pygame.K_w,0,1), (pygame.K_s,0,-1), (pygame.K_a,1,0), (pygame.K_d,-1,0)):
                # wasd
                if event.key == key:
                    x,y = self.opentile
                    tile = x+dx, y+dy
                    if self.in_grid(tile): self.switch(tile)

            # for key, dx, dy in ((pygame.K_UP,0,-1), (pygame.K_DOWN,0,1), (pygame.K_LEFT,-1,0), (pygame.K_RIGHT,1,0)):
            for key, dx, dy in ((pygame.K_UP,0,1), (pygame.K_DOWN,0,-1), (pygame.K_LEFT,1,0), (pygame.K_RIGHT,-1,0)):
                # arrow control
                if event.key == key:
                    x,y = self.opentile
                    tile = x+dx, y+dy
                    if self.in_grid(tile): self.switch(tile)

            if event.key == pygame.K_SPACE:
                for i in range(300): self.random()

 
def main():
    tile_size = 160

    pygame.init()
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    pygame.display.set_caption(game_caption)
    screen = pygame.display.set_mode((game_width, game_height))
    fpsclock = pygame.time.Clock()
    program = SlidePuzzle(PuzzleSize, tile_size, 5)

    while True:
        dt = fpsclock.tick()/1000

        screen.fill(GAME_BACKGROUND)
        program.draw(screen)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()
            program.events(event)

        program.update(dt)

if __name__ == '__main__':
    main()
