import pygame
import random

pygame.init()

# making window
screen_width = 600
screen_height = 590
screen = pygame.display.set_mode((screen_width, screen_height))

# changing title
pygame.display.set_caption("Space Invaders")

# changing icon
icon = pygame.image.load("spaceship.png")
pygame.display.set_icon(icon)

# game variable
velocity = 0.5
spaceshipx = ((screen_width // 2) - 32)
spaceshipy = (screen_height * 0.8)
playerimg = pygame.image.load("spaceshipch.png")
backgroundimg = pygame.image.load("bacground1.jpg")
enemy1 = pygame.image.load("enemy.png")
enemy2 = pygame.image.load("enemy2.png")
enemy3 = pygame.image.load("enemy3.png")
enemy4 = pygame.image.load("enemy4.png")
enemy5 = pygame.image.load("enemy5.png")
enemys = [enemy1, enemy2, enemy3, enemy4, enemy5]

enemyVelocity = 0.5
enemyx = (random.randint(5, screen_width - 69))
enemyy = 5
enemyappear = True
playerappear = True
moveright = True
moverLeft = False
bullety = 0
bulletx = 0
score = 0
draw = False
hit_sound = pygame.mixer.Sound('hit.wav')
die_sound = pygame.mixer.Sound('die.wav')
music = pygame.mixer.music.load('music.mp3')
#music = pygame.mixer.music.load('song.mp3')
bullets = []
enemy = random.choice(enemys)
powerups=3
mus=False


def player(x, y):
    if playerappear:
        screen.blit(playerimg, (x, y))


hits = 0
font = pygame.font.SysFont("comicsans", 27)
cscore=0

def showText(text, color, x, y):
    screen_text = font.render(text, True, color)
    screen.blit(screen_text, [x, y])


def makeenemy():
    global enemyappear, playerappear, enemyy, enemyx, enemy, moverLeft, moveright, enemyVelocity, hits, draw, bullety, score

    # if enemyy>=100:
    #     enemyappear=False
    #     enemyy=-1

    if enemyy + 64 >= spaceshipy:
        hits = 0
        score -= 10
        enemyappear = False
        showText("-10", (0, 0, 0), 2, 2)

    for bullet in bullets:
        if abs(bullet[0] - enemyx) < 33 and abs(bullet[1] - enemyy) < 33:
            hit_sound.play()

            die_sound.play()
            hits += 1
            bullets.pop(bullets.index(bullet))
        if hits >= 10:
            score += 1
            draw = False
            enemy = random.choice(enemys)
            enemyappear = False
            hits = 0

    if enemyappear:
        enemyVelocity += 0.0009
        screen.blit(enemy, (enemyx, enemyy))
        if enemyx <= 5:
            enemyy += 120
            moveright = True
            moverLeft = False
        elif enemyx >= screen_width - 69:
            enemyy += 120
            moveright = False
            moverLeft = True
        if moveright:
            enemyx += enemyVelocity
        elif moverLeft:
            enemyx -= enemyVelocity
    if enemyappear == False:
        enemyVelocity = 0.5
        enemyx = (random.randint(5, screen_width - 69))
        enemyy = 5
        enemyappear = True
        hits = 0
        playerappear = True
        moveright = True
        moverLeft = False
        enemy = random.choice(enemys)
    showText(f"Hits required={10-hits}",(255,0,0),screen_width-150,0)

    pygame.display.update()


with open("alhigh.txt", "r") as hi:
    hscore = (hi.read())

# mainloop
flag = "green"
while flag == "green":

    if pygame.event.get(pygame.QUIT):
        flag = "red"
        pygame.quit()

    # making a keys list
    keys = pygame.key.get_pressed()

    if keys[pygame.K_ESCAPE]:
        flag = "red"

    if keys[pygame.K_LEFT]:
        if not spaceshipx <= 5:
            spaceshipx -= velocity
    if keys[pygame.K_RIGHT]:
        if not spaceshipx + 69 >= screen_width:
            spaceshipx += velocity
    if keys[pygame.K_RALT]:
        spaceshipx = screen_width - 69
    if keys[pygame.K_LALT]:
        spaceshipx = 0
    if keys[pygame.K_UP]:
        if not velocity >= 3:
            velocity += 0.1
    if keys[pygame.K_DOWN]:
        draw = True
        if not velocity <= 1:
            velocity -= 0.1
    if keys[pygame.K_RSHIFT]:
        if powerups>0:
            pygame.time.delay(300)
            enemyappear=False
            powerups-=1

    screen.blit(backgroundimg, (0, 0))
    showText(f"Score: {score}", (255, 0, 0), 2, 2)
    showText(f"High Score: {hscore}", (255, 0, 0), 2, 18)
    showText(f"Powerups: {powerups}", (255, 0, 0), 2, 34)
    if keys[pygame.K_DELETE]:
        for bullet in bullets:
            bullets.pop(bullets.index(bullet))
    if keys[pygame.K_m]:
            pygame.mixer.music.play(-1)
    if keys[pygame.K_n]:
        pygame.mixer.music.pause()

    if keys[pygame.K_SPACE]:
        bulletx = spaceshipx // 1
        bullety = spaceshipy // 1
        if len(bullets) < 1:
            bullets.append([bulletx, bullety])
        draw = True
    if draw:
        for bullet in bullets:
            pygame.draw.circle(screen, (255, 0, 0), (int(bullet[0]) + 32, int(bullet[1])), 6)
    for bullet in bullets:

        if bullet[1] < screen_width and bullet[1] > 0:
            bullet[1] -= 4
        else:
            bullets.pop(bullets.index(bullet))

    player(spaceshipx, spaceshipy)

    makeenemy()
    pygame.display.update()

with open("alhigh.txt", "w") as high:
    if int(hscore) < score:
        high.write(str(score))
    else:

        high.write(hscore)

pygame.quit()
