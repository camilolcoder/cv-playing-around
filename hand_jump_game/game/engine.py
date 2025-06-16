import pygame
import cv2
import random
from game.player import Player
from game.obstacle import Obstacle

class GameEngine:
    def __init__(self, camera, detector, config):
        pygame.init()
        self.screen = pygame.display.set_mode(config['size'])
        pygame.display.set_caption('Hand-Jump Dino Game')
        self.clock = pygame.time.Clock()
        self.camera = camera
        self.detector = detector

        # Load background
        self.background = pygame.image.load(config['background_img']).convert()

        # Player setup
        self.player = Player(
            config['player_x'],
            config['floor_y'],
            config['player_img'],
            scale=config.get('player_scale', 0.5)
        )
        self.player._floor_y = config['floor_y']

        # Groups
        self.obstacles = pygame.sprite.Group()
        self.sprites = pygame.sprite.Group(self.player)

        # Spawn timing
        self.last_spawn = pygame.time.get_ticks()
        self.config = config
        self.spawn_jitter = config.get('spawn_jitter', 1000)

        # Status
        self.last_ap = 0
        self.status_font = pygame.font.SysFont(None, 32)

    def run(self):
        running = True
        while running:
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    running = False

            # Hand detection
            ret, frame = self.camera.read()
            if not ret:
                break
            ap = self.detector.aperture(frame)
            action = None
            if ap is not None:
                if ap > self.config['threshold'] and self.last_ap <= self.config['threshold']:
                    self.player.jump()
                    action = 'JUMP'
                elif ap < self.last_ap:
                    action = 'STAY'
                self.last_ap = ap

            # Background
            self.screen.blit(self.background, (0, 0))

            # Draw camera feed (small overlay)
            cam_frame = self.detector.draw(frame)
            cam_surf = pygame.image.frombuffer(
                cv2.resize(cam_frame, (200, 160)).tobytes(), (200, 160), 'BGR'
            )
            self.screen.blit(cam_surf, (10, 10))

            # Spawn obstacles with random interval
            now = pygame.time.get_ticks()
            interval = self.config['spawn_interval'] + random.randint(0, self.spawn_jitter)
            if now - self.last_spawn >= interval:
                obs = Obstacle(
                    self.config['size'][0] + 20,
                    self.config['floor_y'],
                    self.config['obs_size'],
                    self.config['obs_speed'],
                )
                self.obstacles.add(obs)
                self.sprites.add(obs)
                self.last_spawn = now

            # Update & draw
            self.sprites.update()
            self.screen.blit(self.player.image, self.player.rect)
            for obs in self.obstacles:
                self.screen.blit(obs.image, obs.rect)

            # Collision detection
            if pygame.sprite.spritecollideany(self.player, self.obstacles):
                collide_text = self.status_font.render('Collision!', True, (255, 0, 0))
                self.screen.blit(collide_text, (self.config['size'][0]//2 - 50, 50))

            # Status text
            if action:
                text = 'Expanding → JUMP' if action=='JUMP' else 'Contracting → STAY'
                status_surf = self.status_font.render(text, True, (0, 0, 0))
                self.screen.blit(status_surf, (200, 10))

            pygame.display.flip()
            self.clock.tick(60)

        self.camera.release()
        pygame.quit()