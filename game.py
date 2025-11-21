import pygame
pygame.init()
screen = pygame.display.set_mode((1000, 600))
pygame.display.set_caption("Simple Game Loop")
clock = pygame.time.Clock()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill((0, 0, 0))
    # Grenzposition
    boundary_x = 600

    # Vertikale Linie zeichnen
    pygame.draw.line(screen, (255, 255, 255), (boundary_x, 0), (boundary_x, 600), 2)

    pygame.display.flip()
    clock.tick(60)
pygame.quit()