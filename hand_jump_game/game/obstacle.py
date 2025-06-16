import pygame

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, x, y, size, speed):
        super().__init__()
        self.image = pygame.Surface(size)
        self.image.fill((200, 50, 50))
        self.rect = self.image.get_rect(midbottom=(x, y))
        self.speed = speed

    def update(self):
        self.rect.x -= self.speed
        if self.rect.right < 0:
            self.kill()