from tkinter import ROUND
import pygame
import button
from pygame import mixer
from fighter import Fighter

mixer.init()
pygame.init()

# creer une fenetre de jeu
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Fighter")

# variable du jeu
game_paused = False
menu_state = "main"

# definir la police
font = pygame.font.Font("image/turok.ttf", 30)

# définir le taux de rafraîchissement
clock = pygame.time.Clock()
FPS = 60

# definir couleur
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
TEXT_COL = (255, 255, 255)

# charger les images du menu
resume_img = pygame.image.load(
    "image/button/button_resume.png").convert_alpha()
options_img = pygame.image.load(
    "image/button/button_options.png").convert_alpha()
quit_img = pygame.image.load("image/button/button_quit.png").convert_alpha()
video_img = pygame.image.load("image/button/button_video.png").convert_alpha()
audio_img = pygame.image.load("image/button/button_audio.png").convert_alpha()
keys_img = pygame.image.load("image/button/button_keys.png").convert_alpha()
back_img = pygame.image.load("image/button/button_back.png").convert_alpha()

# creation du bouton
resume_button = button.Button(410, 125, resume_img, 1)
options_button = button.Button(402, 250, options_img, 1)
quit_button = button.Button(442, 375, quit_img, 1)
video_button = button.Button(330, 125, video_img, 1)
audio_button = button.Button(330, 225, audio_img, 1)
keys_button = button.Button(352, 325, keys_img, 1)
back_button = button.Button(438, 450, back_img, 1)

# definir variable jeu
intro_count = 3
last_count_update = pygame.time.get_ticks()
score = [0, 0]  # score du joueur [player 1, player 2]
round_over = False
ROUND_OVER_COOLDOWN = 2000

# definir variables combattant
'''WARRIOR_SIZE = 162
WARRIOR_SCALE = 4
WARRIOR_OFFSET = [72, 56]
WARRIOR_DATA = [WARRIOR_SIZE, WARRIOR_SCALE, WARRIOR_OFFSET]'''

WIZARD_SIZE = 250
WIZARD_SCALE = 3
WIZARD_OFFSET = [112, 107]
WIZARD_DATA = [WIZARD_SIZE, WIZARD_SCALE, WIZARD_OFFSET]

COCO_SIZE = 162
COCO_SCALE = 2
COCO_OFFSET = [72, 28]
COCO_DATA = [COCO_SIZE, COCO_SCALE, COCO_OFFSET]

# charger la musique et les effets sonores
pygame.mixer.music.load("audio/smash.mp3")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1, 0.0, 5000)
sword_fx = pygame.mixer.Sound("audio/epee.wav")
sword_fx.set_volume(0.2)
ricard_fx = pygame.mixer.Sound("audio/bonk.mp3")
ricard_fx.set_volume(0.3)
magic_fx = pygame.mixer.Sound("audio/bonk.mp3")
magic_fx.set_volume(0.3)
#victory_fx = pygame.mixer.Sound("audio/siuu.mp3")
# victory_fx.set_volume(0.3)


# charger image en arriere plan
background_image = pygame.image.load(
    "image/background/back.jpg").convert_alpha()

# charger animation
warrior_sheet = pygame.image.load("image/Fighter/warrior.png").convert_alpha()
wizard_sheet = pygame.image.load("image/Fighter2/wizard.png").convert_alpha()
coco_sheet = pygame.image.load("image/Coco/Coco1.png")

# charger image
victory_img = pygame.image.load(
    "image/background/victory royale.png").convert_alpha()

# définition du nombre d'étapes pour chaque animation
WARRIOR_ANIMATION_STEPS = [10, 8, 3, 7, 7, 3, 7]
WIZARD_ANIMATION_STEPS = [8, 8, 2, 8, 8, 3, 7]
COCO_ANIMATION_STEPS = [9, 5, 2, 8, 10, 2, 7]

# definir police
count_font = pygame.font.Font("image/turok.ttf", 80)
score_font = pygame.font.Font("image/turok.ttf", 30)

# fonction pour dessiner du texte


def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

# fonction pour dessiner arriere plan


