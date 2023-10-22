from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
import time


Builder.load_string('''
<CameraClick>:
    orientation: 'vertical'
    Camera:
        id: camera
        resolution: (6400, 4800)
        play: False
        height: '100dp'
    ToggleButton:
        text: 'Play'
        on_press: camera.play = not camera.play
        pos_hint: {'x': 0.8, 'y': 0.3}
        size_hint: (0.2, 0.1)
    Button:
        background_color: 0, 0.7, 0.3, 1
        color: 1, 1, 1, 1
        pos_hint: {'x': 0.6, 'y': 0.3}
        size_hint: (0.2, 0.1)
        text: 'Capture'
        on_press: camera.play and root.capture()
''')


class CameraClick(BoxLayout):
    def capture(self):
        '''
        Function to capture the images and give them the names
        according to their captured time and date.
        '''
        camera = self.ids['camera']
        # timestr = time.strftime("%Y%m%d_%H%M%S")
        camera.export_to_png("try.png")
        print("Captured")
        name = "try.png"
        return name
