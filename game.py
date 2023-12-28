import pygame
import random
import math
import sys
import os

pygame.init()
screen_witdh = 800
screen_height = 600
screen = pygame.display.set_mode((screen_witdh, screen_height))


def resource_path(relative_patn):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
        return os.path.join(base_path, relative_patn)


asset_background = resource_path("assets//images//background.png")
background = pygame.image.load(asset_background)

asset_icon = resource_path("assets//images//ufo.png")
icon = pygame.image.load(asset_icon)

asset_sound = resource_path("assets//audios//background_music.mp3")
background_sound = pygame.mixer.music.load(asset_sound)

asset_playerimg = resource_path("assets//images//space-invaders.png")
playerimg = pygame.image.load(asset_playerimg)

asset_bulletimg = resource_path("assets//images//bullet.png")
bulletimg = pygame.image.load(asset_bulletimg)

asset_over_font = resource_path("assets//fonts//RAVIE.TTF")
over_font = pygame.font.Font(asset_over_font, 60)

asset_font = resource_path("assets//fonts//comicbd.ttf")
font = pygame.font.Font(asset_font, 32)

pygame.display.set_caption("jugito de naves")

pygame.display.set_icon(icon)

pygame.mixer.music.play(-1)

clock = pygame.time.Clock()

playerX = 370
playerY = 470
playerx_change = 0
playery_change = 0

enemyimg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
no_of_enemies = 10

for i in range(no_of_enemies):
    enemy1 = resource_path("assets//images//enemy1.png")
    enemyimg.append(pygame.image.load(enemy1))

    enemy2 = resource_path("assets//images//enemy2.png")
    enemyimg.append(pygame.image.load(enemy2))

    enemyX.append(random.randint(0, 736))
    enemyY.append(random.randint(0, 150))

    enemyX_change.append(5)
    enemyY_change.append(20)

    bulletX = 0
    bulletY = 480
    bulletX_change = 0
    bulletY_change = 10
    bullet_state = "ready"

    score = 0

    def show_score():
        score_value = font.render("SCORE " + str(score), True, (255, 255, 255))
        screen.blit(score_value, (10, 10))

    def player(x, y):
        screen.blit(playerimg, (x, y))

    def enemy(x, y, i):
        screen.blit(enemyimg[i], (x, y))

    def fire_bullet(x, y):
        global bullet_state

        bullet_state = "fire"
        screen.blit(bulletimg, (x + 16, y + 10))

    def isCollision(enemyX, enemyY, bulletX, bulletY):
        distance = math.sqrt((math.pow(enemyX-bulletX, 2)) +
                             (math.pow(enemyY-bulletY, 2)))
        if distance < 27:
            return True
        else:
            return False

    def game_over_text():
        over_text = over_font.render("JUEGO TERMINADO", True, (255, 255, 255))
        text_rect = over_text.get_rect(
            center=(int(screen_witdh/2), int(screen_height/2)))
        screen.blit(over_text, text_rect)
        clock.tick(120)
        pygame.quit()
        sys.exit()

    def gameloop():
        global score
        global playerX
        global playerx_change
        global bulletX
        global bulletY
        global Collision
        global bullet_state

        in_game = True
        while in_game:
            screen.fill((0, 0, 0))
            screen.blit(background, (0, 0))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    in_game = False
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        playerx_change = -5

                    if event.key == pygame.K_RIGHT:
                        playerx_change = 5

                    if event.key == pygame.K_SPACE:
                        if bullet_state == "ready":
                            bulletX = playerX
                            fire_bullet(bulletX, bulletY)

                    if event.type == pygame.KEYUP:
                        playerx_change = 0

            playerX += playerx_change

            if playerX <= 0:
                playerX = 0
            elif playerX >= 736:
                playerX = 736

            for i in range(no_of_enemies):
                if enemyY[i] > 440:
                    for j in range(no_of_enemies):
                        enemyY[j] = 2000
                    game_over_text()
                enemyX[i] += enemyX_change[i]
                if enemyX[i] <= 0:
                    enemyX_change[i] = 5
                    enemyY[i] += enemyY_change[i]
                elif enemyX[i] >= 736:
                    enemyX_change[i] = -5
                    enemyY[i] += enemyY_change[i]
                collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
                if collision:
                    bulletY = 454
                    bullet_state = "ready"
                    score += 1
                    enemyX[i] = random.randint(0, 736)
                    enemyY[i] = random.randint(0, 150)
                enemy(enemyX[i], enemyY[i], i)

            if bulletY < 0:
                bulletY = 454
                bullet_state = "ready"
            if bullet_state == "fire":
                fire_bullet(bulletX, y=bulletY)
                bulletY -= bulletY_change

            player(playerX, playerY)
            show_score()

            pygame.display.update()

            clock.tick(120)

gameloop()