def draw_bg():
    scaled_background = pygame.transform.scale(
        background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
    screen.blit(scaled_background, (0, 0))

# fontion pour dessiner barre de vie


def draw_health_bar(health, x, y):
    ratio = health / 100
    pygame.draw.rect(screen, WHITE, (x - 2, y - 2, 404, 34))
    pygame.draw.rect(screen, RED, (x, y, 400, 30))
    pygame.draw.rect(screen, YELLOW, (x, y, 400 * ratio, 30))


# creation de deux instance de combattants
coco = Fighter(1, 200, 310, False, COCO_DATA, coco_sheet,
               COCO_ANIMATION_STEPS, ricard_fx)
'fighter_1 = Fighter(1, 200, 310, False, WARRIOR_DATA, warrior_sheet, WARRIOR_ANIMATION_STEPS, sword_fx)'
fighter_2 = Fighter(2, 700, 310, True, WIZARD_DATA,
                    wizard_sheet, WIZARD_ANIMATION_STEPS, magic_fx)


# boucle de jeu
run = True
while run:

    clock.tick(FPS)

    # dessiner arriere plan
    draw_bg()

    # verifie si le jeu est en pause
    if game_paused == True:
        # Empeche les joueurs de jouer
        # test
        # verifie letat du menu
        if menu_state == "main":
            # boutons de pause
            if resume_button.draw(screen):
                game_paused = False
            if options_button.draw(screen):
                menu_state = "options"
            if quit_button.draw(screen):
                run = False
        # verifie si le menu option est ouvert
        if menu_state == "options":
            # options du menu options
            if video_button.draw(screen):
                print("video")
            if audio_button.draw(screen):
                print("audio")
            if keys_button.draw(screen):
                print("keys")
            if back_button.draw(screen):
                menu_state = "main"
    else:
        draw_text("Press ECHAP to pause", font, TEXT_COL, 15, 560)

    # afficher stats des joueurs
    draw_health_bar(coco.health, 20, 30)
    'draw_health_bar(fighter_1.health,20,30)'
    draw_health_bar(fighter_2.health, 580, 30)
    draw_text("P1: " + str(score[0]), score_font, RED, 20, 60)
    draw_text("P2: " + str(score[1]), score_font, RED, 580, 60)
    # changer le compte a rebours
    if intro_count <= 0:
        # Deplacement joueurs
        coco.move(SCREEN_WIDTH, SCREEN_HEIGHT,
                  screen, fighter_2, round_over, True)
        'fighter_1.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, fighter_2, round_over)'
        fighter_2.move(SCREEN_WIDTH, SCREEN_HEIGHT,
                       screen, coco, round_over, True)
    else:
        # affichage du compte a rebours
        draw_text(str(intro_count), count_font, RED,
                  SCREEN_WIDTH / 2, SCREEN_HEIGHT / 3)
        # evolution du temps
        if (pygame.time.get_ticks() - last_count_update) >= 1000:
            intro_count -= 1
            last_count_update = pygame.time.get_ticks()

    # evoluer combattants
    coco.update()
    'fighter_1.update()'
    fighter_2.update()

    # dessiner fighter
    coco.draw(screen)
    'fighter_1.draw(screen)'
    fighter_2.draw(screen)

    # verifie si le joueur a perdu
    if round_over == False:
        if coco.alive == False:
            score[1] += 1
            round_over = True
            round_over_time = pygame.time.get_ticks()
        elif fighter_2.alive == False:
            score[0] += 1
            round_over = True
            round_over_time = pygame.time.get_ticks()
    else:
        # affiche l'image de victoire
        screen.blit(victory_img, (300, 90))
        # victory_fx.play()
        if pygame.time.get_ticks() - round_over_time > ROUND_OVER_COOLDOWN:
            round_over = False
            intro_count = 3
            coco = Fighter(1, 200, 310, False, COCO_DATA,
                           coco_sheet, COCO_ANIMATION_STEPS, sword_fx)
            'fighter_1 = Fighter(1, 200, 310, False, WARRIOR_DATA, warrior_sheet, WARRIOR_ANIMATION_STEPS, sword_fx)'
            fighter_2 = Fighter(2, 700, 310, True, WIZARD_DATA,
                                wizard_sheet, WIZARD_ANIMATION_STEPS, magic_fx)

    # gestionnaire d'événement
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                game_paused = True
        if event.type == pygame.QUIT:
            run = False

    # maj ecran
    pygame.display.update()

# quitter jeu
pygame.quit()
