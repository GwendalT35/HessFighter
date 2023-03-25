import pygame
import button
import re
import json
import serveur
from pygame import mixer
from fighter import Fighter

mixer.init()
pygame.init()

# Recuperation des options
with open("options.json", 'r') as fileOptions:
    option = json.load(fileOptions)

# creer une fenetre de jeu
SCREEN_WIDTH = option["video_settings"]["width"]
SCREEN_HEIGHT = option["video_settings"]["height"]

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Fighter")

# variable du jeu
game_paused = False
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
BLACK = (0, 0, 0)
TEXT_COL = (255, 255, 255)

# charger les images du menu
solo_img = pygame.image.load("image/button/button_solo.png").convert_alpha()
multi_img = pygame.image.load("image/button/button_multi.png").convert_alpha()
play_img = pygame.image.load("image/button/button_play.png").convert_alpha()
resume_img = pygame.image.load(
    "image/button/button_resume.png").convert_alpha()
options_img = pygame.image.load(
    "image/button/button_options.png").convert_alpha()
quit_img = pygame.image.load("image/button/button_quit.png").convert_alpha()
video_img = pygame.image.load("image/button/button_video.png").convert_alpha()
apply_img = pygame.image.load("image/button/button_apply.png").convert_alpha()
audio_img = pygame.image.load("image/button/button_audio.png").convert_alpha()
keys_img = pygame.image.load("image/button/button_keys.png").convert_alpha()
back_img = pygame.image.load("image/button/button_back.png").convert_alpha()

# charger images pour le choix des personnages
playerCoco_img = pygame.image.load("image/Coco/Coco.png")
playerWizard_img = pygame.image.load("image/Fighter2/wizardChoose.png")
playerWar_img = pygame.image.load("image/Fighter/warChoose.png")

# creation des menus

# Main menu
main_button = [
    button.Button(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 5, solo_img, 1,
                  (SCREEN_WIDTH, SCREEN_HEIGHT)),
    button.Button(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 5 * 2, multi_img, 1,
                  (SCREEN_WIDTH, SCREEN_HEIGHT)),
    button.Button(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 5 * 3, options_img, 1,
                  (SCREEN_WIDTH, SCREEN_HEIGHT)),
    button.Button(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 5 * 4, quit_img, 1,
                  (SCREEN_WIDTH, SCREEN_HEIGHT))
]
#Multijoueur menu
multi_button = [
    button.Button(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 5 * 4, play_img, 1,
                  (SCREEN_WIDTH, SCREEN_HEIGHT))
]
# Option Menu
option_button = [
    button.Button(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 5, video_img, 1,
                  (SCREEN_WIDTH, SCREEN_HEIGHT)),
    button.Button(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 5 * 2, audio_img, 1,
                  (SCREEN_WIDTH, SCREEN_HEIGHT)),
    button.Button(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 5 * 3, keys_img, 1,
                  (SCREEN_WIDTH, SCREEN_HEIGHT)),
    button.Button(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 5 * 4, back_img, 1,
                  (SCREEN_WIDTH, SCREEN_HEIGHT))
]

# video settings menu
video_button = [
    button.Button(SCREEN_WIDTH // 2 - apply_img.get_width(),
                  SCREEN_HEIGHT - 100, apply_img, 1,
                  (SCREEN_WIDTH, SCREEN_HEIGHT)),
    button.Button(SCREEN_WIDTH // 2 + back_img.get_width(),
                  SCREEN_HEIGHT - 100, back_img, 1,
                  (SCREEN_WIDTH, SCREEN_HEIGHT))
]

# Pause Menu
pause_button = [
    button.Button(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4, resume_img, 1,
                  (SCREEN_WIDTH, SCREEN_HEIGHT)),
    button.Button(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4 * 2, options_img, 1,
                  (SCREEN_WIDTH, SCREEN_HEIGHT)),
    button.Button(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4 * 3, quit_img, 1,
                  (SCREEN_WIDTH, SCREEN_HEIGHT))
]

