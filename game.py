toggle=1
soundV=0

import pygame

pygame.init()
screen = pygame.display.set_mode((1000, 600))
pygame.display.set_caption("Simple Game Loop")
clock = pygame.time.Clock()
running = True
sound=pygame.mixer.Sound("background music.mp3")
while running:
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos=event.pos #Mausposition abfragen
            if rect.collidepoint(mouse_pos):
                print("Bild angeklickt!")
                toggle=toggle*-1
        if event.type == pygame.QUIT:
            running = False
        
    if toggle==1 and not soundV==1:
        sound.play()
        soundV=1
    if toggle==-1: 
        sound.stop()
        soundV=0
        
    screen.fill((255, 255, 255))
    # Grenzposition
    boundary_x = 600

    #Objekte zeichnen
    #BLUE=(50,120,255)
    #rect=pygame.Rect(100,150,80,80)
    #pygame.draw.rect(screen, BLUE, rect)

    #Bild einfügen
    if toggle==-1:
        image=pygame.image.load("SpeakerWithX.png")
    else: image=pygame.image.load("Speaker.png")
    x=50
    y=50
    image=pygame.transform.scale(image,(40,40))
    rect=image.get_rect()
    rect.topleft=(x,y)
    screen.blit(image,(x,y))


    # Vertikale Linie zeichnen
    pygame.draw.line(screen, (255, 255, 255), (boundary_x, 0), (boundary_x, 600), 2)
    pygame.display.flip()
    clock.tick(60)



    

pygame.quit()