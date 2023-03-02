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
game_started = False
# definir la police
font = pygame.font.Font("image/Turok.ttf", 30)

# définir le taux de rafraîchissement
clock = pygame.time.Clock()
FPS = 60

# definir couleur
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
TEXT_COL = (255, 255, 255)

# charger les images du menu
solo_img = pygame.image.load("image/button/button_solo.png").convert_alpha()
resume_img = pygame.image.load(
    "image/button/button_resume.png").convert_alpha()
options_img = pygame.image.load(
    "image/button/button_options.png").convert_alpha()
quit_img = pygame.image.load("image/button/button_quit.png").convert_alpha()
video_img = pygame.image.load("image/button/button_video.png").convert_alpha()
audio_img = pygame.image.load("image/button/button_audio.png").convert_alpha()
keys_img = pygame.image.load("image/button/button_keys.png").convert_alpha()
back_img = pygame.image.load("image/button/button_back.png").convert_alpha()

#charger images pour le choix des personnages
playerCoco_img = pygame.image.load("image/Coco/Coco.png")
playerWizard_img = pygame.image.load("image/Fighter2/wizardChoose.png")

# creation du bouto
# Main menu
solo_button = button.Button(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4, solo_img, 1,
                            (SCREEN_WIDTH, SCREEN_HEIGHT))
options_button = button.Button(SCREEN_WIDTH // 2,
                               solo_button.y + solo_button.y, options_img, 1,
                               (SCREEN_WIDTH, SCREEN_HEIGHT))
quit_button = button.Button(SCREEN_WIDTH // 2,
                            options_button.y + options_button.y / 2, quit_img,
                            1, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Option Menu
video_button = button.Button(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 5, video_img,
                             1, (SCREEN_WIDTH, SCREEN_HEIGHT))

audio_button = button.Button(SCREEN_WIDTH // 2,
                             video_button.y + video_button.y, audio_img, 1,
                             (SCREEN_WIDTH, SCREEN_HEIGHT))

keys_button = button.Button(SCREEN_WIDTH // 2,
                            audio_button.y + audio_button.y / 2, keys_img, 1,
                            (SCREEN_WIDTH, SCREEN_HEIGHT))

back_button = button.Button(SCREEN_WIDTH // 2,
                            keys_button.y + keys_button.y / 3, back_img, 1,
                            (SCREEN_WIDTH, SCREEN_HEIGHT))

# Pause Menu
resume_button = button.Button(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4,
                              resume_img, 1, (SCREEN_WIDTH, SCREEN_HEIGHT))

coco_button = button.Button(100, 100, playerCoco_img, 1,
                            (SCREEN_WIDTH, SCREEN_HEIGHT))
wizard_button = button.Button(coco_button.width + coco_button.width / 2, 100,
                              playerWizard_img, 1,
                              (SCREEN_WIDTH, SCREEN_HEIGHT))

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
ricard_fx = pygame.mixer.Sound("audio/bonk.wav")
ricard_fx.set_volume(0.3)
magic_fx = pygame.mixer.Sound("audio/bonk.wav")
magic_fx.set_volume(0.3)
# victory_fx = pygame.mixer.Sound("audio/siuu.mp3")
# victory_fx.set_volume(0.3)

#charger image du main menu
main_image = pygame.image.load("image/background/main.gif").convert_alpha()

#charger image du choix perso
bg_choixPerso = pygame.image.load("image/background/choix_perso.gif")

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
def draw_bg(img):
    scaled_background = pygame.transform.scale(img,
                                               (SCREEN_WIDTH, SCREEN_HEIGHT))
    screen.blit(scaled_background, (0, 0))


# fontion pour dessiner barre de vie
def draw_health_bar(health, x, y):
    ratio = health / 100
    pygame.draw.rect(screen, WHITE, (x - 2, y - 2, 404, 34))
    pygame.draw.rect(screen, RED, (x, y, 400, 30))
    pygame.draw.rect(screen, YELLOW, (x, y, 400 * ratio, 30))


# creation de deux instance de combattants
fighter_choose = dict()
fighter_choose["coco"] = (COCO_DATA, coco_sheet, COCO_ANIMATION_STEPS,
                          ricard_fx, 20)
fighter_choose["wizard"] = (WIZARD_DATA, wizard_sheet, WIZARD_ANIMATION_STEPS,
                            magic_fx, 10)

choix = []

create_Fighters = True
# boucle de jeu
run = True
while run:

    clock.tick(FPS)
    if menu_state == "main":
        # dessiner arriere plan
        draw_bg(main_image)
        if solo_button.draw(screen):
            # enlever le menu pour lancer le jeu
            menu_state = "choix_perso"
        if options_button.draw(screen):
            menu_state = "options"
        if quit_button.draw(screen):
            print("quitting")
            run = False
    elif menu_state == "choix_perso":
        draw_bg(bg_choixPerso)
        playerToChoose = 0
        if coco_button.draw(screen):
            choix.append("coco")
        if wizard_button.draw(screen):
            choix.append("wizard")
        if len(choix) == 2:
            menu_state = "in_game"

    elif menu_state == "in_game":
        if (create_Fighters == True):
            fighter_1 = Fighter(1, 200, 310, False, *fighter_choose[choix[0]])
            fighter_2 = Fighter(2, 700, 310, True, *fighter_choose[choix[1]])
            create_Fighters = False

        draw_bg(background_image)
        game_started = True

        # afficher stats des joueurs
        draw_health_bar(fighter_1.health, 20, 30)
        draw_health_bar(fighter_2.health, 580, 30)
        draw_text("P1: " + str(score[0]), score_font, RED, 20, 60)
        draw_text("P2: " + str(score[1]), score_font, RED, 580, 60)

        # changer le compte a rebours
        if intro_count == 0:
            # Deplacement joueurs
            fighter_1.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, fighter_2,
                           round_over)
            fighter_2.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, fighter_1,
                           round_over)
        else:

            # affichage du compte a rebours
            draw_text(str(intro_count), count_font, RED, SCREEN_WIDTH / 2,
                      SCREEN_HEIGHT / 3)

            # evolution du temps
            if (pygame.time.get_ticks() -
                    last_count_update) >= 1000 and intro_count > 0:
                intro_count -= 1
                last_count_update = pygame.time.get_ticks()

        # dessiner fighter
        fighter_1.draw(screen)
        fighter_2.draw(screen)

        # evoluer combattants
        fighter_1.update()
        fighter_2.update()

        # verifie si le joueur a perdu
        if round_over == False:
            if fighter_1.alive == False:
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
                create_Fighters = True
        draw_text("Press ECHAP to pause", font, TEXT_COL, 15, 560)

    elif menu_state == "pause":
        if resume_button.draw(screen):
            game_paused = False
            menu_state = "in_game"
        if options_button.draw(screen):
            menu_state = "options"
        if back_button.draw(screen):
            menu_state = "main"

    # verifie si le jeu est en pause
    elif menu_state == "options":
        # options du menu options
        if video_button.draw(screen):
            print("video")
        if audio_button.draw(screen):
            print("audio")
        if keys_button.draw(screen):
            menu_state == "key_binding"
        if menu_state == "key_binding":
            print("key_binding")
        if back_button.draw(screen):
            if game_started == True:
                menu_state = "pause"
            else:
                game_start = False
                menu_state = "main"

    # gestionnaire d'événement
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if (event.key == pygame.K_ESCAPE and menu_state == "in_game"):
                game_paused = True
                menu_state = "pause"
        if event.type == pygame.QUIT:
            run = False

    # maj ecran
    pygame.display.update()

# quitter jeu
pygame.quit()
