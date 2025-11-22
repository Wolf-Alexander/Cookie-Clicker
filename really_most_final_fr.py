
import pygame
import pygame_widgets
from pygame_widgets.button import Button as WidgetButton
import math

# --- Globale Variablen ---
toggle = 1
soundV = 0
FPS = 60
display_width = 1000
display_height = 600
money = 0  # Geld/Punkte Zähler
click_value = 1  # Wert pro Klick
passive_income = 0

pygame.init()
screen = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption("Cookie Clicker Game")
clock = pygame.time.Clock()

# Lade das Cursorbild
cursor_image = pygame.image.load("Assets/Öffner/Baby_Opener.png")
cursor_image = pygame.transform.scale(cursor_image, (100, 100))
cursor_rect = cursor_image.get_rect()

# Setze den Mauszeiger standardmäßig unsichtbar
pygame.mouse.set_visible(False)

# --- Klassen aus cookies.py ---

class Button:
    def __init__(self, image_unpressed, image_pressed, pos, clicked_scale):
        self.image_unpressed = image_unpressed
        self.image_pressed = image_pressed
        self.image = self.image_unpressed
        rect = self.image.get_rect()
        self.dimensions = (rect[2], rect[3])
        self.pos = pos
        self.clicked_scale = clicked_scale
        self.scale = 1

    def under_mouse(self, cursor):
        return (
            (cursor[0] >= self.pos[0] - self.dimensions[0]/2) &
            (cursor[0] <= self.pos[0] + self.dimensions[0]/2) &
            (cursor[1] >= self.pos[1] - self.dimensions[1]/2) &
            (cursor[1] <= self.pos[1] + self.dimensions[1]/2) 
        )

    def handle_mouse(self, cursor, clicked, pressed):
        if not pressed:
            self.image = self.image_unpressed
            self.scale = 1
        if clicked & self.under_mouse(cursor):
            self.image = self.image_pressed
            self.scale = self.clicked_scale
            self.click_action()
    
    def click_action(self):
        print("pressed")

    def get_frame_image(self):
        frame_scale = (
            self.image_unpressed.get_rect()[2] * self.scale,
            self.image_unpressed.get_rect()[3] * self.scale
        )
        return pygame.transform.scale(self.image, frame_scale)

    def draw(self, display):
        image = self.get_frame_image()
        box = image.get_rect()
        display.blit(image, (
            self.pos[0] - box[2]/2,
            self.pos[1] - box[3]/2
        ))


class Button_Toggle(Button):
    def __init__(self, image_unpressed, image_pressed, pos, clicked_scale):
        super().__init__(image_unpressed, image_pressed, pos, clicked_scale)
        self.toggled = True

    def handle_mouse(self, cursor, clicked, pressed):
        if not pressed:
            self.scale = 1

        if pressed & self.under_mouse(cursor):
            self.scale = self.clicked_scale

        if clicked & self.under_mouse(cursor):
            if self.toggled:
                self.toggled = False
                self.image = self.image_pressed
                self.click_action()
            else:
                self.toggled = True
                self.image = self.image_unpressed
                self.unclick_action()

    def unclick_action(self):
        pass


class Cookie(Button):
    def __init__(self, image, image_pressed, pos, clicked_scale, id):
        super().__init__(image, image_pressed, pos, clicked_scale)
        self.id = id
        self.rot = 0
        self.rot_vel = 0

    def click_action(self):
        global money, click_value
        money += click_value  # Geld hinzufügen
        self.rot_vel += 4

    def physics_ig(self):
        self.rot_vel *= 0.96
        self.rot += self.rot_vel

    def get_frame_image(self):
        frame_scale = (
            self.image_unpressed.get_rect()[2] * self.scale,
            self.image_unpressed.get_rect()[3] * self.scale
        )
        tmp_img = pygame.transform.scale(self.image, frame_scale)
        return pygame.transform.rotate(tmp_img, self.rot)


class Cookies:
    def __init__(self, amount, radius, pos=(0, 0)):
        self.pos = pos
        self.image = pygame.image.load('Assets/Flaschen/ClubMate.png')
        self.image = pygame.transform.scale(self.image, (600, 250))
        self.image_clicked = pygame.image.load('Assets/Flaschen/ClubMate.png')
        self.image_clicked = pygame.transform.scale(self.image_clicked, (600, 250))
        self.amount = amount

        if amount == 1:
            radius = 0

        self.cookies = []
        for i in range(self.amount):
            self.cookies.append(Cookie(
                image=self.image,
                image_pressed=self.image_clicked,
                pos=(
                    math.cos(((2*math.pi)/amount) * i) * radius + self.pos[0],
                    math.sin(((2*math.pi)/amount) * i) * radius + self.pos[1]
                ),
                id=i,
                clicked_scale=0.8
            ))

    def draw(self, display):
        for i in range(self.amount):
            self.cookies[i].draw(display)

    def handle_mouse(self, cursor, click, pressed):
        for i in range(self.amount):
            self.cookies[i].handle_mouse(cursor, click, pressed)

    def do_stuff(self):
        for i in range(self.amount):
            self.cookies[i].physics_ig()


# --- Shop Button Klasse ---

class ShopButton:
    def __init__(self, screen, x, y, width, height, name, price, callback=None):
        self.screen = screen
        self.name = name
        self.price = price
        self.callback = callback
        self.font = pygame.font.Font(None, 24)
        self.button = WidgetButton(
            screen, x, y, width, height,
            text=name,
            textHAlign="left",
            onClick=self.on_click
        )
        self.price_pos = (x + width - 50, y + 5)

    def on_click(self):
        global money
        if money >= self.price:
            money -= self.price
            if self.callback:
                self.callback()
        else:
            pass  # Nicht genug Geld - keine Aktion

    def draw_price(self):
        price_surface = self.font.render(str(self.price), True, (255, 255, 255))
        self.screen.blit(price_surface, self.price_pos)

    def set_price(self, new_price):
        self.price = new_price


