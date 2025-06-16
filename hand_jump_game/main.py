from capture.camera import Camera
from detection.hand_detector import HandDetector
from game.engine import GameEngine

CONFIG = {
    'size': (1200, 600),
    'player_x': 100,
    'floor_y': 600,
    'player_img': 'assets/dino_py.png',
    'background_img': 'assets/jungle_test.png',
    'player_scale': 0.4,        # Dino size
    'threshold': 0.3,
    'spawn_interval': 1500,
    'spawn_jitter': 1000,
    'obs_size': (30, 50),
    'obs_speed': 6,
}

if __name__ == '__main__':
    cam = Camera(index=1)
    detector = HandDetector()
    game = GameEngine(cam, detector, CONFIG)
    game.run()