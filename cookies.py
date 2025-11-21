
import pygame
import cookie
import math


# --- variables

FPS = 60


# --- classes ---

class Cookies:
    def __init__ (self, amount, radius):
        self.image = pygame.image.load('cookie.png')
        self.amount = amount
        self.poss = []
        for i in range(self.amount):
            self.poss.append([
                math.cos((360/amount) * i) * radius,
                math.sin((360/amount) * i) * radius
                ])

    def draw (self, display):
        for i in range(self.amount):
            display.blit(self.image, self.poss[i][0], self.poss[i][1])


# --- functions ---

def draw ():
    screen.fill("#202020")
    cookies_arr.draw(screen)


# --- main ---

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((1000, 600))
    pygame.display.set_caption("cookie clicker")
    clock = pygame.time.Clock()
    dt = 0
    cookies_arr = Cookies(5, 10)

    running = True
    while running:
        # poll for events
        # pygame.QUIT event means the user clicked X to close your window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # draw
        draw()

        # key events
        keys = pygame.key.get_pressed()
        # example: if keys[pygame.K_w]: print("w pressed")

        # update display
        pygame.display.flip()

        # limits FPS to 60
        dt = clock.tick(FPS) / 1000

    pygame.quit()