# --- Upgrade Funktionen ---

def upgrade_bottle():
    global click_value
    click_value += 1

def upgrade_stronger_clicks():
    global click_value
    click_value += 2

def upgrade_double_click():
    global click_value
    click_value *= 2

def upgrade_passive_income():
    global passive_income
    passive_income += 1

def upgrade_production_boost():
    global passive_income
    passive_income *= floor(1.1)

def upgrade_bottle_factory():
    global passive_income
    passive_income += 8

# --- Initialisierung ---

# Cookie Clicker Setup
cookies_arr = Cookies(
    amount=1,
    radius=100,
    pos=(300, display_height / 2)
)

# Control Buttons (Audio, Retry)

control_buttons = []
"""
control_buttons.append(Button_Toggle(
    pygame.image.load("audio_on.png"),
    pygame.image.load("audio_off.png"),
    (60, display_height - 60),
    0.9
))
control_buttons.append(Button(
    pygame.image.load("retry.png"),
    pygame.image.load("retry.png"),
    (180, display_height - 60),
    0.9
))
"""

# Shop Buttons
shop_buttons = []
shop_buttons.append(ShopButton(screen, 650, 100, 300, 30, "Upgrade Bottle", 10, upgrade_bottle))
shop_buttons.append(ShopButton(screen, 650, 140, 300, 30, "Stronger Clicks", 20, upgrade_stronger_clicks))
shop_buttons.append(ShopButton(screen, 650, 180, 300, 30, "Double-Click Chance", 30, upgrade_double_click))
shop_buttons.append(ShopButton(screen, 650, 400, 300, 30, "Passive Income", 40, upgrade_passive_income))
shop_buttons.append(ShopButton(screen, 650, 440, 300, 30, "Production Boost", 50, upgrade_production_boost))
shop_buttons.append(ShopButton(screen, 650, 480, 300, 30, "Bottle Factory", 60, upgrade_bottle_factory))

# Audio
sound = pygame.mixer.Sound("Assets/sounds/background music.mp3")

# --- Main Game Loop ---

running = True
while running:
    events = pygame.event.get()
    mouse = pygame.mouse.get_pos()
    mouse_click = False
    
    for event in events:
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_click = True
            mouse_pos = event.pos
            # Speaker Button Check
            if rect.collidepoint(mouse_pos):
                print("Speaker angeklickt!")
                toggle = toggle * -1
        if event.type == pygame.QUIT:
            running = False
    
    # Audio Control
    if toggle == 1 and not soundV == 1:
        sound.play()
        soundV = 1
    if toggle == -1: 
        sound.stop()
        soundV = 0
    
    # Screen Clear
    screen.fill((255, 255, 255))
    
    # Grenzlinie
    boundary_x = 600
    mouse_x, mouse_y = mouse
    
    # Custom Cursor Logic
    if mouse_x < 600:
        cursor_rect.center = (mouse_x, mouse_y)
        pygame.mouse.set_visible(False)
        pygame.draw.line(screen, (0, 0, 0), (600, 0), (600, 600), 2)
    else:
        pygame.mouse.set_visible(True)
        pygame.draw.line(screen, (0, 0, 0), (600, 0), (600, 600), 2)
    
    # Cookie Clicker Mechanics (nur auf linker Seite)
    if mouse_x < 600:
        cookies_arr.handle_mouse(mouse, mouse_click, pygame.mouse.get_pressed()[0])
    cookies_arr.do_stuff()
    
    # Draw Cookies
    cookies_arr.draw(screen)
    
    # Draw Control Buttons
    for button in control_buttons:
        button.handle_mouse(mouse, mouse_click, pygame.mouse.get_pressed()[0])
        button.draw(screen)
    
    # Geld-Anzeige (ganz oben links)
    money_font = pygame.font.Font(None, 48)
    money_text = money_font.render(f"${money}", True, (0, 180, 0))
    screen.blit(money_text, (20, 10))
    
    # Click Value Anzeige (darunter)
    value_font = pygame.font.Font(None, 32)
    value_text = value_font.render(f"+${click_value} per click", True, (100, 100, 100))
    screen.blit(value_text, (20, 60))

    # passive income Anzeige (darunter)
    value_font = pygame.font.Font(None, 32)
    value_text = value_font.render(f"+${passive_income / FPS} per second", True, (100, 100, 100))
    screen.blit(value_text, (20, 150))
    
    # Speaker Icon
    if toggle == -1:
        image = pygame.image.load("Assets/SpeakerWithX.png")
    else:
        image = pygame.image.load("Assets/Speaker.png")
    x, y = 530, 25
    image = pygame.transform.scale(image, (40, 40))
    rect = image.get_rect()
    rect.topleft = (x, y)
    screen.blit(image, (x, y))
    
    # Shop UI
    pygame_widgets.update(events)
    
    font = pygame.font.Font(None, 36)
    text_surface = font.render("Store", True, (0, 0, 0))
    screen.blit(text_surface, (750, 10))
    
    for shop_btn in shop_buttons:
        shop_btn.draw_price()
    
    # Custom Cursor (über allem)
    if mouse_x < 600:
        screen.blit(cursor_image, cursor_rect)

    # passive income
    money += passive_income
    
    # Update Display
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()