#données perso pour crées les bouttons
#( image, scale, (screen width, screen height), name)
persoData = [
    (playerCoco_img, 1, (SCREEN_WIDTH, SCREEN_HEIGHT), "coco"),
    (playerWizard_img, 1, (SCREEN_WIDTH, SCREEN_HEIGHT), "wizard"),
    (playerWar_img, 1, (SCREEN_WIDTH, SCREEN_HEIGHT), "war"),
    (playerCoco_img, 1, (SCREEN_WIDTH, SCREEN_HEIGHT), "coco"),
    (playerWizard_img, 1, (SCREEN_WIDTH, SCREEN_HEIGHT), "wizard"),
    (playerWar_img, 1, (SCREEN_WIDTH, SCREEN_HEIGHT), "war"),
    (playerCoco_img, 1, (SCREEN_WIDTH, SCREEN_HEIGHT), "coco"),
    (playerWizard_img, 1, (SCREEN_WIDTH, SCREEN_HEIGHT), "wizard"),
    (playerWar_img, 1, (SCREEN_WIDTH, SCREEN_HEIGHT), "war"),
]

button_Choix_Perso = []
xMultiplier = 0
yMultiplier = 0
#Création des bouttons pour le choix des personnages
#en fonction de persoData
for data in persoData:
    if (100 + (150 * xMultiplier)) >= SCREEN_WIDTH - 100:
        xMultiplier = 0
        yMultiplier += 1
    button_Choix_Perso.append(
        button.Button(100 + (150 * xMultiplier), 100 + (150 * yMultiplier),
                      *data))
    xMultiplier += 1

#Dictionnaire des 'menu_state'
menu = {
    "main": main_button,
    "multi": multi_button,
    "choix_perso": button_Choix_Perso,
    "options": option_button,
    "video_settings": video_button,
    "audio_settings": video_button,
    "key_binding": video_button,
    "pause": pause_button,
    "in_game": [],
    "empty": []
}

# definir variable jeu
menu_state = "main"
previous_state = ""
button_clicked = False
intro_count = 3
last_count_update = pygame.time.get_ticks()
score = [0, 0]  # score du joueur [player 1, player 2]
round_over = False
ROUND_OVER_COOLDOWN = 2000

# definir variables combattant
WARRIOR_SIZE = 162
WARRIOR_SCALE = 4
WARRIOR_OFFSET = [72, 56]
WARRIOR_DATA = [WARRIOR_SIZE, WARRIOR_SCALE, WARRIOR_OFFSET]

WIZARD_SIZE = 250
WIZARD_SCALE = 3
WIZARD_OFFSET = [112, 107]
WIZARD_DATA = [WIZARD_SIZE, WIZARD_SCALE, WIZARD_OFFSET]

COCO_SIZE = 162
COCO_SCALE = 2
COCO_OFFSET = [72, 28]
COCO_DATA = [COCO_SIZE, COCO_SCALE, COCO_OFFSET]

# charger la musique et les effets sonores
volume = option["audio_settings"]
pygame.mixer.music.load("audio/smash.mp3")
pygame.mixer.music.set_volume(volume["music_volume"] / 100)
pygame.mixer.music.play(-1, 0.0, 5000)
sword_fx = pygame.mixer.Sound("audio/epee.wav")
sword_fx.set_volume(volume["fx_volume"] / 100)
ricard_fx = pygame.mixer.Sound("audio/bonk.wav")
ricard_fx.set_volume(volume["fx_volume"] / 100)
magic_fx = pygame.mixer.Sound("audio/bonk.wav")
magic_fx.set_volume(volume["fx_volume"] / 100)
# victory_fx = pygame.mixer.Sound("audio/siuu.mp3")
# victory_fx.set_volume(0.3)

#chargement des images
main_image = pygame.image.load("image/background/main.gif").convert_alpha()
bg_choixPerso = pygame.image.load("image/background/choix_perso.gif")
background_image = pygame.image.load(
    "image/background/back.jpg").convert_alpha()
