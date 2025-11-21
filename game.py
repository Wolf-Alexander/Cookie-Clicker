import pygame
import pygame_widgets
from pygame_widgets.button import Button

pygame.init()
screen = pygame.display.set_mode((1000, 600))
pygame.display.set_caption("Simple Game Loop")

class shop_button:
    def __init__(self, screen, x, y, width, height, text=" "):
        self.button = Button(screen, x, y, width, height, text=text)

button1 = shop_button(screen, 650, 70, 300, 30,"Buy Now")
button2 = shop_button(screen, 650, 110, 300, 30,"Buy Now")
button3 = shop_button(screen, 650, 150, 300, 30,"Buy Now")
button4 = shop_button(screen, 650, 190, 300, 30,"Buy Now")

clock = pygame.time.Clock()
running = True
while running:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False
    screen.fill((0, 0, 0))
    # Grenzposition
    boundary_x = 600

    # Vertikale Linie zeichnen
    pygame.draw.line(screen, (255, 255, 255), (boundary_x, 0), (boundary_x, 600), 2)

    pygame_widgets.update(events)

    font = pygame.font.Font(None, 36)   # Schriftart & Größe
    text_surface = font.render("Store", True, (255, 255, 255))  # Text, Anti-Alias, Farbe
    screen.blit(text_surface, (750, 10))   # Text an (x, y) zeichnen


    pygame.display.flip()
    clock.tick(60)
pygame.quit()
