import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, image_path, scale=0.5):
        super().__init__()
        # Load original sprite
        orig = pygame.image.load(image_path).convert_alpha()
        
        # Scale dimensions
        w, h = orig.get_size()
        new_size = (int(w * scale), int(h * scale))
        self.image = pygame.transform.scale(orig, new_size)

        # Set position
        self.rect = self.image.get_rect(midbottom=(x, y))
        self._floor_y = y

        self.vel_y = 0
        self.gravity = 0.8
        self.jump_speed = -15

    def update(self):
        self.vel_y += self.gravity
        self.rect.y += self.vel_y
        # Floor collision
        if self.rect.bottom >= self._floor_y:
            self.rect.bottom = self._floor_y
            self.vel_y = 0

    def jump(self):
        if self.rect.bottom >= self._floor_y:
            self.vel_y = self.jump_speed