victory_img = pygame.image.load(
    "image/background/victory royale.png").convert_alpha()

# charger animation
warrior_sheet = pygame.image.load("image/Fighter/warrior.png").convert_alpha()
wizard_sheet = pygame.image.load("image/Fighter2/wizard.png").convert_alpha()
coco_sheet = pygame.image.load("image/Coco/Coco1.png")

# définition du nombre d'étapes pour chaque animation
WARRIOR_ANIMATION_STEPS = [10, 8, 3, 7, 7, 3, 7]
WIZARD_ANIMATION_STEPS = [8, 8, 2, 8, 8, 3, 7]
COCO_ANIMATION_STEPS = [9, 5, 2, 8, 10, 2, 7]

# création des choix de combattants
fighter_choose = dict()
fighter_choose["coco"] = (COCO_DATA, coco_sheet, COCO_ANIMATION_STEPS,
                          ricard_fx, 15)
fighter_choose["wizard"] = (WIZARD_DATA, wizard_sheet, WIZARD_ANIMATION_STEPS,
                            magic_fx, 10)
fighter_choose["war"] = (WARRIOR_DATA, warrior_sheet, WARRIOR_ANIMATION_STEPS,
                         sword_fx, 20)
choix = []
create_Fighters = True
fighter_1 = None
fighter_2 = None
fighter_1_options = option["keyboard_settings"]["p1"]
fighter_2_options = option["keyboard_settings"]["p2"]

# definir police
count_font = pygame.font.Font("image/turok.ttf", 80)
score_font = pygame.font.Font("image/turok.ttf", 30)

#Dictionnaire des touches
toucheDict = dict({"K_a" : "A",
"K_b" : "B",
"K_c" : "C",
"K_d" : "D",
"K_e" : "E",
"K_f" : "F",
"K_g" : "G",
"K_h" : "H",
"K_i" : "I",
"K_j" : "J",
"K_k" : "K",
"K_l" : "L",
"K_m" : "M",
"K_n" : "N",
"K_o" : "O",
"K_p" : "P",
"K_q" : "Q",
"K_r" : "R",
"K_s" : "S",
"K_t" : "T",
"K_u" : "U",
"K_v" : "V",
"K_w" : "W",
"K_x" : "X",
"K_y" : "Y",
"K_z" : "Z",
"K_KP1" : "Clic gauche",
"K_KP2" : "Clic droit",
"K_UP" : "Fleche du haut",
"K_LEFT" : "Fleche de gauche",
"K_RIGHT" : "Fleche de droite",
"K_SPACE" : "Espace"
})

# Prompt ip server
ip_text = ""
ipMatch = re.compile(
    r"^((25[0-5]|(2[0-4]|1[0-9]|[1-9]|)[0-9])(\.(?!$)|$)){4}$")

# fonction pour dessiner du texte
def draw_text(text, font, text_col, x, y):
    text_render = font.render(text, True, text_col)
    screen.blit(text_render, (x, y))

# fonction pour dessiner l'arriere plan
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

# fonction pour dessiner les stats des personnages
def draw_stats(fighter1, fighter2):
    # afficher stats des joueurs
    draw_health_bar(fighter1.health, 20, 30)
    draw_health_bar(fighter2.health, 580, 30)
    draw_text("P1: " + str(score[0]), score_font, RED, 20, 60)
    draw_text("P2: " + str(score[1]), score_font, RED, 580, 60)
    # dessiner fighter
    fighter_1.draw(screen)
    fighter_2.draw(screen)

# fonction pour dessiner les bouttons des menus
def draw_button(buttonList):
    for button in menu[buttonList]:
        button.draw(screen)

# fonction pour sauvegarder les options
def save_options(options):
    with open("options.json", "w") as fileOptions:
        fileOptions.write(str(options).replace("'", "\""))


