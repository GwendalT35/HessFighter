import pygame


class Button():

    def __init__(self, x, y, image, scale, windowSize):
        self.windowX = windowSize[0]
        self.windowY = windowSize[1]
        self.image = image
        self.scale = scale
        self.width, self.height = self.image.get_rect().size
        self.width *= self.scale
        self.height *= self.scale
        self.x = x
        self.y = y
        self.clicked = False
        self.rect = self.image.get_rect()

    def draw(self, surface):
        action = False
        # get mouse position
        pos = pygame.mouse.get_pos()

        # set the button position
        self.rect.center = (self.x, self.y)

        # check mouseover and clicked conditions
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and not self.clicked:
                self.clicked = True
                action = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

            # draw button on screen
            surface.blit(self.image,
                         (self.x - self.width // 2, self.y - self.height // 2))

        return action
