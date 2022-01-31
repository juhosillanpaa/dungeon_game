import pygame
import numpy as np
import pygame_gui

from Classes.Game.Game import Game


WHITE = (255, 255, 255)
FPS = 60
GREY = pygame.Color(200, 200, 200)
DARK = pygame.Color(50,50,50)



def main():


    pygame.init()
    pygame.display.set_caption("Tower defense")
    window = pygame.display.set_mode((800, 800))

    clock = pygame.time.Clock()
    run = True



    game = Game(game_surface=window)




    while run:
        time_delta = clock.tick(FPS) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    print('pause')
                    exit()
            game.listen_mouse_presses(event)

        game.run_iteration()
        window.fill(DARK)

        game.draw()
        pygame.display.update()
    pygame.quit()


if __name__ == '__main__':
    main()
