import kivy

import camera
from python_functions import analyzing_function
from classes import Input, Sample

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.image import Image
from kivy.graphics import Color, Line
from os.path import getmtime


def is_point_inside_ellipse(x, y, center_x, center_y, a, b):
    """
    Check if a point (x, y) is inside the ellipse defined by (center_x, center_y, a, b).
    """
    # Calculate the value of the ellipse equation
    value = ((x - center_x) ** 2) / (a ** 2) + ((y - center_y) ** 2) / (b ** 2)

    return value <= 1


class TakeAPicScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')
        self.camera = camera.CameraClick()
        self.button = Button(
            text="Go to edit photo",
            on_release=self.go_to_second,
            size_hint=(0.2, 0.1),
            pos_hint={'x': 0.4, 'y': 0.3}
        )
        layout.add_widget(self.camera)
        layout.add_widget(self.button)
        self.add_widget(layout)

    def go_to_second(self, instance):
        self.manager.current = 'edit pic'


class EditPicScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')
        self.image = Image(source='try.png')
        layout.add_widget(self.image)
        self.add_widget(layout)
        self.last_modified = None
        self.painter = EllipseDrawer(my_img=self.image)
        self.painter.pos = self.image.pos
        self.painter.size = self.image.size
        self.add_widget(self.painter)
        self.back_button = Button(
            text="Go back to the camera",
            on_release=self.go_to_first,
            size_hint=(0.2, 0.1),
            pos_hint={'x': 0.2, 'y': 0}
        )
        self.clear_button = Button(
            text="Clear Drawing",
            on_press=self.painter.clear_drawing_canvas,
            size_hint=(0.2, 0.1),
            pos_hint={'x': 0.4, 'y': 0}
        )
        self.analyse_button = Button(
            text="analyse",
            on_press=self.painter.active_analyzing,
            size_hint=(0.2, 0.1),
            pos_hint={'x': 0.6, 'y': 0}
        )
        layout.add_widget(self.back_button)
        layout.add_widget(self.clear_button)
        layout.add_widget(self.analyse_button)

    def update_image(self):
        current_modified_time = getmtime(self.image.source)
        if current_modified_time != self.last_modified:
            self.image.reload()
            self.last_modified = current_modified_time

    def go_to_first(self, instance):
        self.manager.current = 'take a pic'


class EllipseDrawer(BoxLayout):
    def __init__(self, my_img, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.myImage = my_img
        self.canvas = self.myImage.canvas
        self.ellipses = []
        self.whichEllipse = None
        self.drawing = False

    def on_touch_down(self, touch):
        if self.myImage.collide_point(*touch.pos):
            self.drawing = True
            for index in range(len(self.ellipses)):
                ellipse = self.ellipses[index].ellipse
                if is_point_inside_ellipse(
                        touch.x, touch.y,
                        ellipse[0] + (ellipse[2]/2), ellipse[1] + (ellipse[3]/2),
                        ellipse[2]/2, ellipse[3]/2
                ):
                    self.whichEllipse = index
            print(self.whichEllipse)
            if self.whichEllipse is None:
                with self.canvas:
                    Color(0.5, 1, 1)
                    line_ellipse = Line(ellipse=(touch.x - 10, touch.y - 10, 20, 20), width=3)
                    self.ellipses.append(line_ellipse)

    def on_touch_move(self, touch):
        if self.drawing and self.myImage.collide_point(*touch.pos):
            line_ellipse = self.ellipses[-1 if self.whichEllipse is None else self.whichEllipse]
            line_ellipse.ellipse = (
                line_ellipse.ellipse[0], line_ellipse.ellipse[1],
                touch.x - line_ellipse.ellipse[0], touch.y - line_ellipse.ellipse[1]
            )

    def on_touch_up(self, touch):
        self.drawing = False
        self.whichEllipse = None

    def clear_drawing_canvas(self, instance):
        for ellipse in self.ellipses:
            self.canvas.remove(ellipse)
        self.ellipses = []

    def active_analyzing(self, instance):
        ctr_ellipse = self.ellipses[0].ellipse
        control = Sample(ctr_ellipse[0] + (ctr_ellipse[2]/2), ctr_ellipse[1] + (ctr_ellipse[3]/2),
                         ctr_ellipse[2], ctr_ellipse[3])
        samples_ellipses = []
        for index in range(len(self.ellipses)):
            ellipse = self.ellipses[index].ellipse
            sample = Sample(ellipse[0] + (ellipse[2]/2), ellipse[1] + (ellipse[3]/2), ellipse[2], ellipse[3])
            samples_ellipses.append(sample)
        input_for_analysis = Input(self.myImage.source, control, samples_ellipses)
        analyzing_function(input_for_analysis)


class MyApp(App):

    def build(self):
        sm = ScreenManager()
        take_a_pic_screen = TakeAPicScreen(name='take a pic')
        edit_pic_screen = EditPicScreen(name='edit pic')

        edit_pic_screen.bind(on_enter=lambda instance: edit_pic_screen.update_image())

        sm.add_widget(take_a_pic_screen)
        sm.add_widget(edit_pic_screen)
        return sm


if __name__ == '__main__':
    MyApp().run()
