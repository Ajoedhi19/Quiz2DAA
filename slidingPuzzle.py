import pygame, sys, os

game_height = 800
game_width = 600
PuzzleSize = (3,3)

game_caption = 'Slide Puzzle'

BLACK = (0,0,0)
GREEN = (0, 255, 0)

class SlidePuzzle:
    def __init__(self, gs, ts, ms): # grid size, tile size, margin size
        self.gs, self.ts, self.ms = gs, ts, ms

        self.tiles_len = gs[0]*gs[1]-1  #  Banyak tiles (kurangi 1)

        self.tiles = [(x, y) for y in range(gs[1]) for x in range(gs[0])]

        self.tilepos = {(x, y):(x*(ts+ms)+ms,y*(ts+ms)+ms) 
            for y in range(gs[1]) for x in range(gs[0])}    # creating grid

        self.images = []
        font = pygame.font.Font(None, 120)

        for i in range(self.tiles_len):
            image = pygame.Surface((ts,ts))
            image.fill(GREEN)

            text = font.render(str(i+1), 2, BLACK)
            w,h = text.get_size()

            image.blit(text, ((ts-w)/2,(ts-h)/2))   
            self.images += [image]

    def getBlank(self): return self.tiles[-1]
    def setBlank(self, pos): self.tiles[-1] = pos
    opentile = property(getBlank, setBlank)

    def switch(self, tile): # Swap blank tile with position
        n = self.tiles.index(tile)
        self.tiles[n], self.opentile = self.opentile, self.tiles[n]
        
    def update(self, dt):
        pass

    def draw(self, screen):
        for i in range(self.tiles_len):
            x,y = self.tilepos[self.tiles[i]]
            screen.blit(self.images[i], (x,y))
            # pygame.draw.rect(screen, GREEN, (x,y,self.ts,self.ts))  # show grid in console

            
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

        screen.fill(BLACK)
        program.draw(screen)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()

        program.update(dt)

if __name__ == '__main__':
    main()
