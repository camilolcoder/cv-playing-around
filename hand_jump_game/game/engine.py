import pygame
from game.player import Player
from game.obstacle import Obstacle

class GameEngine:
    def __init__(self, camera, detector, config):
        pygame.init()
        self.screen = pygame.display.set_mode(config['size'])
        self.clock = pygame.time.Clock()
        self.camera = camera
        self.detector = detector

        self.player = Player(100, config['floor_y'], config['player_img'])
        self.player._floor_y = config['floor_y']
        self.sprites = pygame.sprite.Group(self.player)

        self.spawn_timer = 0
        self.config = config

    def run(self):
        running = True
        last_ap = 0
        while running:
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    running = False

            ret, frame = self.camera.read()
            if not ret:
                break

            ap = self.detector.aperture(frame)
            if ap and ap > self.config['threshold'] and last_ap <= self.config['threshold']:
                self.player.jump()
            last_ap = ap or last_ap

            # draw landmarks overlay
            display_frame = self.detector.draw(frame)
            surf = pygame.image.frombuffer(
                display_frame.tobytes(), display_frame.shape[1::-1], 'BGR'
            )
            self.screen.blit(surf, (0, 0))

            # spawn obstacles
            now = pygame.time.get_ticks()
            if now - self.spawn_timer > self.config['spawn_interval']:
                obs = Obstacle(
                    self.config['size'][0] + 20,
                    self.config['floor_y'],
                    self.config['obs_size'],
                    self.config['obs_speed'],
                )
                self.sprites.add(obs)
                self.spawn_timer = now

            self.sprites.update()
            self.sprites.draw(self.screen)

            pygame.display.flip()
            self.clock.tick(60)

        self.camera.release()
        pygame.quit()