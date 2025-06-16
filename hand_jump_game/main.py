from capture.camera import Camera
from detection.hand_detector import HandDetector
from game.engine import GameEngine

CONFIG = {
    'size': (800, 400),
    'floor_y': 380,
    'player_img': 'assets/dino_py.png',
    'threshold': 0.3,
    'spawn_interval': 1500,
    'obs_size': (30, 50),
    'obs_speed': 6,
}

if __name__ == '__main__':
    cam = Camera(index=1)
    detector = HandDetector()
    game = GameEngine(cam, detector, CONFIG)
    game.run()