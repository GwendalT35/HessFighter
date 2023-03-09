import pygame


class Button():

    def __init__(self, x, y, image, scale, windowSize, nom=""):
        self.windowX = windowSize[0]
        self.windowY = windowSize[1]
        self.image = image
        self.scale = scale
        self.width, self.height = self.image.get_rect().size
        self.width *= self.scale
        self.height *= self.scale
        self.x = x
        self.y = y
        self.rect = self.image.get_rect()
        self.nom = nom

    def draw(self, surface):
        # draw button on screen
        surface.blit(self.image,
                     (self.x - self.width // 2, self.y - self.height // 2))

    def is_Clicked(self, surface):
        action = False
        # get mouse position
        pos = pygame.mouse.get_pos()

        # set the button position
        self.rect.center = (self.x, self.y)

        # check mouseover and clicked conditions
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1:
                action = True
        return action