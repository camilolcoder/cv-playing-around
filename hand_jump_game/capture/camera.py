import cv2

class Camera:
    def __init__(self, index=1, backend=cv2.CAP_DSHOW):
        self.cap = cv2.VideoCapture(index, backend)

    def read(self):
        ret, frame = self.cap.read()
        return ret, frame

    def release(self):
        self.cap.release()