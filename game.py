import pygame
import pygame_widgets
from pygame_widgets.button import Button

pygame.init()
screen = pygame.display.set_mode((1000, 600))
pygame.display.set_caption("Simple Game Loop")

button = Button(screen, 100, 100, 300, 150)

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

    pygame.display.flip()
    clock.tick(60)
pygame.quit()
