import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()
        self.image = pygame.image.load(image).convert_alpha()
        self.rect = self.image.get_rect(midbottom=(x, y))
        self.vel_y = 0
        self.gravity = 0.8
        self.jump_speed = -15

    def update(self):
        self.vel_y += self.gravity
        self.rect.y += self.vel_y
        if self.rect.bottom >= self._floor_y:
            self.rect.bottom = self._floor_y
            self.vel_y = 0

    def jump(self):
        if self.rect.bottom >= self._floor_y:
            self.vel_y = self.jump_speed