# boucle de jeu
run = True
while run:

    clock.tick(FPS)
    # Test des differents 'menu_state'
    if menu_state == "main":
        draw_bg(main_image)
        if previous_state != "":
            previous_state = ""
        # Test les bouttons pour savoir s'il son clique 
        if main_button[0].is_Clicked() and not button_clicked:
            button_clicked = True
            menu_state = "choix_perso"
            choix.clear()
        if main_button[1].is_Clicked() and not button_clicked:
            button_clicked = True
            menu_state = "multi"
        if main_button[2].is_Clicked() and not button_clicked:
            button_clicked = True
            menu_state = "options"
        if main_button[3].is_Clicked() and not button_clicked:
            button_clicked = True
            print("quitting")
            run = False
    elif menu_state == "multi":
        previous_state = "main"
        draw_bg(bg_choixPerso)
        draw_text(f"Entrez l'IP du serveur: {ip_text}", font, TEXT_COL, 15,
                  SCREEN_HEIGHT // 2)
        # Test si l'ip est bien de la forme 'XXX.XXX.XXX.XXX'
        if not bool(ipMatch.fullmatch(ip_text)):
            draw_text("Entrez une IP valide", font, RED, 15,
                      SCREEN_HEIGHT // 3 + SCREEN_HEIGHT // 4)
        if multi_button[0].is_Clicked() and not button_clicked:
            button_clicked = True
            
            print("Connexion au server...")
            menu_state = "choix_perso"
    elif menu_state == "choix_perso":
        previous_state = "main"
        draw_bg(bg_choixPerso)
        draw_text(f"Au joueur {len(choix) + 1} de choisir !", font, TEXT_COL,
                  SCREEN_WIDTH // 3, SCREEN_HEIGHT // 4 * 3)
        if button_Choix_Perso[0].is_Clicked() and not button_clicked:
            button_clicked = True
            choix.append(button_Choix_Perso[0].nom)
        elif button_Choix_Perso[1].is_Clicked() and not button_clicked:
            button_clicked = True
            choix.append(button_Choix_Perso[1].nom)
        elif button_Choix_Perso[2].is_Clicked() and not button_clicked:
            button_clicked = True
            choix.append(button_Choix_Perso[2].nom)
        elif button_Choix_Perso[3].is_Clicked() and not button_clicked:
            button_clicked = True
            choix.append(button_Choix_Perso[3].nom)
        elif button_Choix_Perso[4].is_Clicked() and not button_clicked:
            button_clicked = True
            choix.append(button_Choix_Perso[4].nom)
        elif button_Choix_Perso[5].is_Clicked() and not button_clicked:
            button_clicked = True
            choix.append(button_Choix_Perso[5].nom)
        elif button_Choix_Perso[6].is_Clicked() and not button_clicked:
            button_clicked = True
            choix.append(button_Choix_Perso[6].nom)
        elif button_Choix_Perso[7].is_Clicked() and not button_clicked:
            button_clicked = True
            choix.append(button_Choix_Perso[7].nom)
        elif button_Choix_Perso[8].is_Clicked() and not button_clicked:
            button_clicked = True
            choix.append(button_Choix_Perso[8].nom)
        if len(choix) == 2:
            menu_state = "in_game"
            print(choix)
    elif menu_state == "in_game":
        previous_state = "choix_perso"
        draw_bg(background_image)
        game_started = True
        # Cree les personnages
        if create_Fighters == True:
            fighter_1 = Fighter(1, 200, 310, False, *fighter_choose[choix[0]],
                                fighter_1_options)
            fighter_2 = Fighter(2, 700, 310, True, *fighter_choose[choix[1]],
                                fighter_2_options)
            create_Fighters = False
        # Dessine les stats (Vie + Score)
        draw_stats(fighter_1, fighter_2)
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
        if previous_state == "options":
            draw_bg(background_image)
            draw_stats(fighter_1, fighter_2)
        previous_state = "in_game"
        if pause_button[0].is_Clicked() and not button_clicked:
            button_clicked = True
            game_paused = False
            menu_state = "in_game"
        if pause_button[1].is_Clicked() and not button_clicked:
            button_clicked = True
            menu_state = "options"
            previous_state = "in_game"
        if pause_button[2].is_Clicked() and not button_clicked:
            choix.clear()
            create_Fighters = True
            intro_count = 3
            button_clicked = True
            game_started = False
            menu_state = "main"

    # verifie si le jeu est en pause
    elif menu_state == "options":
        if previous_state != "in_game":
            previous_state = "main"

        draw_bg(bg_choixPerso)
        # options du menu options
        if option_button[0].is_Clicked() and not button_clicked:
            button_clicked = True
            menu_state = "video_settings"
        if option_button[1].is_Clicked() and not button_clicked:
            button_clicked = True
            menu_state = "audio_settings"
        if option_button[2].is_Clicked() and not button_clicked:
            button_clicked = True
            menu_state = "key_binding"
        if option_button[3].is_Clicked() and not button_clicked:
            button_clicked = True
            if game_started == True:
                menu_state = "pause"
                previous_state = "options"
            else:
                game_start = False
                menu_state = "main"
    elif menu_state == "video_settings":
        previous_state = "options"
        draw_bg(bg_choixPerso)
        y = 0
        # ecrit les videos settings
        for settings in option["video_settings"]:
            draw_text(
                "{} : {}".format(settings, option["video_settings"][settings]),
                font, WHITE, SCREEN_WIDTH // 10, SCREEN_HEIGHT // 10 * y)
            y += 1

        if video_button[0].is_Clicked():
            save_options(option)
            menu_state = previous_state
        if video_button[1].is_Clicked():
            menu_state = previous_state
    elif menu_state == "audio_settings":
        previous_state = "options"
        draw_bg(bg_choixPerso)
        y = 0
        # ecrit les audio settings
        for settings in option["audio_settings"]:
            draw_text(
                "{} : {}".format(settings, option["audio_settings"][settings]),
                font, WHITE, 15, SCREEN_HEIGHT // 6 * y)
            y += 1

        if video_button[0].is_Clicked():
            save_options(option)
            menu_state = previous_state
            previous_state = "audio_settings"
        if video_button[1].is_Clicked():
            menu_state = previous_state
    elif menu_state == "key_binding":
        previous_state = "options"
        draw_bg(bg_choixPerso)
        y = 1
        # ecrit les touches
        for settings in option["keyboard_settings"]["p1"]:
            draw_text("Joueur 1", font, WHITE, SCREEN_WIDTH // 8+15, (SCREEN_HEIGHT // 14) - 30)
            draw_text(
                "{} : {}".format(
                    settings, toucheDict[option["keyboard_settings"]["p1"][settings]]),
                font, WHITE, SCREEN_WIDTH // 8, (SCREEN_HEIGHT // 14 + 15) * y)
            draw_text("Joueur 2", font, WHITE, SCREEN_WIDTH // 2+15, (SCREEN_HEIGHT // 14) - 30)
            draw_text(
                "{} : {}".format(
                    settings, toucheDict[option["keyboard_settings"]["p2"][settings]]),
                font, WHITE, SCREEN_WIDTH // 2, (SCREEN_HEIGHT // 14 + 15) * y)
            y += 1
        if video_button[0].is_Clicked():
            save_options(option)
            menu_state = previous_state
        if video_button[1].is_Clicked():
            menu_state = previous_state
    draw_button(menu_state)

    # gestionnaire d'événement
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if (event.key == pygame.K_ESCAPE):
                if menu_state == "in_game":
                    game_paused = True
                    menu_state = "pause"
                else:
                    menu_state = previous_state
        if event.type == pygame.MOUSEBUTTONUP:
            button_clicked = False
        if menu_state == "multi":
            # gestionnaires d'ecriture pour l'ip
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    ip_text = ip_text[:-1]
                else:
                    if len(ip_text) <= 16 and (event.unicode.isdigit()
                                               or event.unicode == "."):
                        ip_text += event.unicode
        if event.type == pygame.QUIT:
            run = False

    # maj ecran
    pygame.display.update()

# quitter jeu
pygame.quit()
