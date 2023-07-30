import cv2


class Point:
    def __init__(self):
        self.x = 0
        self.y = 0

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def update_position(self, x, y):
        self.x = x
        self.y = y

    def get_position(self):
        return self.x, self.y


class Sample:
    def __init__(self):
        self.middle = Point()
        self.r1 = 0
        self.r2 = 0

    def __init__(self, x, y, r1, r2):
        self.middle = Point(x, y)
        self.r1 = r1
        self.r2 = r2

    def update_sample(self, x, y, r1, r2):
        self.middle.update_position(x, y)
        self.r1 = r1
        self.r2 = r2

    def get_area(self):
        return self.middle, self.r1, self.r2


class Input:
    def __init__(self):
        path = r"C:\Users\shaha\sample's_infection_percent\test .jpg"
        self.img = cv2.imread(path, 0)
        self.control = Sample(780, 580, 50, 100)
        self.samples = [Sample(900, 580, 50, 100), Sample(1480, 580, 50, 100)]

