import pygame
import time


class Fighter():
    def __init__(self, player, x, y, flip, data, sprite_sheet, animation_steps, sound):
        self.player = player
        self.size = data[0]
        self.image_scale = data[1]
        self.offset = data[2]
        self.flip = flip
        self.animation_list = self.load_images(sprite_sheet, animation_steps)
        self.action = 0  # 0:idle 1 run 2 jump 3 attack1 4 attack2 5 hit 6 death
        self.frame_index = 0
        self.image = self.animation_list[self.action][self.frame_index]
        self.update_time = pygame.time.get_ticks()
        self.rect = pygame.Rect((x, y, 80, 180))
        self.vel_y = 0
        self.running = False
        self.jump = False
        self.attacking = False
        self.attack_type = 0
        self.attack_cooldown = 0
        self.attack_sound = sound
        self.hit = False
        self.health = 100
        self.alive = True

    def load_images(self, sprite_sheet, animation_steps):
        animation_list = []
        for y, animation in enumerate(animation_steps):
            temp_img_list = []
            for x in range(animation):
                temp_img = sprite_sheet.subsurface(
                    x * self.size, y * self.size, self.size, self.size)
                temp_img_list.append(pygame.transform.scale(
                    temp_img, (self.size * self.image_scale, self.size * self.image_scale)))
            animation_list.append(temp_img_list)
        return animation_list

    def move(self, screen_width, screen_height, surface, target, round_over):
        SPEED = 10
        GRAVITY = 2
        dx = 0
        dy = 0
        self.running = False
        self.attack_type = 0

        # get keypresses
        key = pygame.key.get_pressed()

       #
        if self.attacking == False and self.alive == True and round_over == False:
            # verifie les controles du joueur 1
            if self.player == 1:
                # mouvement
                if key[pygame.K_q]:
                    dx = -SPEED
                    self.running = True
                if key[pygame.K_d]:
                    dx = SPEED
                    self.running = True
                # saut
                if key[pygame.K_z] and self.jump == False:
                    self.vel_y = -30
                    self.jump = True

                # attaque
                if key[pygame.K_r] or key[pygame.K_t]:
                    self.attack(target)
                    if key[pygame.K_a]:
                        self.attack_type = 1
                    if key[pygame.K_e]:
                        self.attack_type = 2

            # verifie les controles du joueur 2
            if self.player == 2:
                # mouvement
                if key[pygame.K_LEFT]:
                    dx = -SPEED
                    self.running = True
                if key[pygame.K_RIGHT]:
                    dx = SPEED
                    self.running = True
                # saut
                if key[pygame.K_UP] and self.jump == False:
                    self.vel_y = -30
                    self.jump = True

                # attaque
                if key[pygame.K_KP1] or key[pygame.K_KP2]:
                    self.attack(target)
                    if key[pygame.K_KP1]:
                        self.attack_type = 1
                    if key[pygame.K_KP2]:
                        self.attack_type = 2

        # appliquer graviter
        self.vel_y += GRAVITY
        dy += self.vel_y

        # bloquer le joueur à l'écran
        if self.rect.left + dx < 0:
            dx = -self.rect.left
        if self.rect.right + dx > screen_width:
            dx = screen_width - self.rect.right
        if self.rect.bottom + dy > screen_height - 110:
            self.vel_y = 0
            self.jump = False
            dy = screen_height - 110 - self.rect.bottom

        if target.rect.centerx > self.rect.centerx:
            self.flip = False
        else:
            self.flip = True

        # temps de recuperation attaques
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1

        # maj position joueur
        self.rect.x += dx
        self.rect.y += dy

   # Evolution animation
    def update(self):
        # verifie quel actions le jouer fait
        if self.health <= 0:
            self.health = 0
            self.alive = False
            self.update_action(6)  # 6:mort
        elif self.hit == True:
            self.update_action(5)  # 5:Se faire taper
        elif self.attacking == True:
            if self.attack_type == 1:
                self.update_action(3)  # 3:attaque 1
            elif self.attack_type == 2:
                self.update_action(4)  # 4:attaque 2
        elif self.jump == True:
            self.update_action(2)  # 2:sauter
        elif self.running == True:
            self.update_action(1)  # 1:courir
        else:
            self.update_action(0)  # 0:inactif

        animation_cooldown = 100
        # evolution de l'image
        self.image = self.animation_list[self.action][self.frame_index]
        # Verifier qu'il se soit écoulé assez de temps depuis la derniere animation
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.frame_index += 1
            self.update_time = pygame.time.get_ticks()
        # Verifie si l'animation est terminé
        if self.frame_index >= len(self.animation_list[self.action]):
            # verifie si le joueur est mort
            if self.alive == False:
                self.frame_index = len(self.animation_list[self.action]) - 1
            else:
                self.frame_index = 0
                # verifie si une attaque a ete execute
                if self.action == 3 or self.action == 4:
                    self.attacking = False
                    self.attack_cooldown = 20
                # verifie que les degats ont ete recus
                if self.action == 5:
                    self.hit = False
                    # arrete le coup dun joueur si il etait au milieu dune attaque
                    self.attacking = False
                    self.attack_cooldown = 20

    def attack(self, target):
        if self.attack_cooldown == 0:
            # execution de l'attaque
            self.attacking = True
            self.attack_sound.play()
            attacking_rect = pygame.Rect(self.rect.centerx - (
                2 * self.rect.width * self.flip), self.rect.y, 2 * self.rect.width, self.rect.height)
            if attacking_rect.colliderect(target.rect):
                target.health -= 10
                target.hit = True

    def update_action(self, new_action):
        # verifie si la nouvelle action est different de la precedente
        if new_action != self.action:
            self.action = new_action
            # change l'etat de l'animation
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    def draw(self, surface):
        img = pygame.transform.flip(self.image, self.flip, False)
        surface.blit(img, (self.rect.x - (self.offset[0] * self.image_scale), self.rect.y - (
            self.offset[1] * self.image_scale)))
