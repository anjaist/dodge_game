import pygame, sys, random, time
from pygame.locals import *

pygame.init()

#color variables defined
black = (0, 0, 0)
white = (255, 255, 255)
light_red = (255, 0, 0)
dark_red = (180, 0, 0)
light_green = (0, 255, 0)
dark_green = (0, 180, 0)
blue = (0, 0, 255)
intro_bgcolor = (215, 225, 242)
bgcolor = (242, 244, 249)
block_color = (79, 43, 9)
yellow = (255, 255, 0)

#display variables defined
display_w = 1024
display_h = 768
gameDisplay = pygame.display.set_mode((display_w, display_h))
pygame.display.set_caption("It's my work-in-progress, my progress is working!")
clock = pygame.time.Clock()
fps = 30

#car variables defined
cars = ["car_blue.png", "car_green.png", "car_yellow.png", "car_red.png", "car_grey.png", "car_police.png"]
carw = 59
carh = 111
random.shuffle(cars)
carImg = pygame.image.load(cars[0])
carImg = pygame.transform.scale(carImg, (carw, carh))

#sound items
pygame.mixer.music.load("music_bg.wav")
sound_crash = pygame.mixer.Sound("sound_crash.wav")

paused = False

def gamequit():
    pygame.quit()
    sys.exit()

def blocks(display,color,x,y,w,h):
    pygame.draw.rect(display,color,(x,y,w,h))

def car(x,y):
    gameDisplay.blit(carImg, (x, y))

def text_objects(text, font):
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()

def game_text(text, center_x, center_y, fontsize):
    gameText = pygame.font.Font("freesansbold.ttf", fontsize)
    textSurf, textRect = text_objects(text, gameText)
    textRect.center = (center_x, center_y)
    gameDisplay.blit(textSurf, textRect)

def crash():
    crashed = True
    pygame.mixer.Sound.play(sound_crash)
    pygame.mixer.music.stop()
    game_text("You crashed.", (display_w/2), (display_h/3.1), 62)
    game_text("Play again?", (display_w/2), (display_h/2.2), 32)
    while crashed:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                gamequit()

        button(display_w/2 - 150,display_h/1.7,65,65,dark_green,light_green,"Yes",game_loop)
        button(display_w/2 + 90,display_h/1.7,65,65,dark_red,light_red,"No",gamequit)

        pygame.display.update()
        clock.tick(fps)

def game_score(count):
    game_text(("Score: "+str(count)),display_w-50,10,15)

def button(x,y,h,w,dark_color,highlight_color,text,action):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    pygame.draw.rect(gameDisplay,dark_color,(x,y,h,w))

    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(gameDisplay,highlight_color,(x,y,h,w))
        if click[0] == True:
            action()
    else:
        pygame.draw.rect(gameDisplay,dark_color,(x,y,h,w))

    game_text(text,(x+(w/2)),(y+(h/2)),18)

def game_unpaused():
    global paused
    pygame.mixer.music.unpause()
    paused = False

def game_paused():
    pygame.mixer.music.pause()
    game_text("Ready to continue?", (display_w/2), (display_h/2.4), 62)
    while paused:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                gamequit()
            elif event.type == KEYDOWN and event.key == K_p:
                game_unpaused()

        button(display_w/2 - 150,display_h/1.7,65,65,dark_green,light_green,"Yes",game_unpaused)
        button(display_w/2 + 90,display_h/1.7,65,65,dark_red,light_red,"No",gamequit)

        pygame.display.update()
        clock.tick(fps)

def game_intro():
    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                gamequit()
        gameDisplay.fill(intro_bgcolor)
        game_text("Ready?", (display_w/2), (display_h/2.4), 62)

        button(display_w/2 - 150,display_h/1.7,65,65,dark_green,light_green,"Yes",game_loop)
        button(display_w/2 + 90,display_h/1.7,65,65,dark_red,light_red,"No",gamequit)

        pygame.display.update()
        clock.tick(fps)


def game_loop():
    global paused
    pygame.mixer.music.play(-1)

    #car variables
    carx = display_w/2 - carw/2
    cary = display_h - (carh+5)
    carx_change = 0
    cary_change = 0
    carspeed = 10

    #blocks variables
    blockh = 100
    blockw = 75
    blockx = random.randrange(0, (display_w-blockw))
    blocky = -50
    block_speed = 5
    count = 0

    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                gamequit()

            #car movements
            if event.type == KEYDOWN:
                if event.key == K_RIGHT:
                    carx_change += carspeed
                elif event.key == K_LEFT:
                    carx_change -= carspeed
                elif event.key == K_UP:
                    cary_change -= carspeed
                elif event.key == K_DOWN:
                    cary_change += carspeed
                elif event.key == K_p:
                    paused = True
                    game_paused()

            if event.type == KEYUP:
                if event.key == K_RIGHT or event.key == K_LEFT:
                    carx_change = 0
                elif event.key == K_UP or event.key == K_DOWN:
                    cary_change = 0

        cary += cary_change
        carx += carx_change

        #screen boundaries to car
        if carx < 0:
            carx = 0
        elif carx > display_w - carw:
            carx = display_w - carw
        if cary < 0:
            cary = 0
        elif cary > display_h - carh:
            cary = display_h - carh

        gameDisplay.fill(bgcolor)
        car(carx,cary)
        game_score(count)
        blocks(gameDisplay,block_color,blockx,blocky,blockw,blockh)
        blocky += block_speed

        #send another block when one is off screen
        if blocky > display_h:
            count += 1
            blocky = 0 - blockh
            blockx = random.randrange(0,(display_w - blockw))
            block_speed += 1
            if block_speed == 15:
                block_speed = 15

        #if car collides with block, crash
        if blocky + blockh > cary and cary + carh > blocky:
            if carx < blockx + blockw and carx > blockx or carx + carw > blockx and carx + carw < blockx + blockw:
                crash()

        pygame.display.update()
        clock.tick(fps)

game_intro()
game_loop()

