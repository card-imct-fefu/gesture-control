import time


class FpsCounter:

    def __init__(self):
        self.pTime = 0
        self.cTime = 0

    def get(self):
        self.cTime = time.time()
        fps = 1 / (self.cTime - self.pTime)
        self.pTime = self.cTime
        return int(fps)
