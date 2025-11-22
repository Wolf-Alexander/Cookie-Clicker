import pygame
import pygame_widgets
from pygame_widgets.button import Button

pygame.init()
screen = pygame.display.set_mode((1000, 600))
pygame.display.set_caption("Simple Game Loop")

# Lade das Cursorbild von GitHub
cursor_image = pygame.image.load("Baby_Opener.png")  # gespeicherter cursor
cursor_image = pygame.transform.scale(cursor_image, (100, 100))  # Größe vom Öffner
cursor_rect = cursor_image.get_rect()

# Setze den Mauszeiger standardmäßig unsichtbar
pygame.mouse.set_visible(False)

class ShopButton:
    def __init__(self, screen, x, y, width, height, name, price):
        self.screen = screen
        self.name = name
        self.price = price
        self.font = pygame.font.Font(None, 24)

        # pygame_widgets Button
        self.button = Button(
            screen, x, y, width, height,
            text=name,
            textHAlign="left"
        )

        # Position des Preis-Textes
        self.price_pos = (x + width - 50, y + 5)

    def draw_price(self):
        price_surface = self.font.render(str(self.price), True, (255, 255, 255))
        self.screen.blit(price_surface, self.price_pos)

    def set_price(self, new_price):
        self.price = new_price


button1 = ShopButton(screen, 650, 100, 300, 30,"Upgrade Bottle", 10)
button2 = ShopButton(screen, 650, 140, 300, 30,"Stronger Clicks", 20)
button3 = ShopButton(screen, 650, 180, 300, 30,"Double-Click Chance", 30)
button4 = ShopButton(screen, 650, 400, 300, 30,"Passive Income", 40)
button5 = ShopButton(screen, 650, 440, 300, 30,"Production Boost", 50)
button6 = ShopButton(screen, 650, 480, 300, 30,"Bottle Factory", 60)

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


    # Vertikale Linie zeichnen
    pygame.draw.line(screen, (255, 255, 255), (boundary_x, 0), (boundary_x, 600), 2)

    pygame_widgets.update(events)

    font = pygame.font.Font(None, 36)   # Schriftart & Größe
    text_surface = font.render("Store", True, (255, 255, 255))  # Text, Anti-Alias, Farbe
    screen.blit(text_surface, (750, 10))   # Text an (x, y) zeichnen


    pygame.display.flip()
    clock.tick(60)
pygame.quit()
