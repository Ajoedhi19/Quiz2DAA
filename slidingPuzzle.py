import pygame, sys, os

game_height = 800
game_width = 600

BLACK = (0,0,0)

def main():
    pygame.init()
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    pygame.display.set_caption('Slide Puzzle')
    screen = pygame.display.set_mode((game_width, game_height))
    fpsclock = pygame.time.Clock()

    while True:
        screen.fill(BLACK)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()


if __name__ == '__main__':
    main()
