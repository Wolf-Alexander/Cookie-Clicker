
import pygame
import cookie
import math


# --- variables

FPS = 60
display_width = 1000
display_height = 600


# --- classes ---

class Button:
    def __init__ (self, image_unpressed, image_pressed, pos, pressed_size):
        self.image_unpressed = image_unpressed
        self.image_pressed = image_pressed
        self.image = self.image_unpressed
        rect = self.image.get_rect()
        self.dimensions = (rect[2], rect[3])
        self.pos = pos
        self.pressed_size = pressed_size

    def under_mouse (self, cursor):
        return (
            (cursor[0] >= self.pos[0] - self.dimensions[0]/2) &
            (cursor[0] <= self.pos[0] + self.dimensions[0]/2) &
            (cursor[1] >= self.pos[1] - self.dimensions[1]/2) &
            (cursor[1] <= self.pos[1] + self.dimensions[1]/2) 
        )

    def handle_mouse (self, cursor, clicked, pressed):
        if not pressed:
            self.image = self.image_unpressed
        if clicked & self.under_mouse(cursor):
            self.image = self.image_pressed
            self.click_action
    
    def click_action (self):
        print("pressed")

    def get_frame_image(self):
        return self.image

    def draw (self, display):
        image = self.get_frame_image()
        box = image.get_rect()
        display.blit(image,
            (
                self.pos[0] - box[2]/2,
                self.pos[1] - box[3]/2
            )
        );

class Cookie (Button):
    def __init__ (self, image, image_pressed, pos, pressed_size, id):
        super().__init__(image, image_pressed, pos, pressed_size)
        self.id = id

        self.rot = 0
        self.rot_vel = 0

    def click_action (self):
        print("button pressed")
        self.rot_vel += 10

    def physics_ig (self):
        self.rot_vel *= 0.93
        self.rot += self.rot_vel

    def get_frame_image(self):
        return pygame.transform.rotate(self.image, self.rot)

class Cookies:
    def __init__ (self, amount, radius, image_clicked_scale = (0, 0), pos = (0, 0) ):
        self.pos = pos

        self.image = pygame.image.load('cookie.png')
        image_dimensions = (
            self.image.get_rect()[2],
            self.image.get_rect()[3]
        )
        self.image_clicked = pygame.image.load('cookie_clicked.png')

        self.amount = amount
        if amount == 1:
            radius = 0
        self.cookies = []
        for i in range(self.amount):
            self.cookies.append( Cookie(
                image = self.image,
                image_pressed = self.image_clicked,
                pos = (
                    math.cos(((2*math.pi)/amount) * i) * radius + self.pos[0],
                    math.sin(((2*math.pi)/amount) * i) * radius + self.pos[1]
                ),
                pressed_size = 0.8,
                id = i
                ))

    def draw (self, display):
        for i in range(self.amount):
            self.cookies[i].draw(display)

    def handle_mouse (self, cursor, click, pressed):
        #print(f"click {click}, pressed {pressed}")
        for i in range(self.amount):
            self.cookies[i].handle_mouse(cursor, click, pressed)

    def do_stuff (self):
        for i in range(self.amount):
            self.cookies[i].physics_ig()


# --- functions ---

def draw ():
    screen.fill("#202020")
    cookies_arr.draw(screen)


# --- main ---

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((display_width, 600))
    pygame.display.set_caption("cookie clicker")
    clock = pygame.time.Clock()
    dt = 0
    main_count = 0

    cookies_arr = Cookies(
        amount = 1,
        radius = 100,
        image_clicked_scale = (120, 120),
        pos = (300, display_height / 2)
    )

    running = True
    while running:
        # check for events
        mouse = pygame.mouse.get_pos()
        mouse_click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_click = True
        cookies_arr.handle_mouse(mouse, mouse_click, pygame.mouse.get_pressed()[0])
        keys = pygame.key.get_pressed()
        if keys[pygame.K_q]:
            running = False
        # example: if keys[pygame.K_w]: print("w pressed")

        # game mechanics
        cookies_arr.do_stuff()

        # draw
        draw()


        # update display
        pygame.display.flip()

        # limits FPS to 60
        dt = clock.tick(FPS) / 1000

    pygame.quit()

