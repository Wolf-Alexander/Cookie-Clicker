import pygame
import pygame_widgets
from pygame_widgets.button import Button
from io import BytesIO

pygame.init()
screen = pygame.display.set_mode((1000, 600))
pygame.display.set_caption("Simple Game Loop")

button = Button(screen, 100, 100, 300, 150)

# Lade das Cursorbild von GitHub
cursor_image = pygame.image.load("/home/skuser/Desktop/Cookie-Clicker/Assets/Öffner/Baby_Opener.png")  # gespeicherter cursor
cursor_image = pygame.transform.scale(cursor_image, (100, 100))  # Größe vom Öffner
cursor_rect = cursor_image.get_rect()

# Setze den Mauszeiger standardmäßig unsichtbar
pygame.mouse.set_visible(False)

clock = pygame.time.Clock()
running = True
while running:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False

    # Mausposition abrufen
    mouse_x, mouse_y = pygame.mouse.get_pos()

    # Wenn die Maus links von der Grenze ist, bleibt der benutzerdefinierte Cursor sichtbar
    if mouse_x < 600:
        # Zeige benutzerdefinierten Cursor
        cursor_rect.center = (mouse_x, mouse_y)
        screen.fill((0, 0, 0))
        pygame.draw.line(screen, (255, 255, 255), (600, 0), (600, 600), 2)
        pygame.mouse.set_visible(False)
        screen.blit(cursor_image, cursor_rect)  # Zeige den benutzerdefinierten Cursor
    else:
        # Wenn die Maus über der Grenze ist, wird der benutzerdefinierte Cursor unsichtbar
        # Nur der Standard-Mauscursor ist unsichtbar
        pygame.mouse.set_visible(True)
        screen.fill((0, 0, 0))
        pygame.draw.line(screen, (255, 255, 255), (600, 0), (600, 600), 2)

    pygame_widgets.update(events)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
