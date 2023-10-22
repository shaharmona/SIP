import cv2


class Point:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def update_position(self, x, y):
        self.x = x
        self.y = y

    def get_position(self):
        return self.x, self.y


class Sample:

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
    def __init__(self, img_path, control_sample, check_samples):
        self.img = img_path
        self.control = control_sample
        self.samples = check_samples
