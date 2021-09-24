import os

os.environ['DISPLAY'] = ":0.0"
# os.environ['KIVY_WINDOW'] = 'egl_rpi'

import spidev
import os
from time import sleep
import RPi.GPIO as GPIO
from pidev.stepper import stepper
from Slush.Devices import L6470Registers

spi = spidev.SpiDev()
from kivy.app import App
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.animation import Animation
from pidev.MixPanel import MixPanel
from pidev.kivy.PassCodeScreen import PassCodeScreen
from pidev.kivy.PauseScreen import PauseScreen
from pidev.kivy import DPEAButton
from pidev.kivy import ImageButton
from pidev.kivy.selfupdatinglabel import SelfUpdatingLabel

from pidev.Joystick import Joystick
from datetime import datetime
from threading import Thread
from time import sleep

time = datetime
joy = Joystick(0, False)

MIXPANEL_TOKEN = "x"
MIXPANEL = MixPanel("Project Name", MIXPANEL_TOKEN)

SCREEN_MANAGER = ScreenManager()
MAIN_SCREEN_NAME = 'main'
ADMIN_SCREEN_NAME = 'admin'
SECOND_SCREEN_NAME = 'second'


class ProjectNameGUI(App):
    """
    Class to handle running the GUI Application
    """

    def build(self):
        """
        Build the application
        :return: Kivy Screen Manager instance
        """
        return SCREEN_MANAGER


Window.clearcolor = (1, 1, 1, 1)  # White


class MainScreen(Screen):
    """
    Class to handle the main screen and its associated touch events
    """
    rotations = 500

    s0 = stepper(port=0, micro_steps=32, hold_current=20, run_current=20, accel_current=20, deaccel_current=20,
                 steps_per_unit=200, speed=5)

    s1 = stepper(port=0, micro_steps=32, hold_current=20, run_current=20, accel_current=20, deaccel_current=20,
                 steps_per_unit=200, speed=5)

    def joy_update(self):  # This should be inside the MainScreen Class
        while True:
            self.mouse.x += (joy.get_axis("x")) * 10
            self.mouse.y += (joy.get_axis("y")) * -10
            sleep(.01)

    def start_joy_thread(self):  # This should be inside the MainScreen Class
        Thread(target=self.joy_update).start()

    @staticmethod
    def transition_to_second_screen():
        SCREEN_MANAGER.current = SECOND_SCREEN_NAME

    def pressed(self):
        """
        Function called on button touch event for button with id: testButton
        :return: None
        """
        if self.btn.text == "on":
            self.btn.text = "off"
        elif self.btn.text == "off":
            self.btn.text = "on"
        print("Callback from MainScreen.pressed()")

    def mover(self):
        anim = Animation(x=50) + Animation(size=(80, 80), duration=2.) + Animation(x=self.width * 0.5) + Animation(
            size=(150, 150), duration=3.)
        anim.start(self.mouse)

    def direction_switch(self):
        self.s0.start_relative_move(-(self.rotations))
        self.s0.start_relative_move(10)

    def pushed(self):
        if self.motor.text == "motor-on":
            self.motor.text = "motor-off"
        elif self.motor.text == "motor-off":
            self.motor.text = "motor-on"

    def counterpressed(self):
        self.counter.text = str(int(self.counter.text) + 1)

    def move_motor(self):
        self.s0.start_relative_move(self.rotations)
        sleep(2)
        self.s0.softStop()

    def motor_speed(self):
        self.s1.set_speed(self.motorslider.value)

    def admin_action(self):
        """
        Hidden admin button touch event. Transitions to passCodeScreen.
        This method is called from pidev/kivy/PassCodeScreen.kv
        :return: None
        """
        SCREEN_MANAGER.current = 'passCode'


class SecondScreen(Screen):
    @staticmethod
    def transition_to_main_screen():
        SCREEN_MANAGER.current = MAIN_SCREEN_NAME


class AdminScreen(Screen):
    """
    Class to handle the AdminScreen and its functionality
    """

    def __init__(self, **kwargs):
        """
        Load the AdminScreen.kv file. Set the necessary names of the screens for the PassCodeScreen to transition to.
        Lastly super Screen's __init__
        :param kwargs: Normal kivy.uix.screenmanager.Screen attributes
        """
        Builder.load_file('AdminScreen.kv')

        PassCodeScreen.set_admin_events_screen(
            ADMIN_SCREEN_NAME)  # Specify screen name to transition to after correct password
        PassCodeScreen.set_transition_back_screen(
            MAIN_SCREEN_NAME)  # set screen name to transition to if "Back to Game is pressed"
        PassCodeScreen.set_transition_back_screen(SECOND_SCREEN_NAME)
        super(AdminScreen, self).__init__(**kwargs)

    @staticmethod
    def transition_back():
        """
        Transition back to the main screen
        :return:
        """
        SCREEN_MANAGER.current = MAIN_SCREEN_NAME

    @staticmethod
    def shutdown():
        """
        Shutdown the system. This should free all steppers and do any cleanup necessary
        :return: None
        """
        os.system("sudo shutdown now")

    @staticmethod
    def exit_program():
        """
        Quit the program. This should free all steppers and do any cleanup necessary
        :return: None
        """
        quit()


"""
Widget additions
"""

Builder.load_file('main.kv')
SCREEN_MANAGER.add_widget(MainScreen(name=MAIN_SCREEN_NAME))
SCREEN_MANAGER.add_widget(PassCodeScreen(name='passCode'))
SCREEN_MANAGER.add_widget(PauseScreen(name='pauseScene'))
SCREEN_MANAGER.add_widget(AdminScreen(name=ADMIN_SCREEN_NAME))
SCREEN_MANAGER.add_widget(SecondScreen(name=SECOND_SCREEN_NAME))

"""
MixPanel
"""


def send_event(event_name):
    """
    Send an event to MixPanel without properties
    :param event_name: Name of the event
    :return: None
    """
    global MIXPANEL

    MIXPANEL.set_event_name(event_name)
    MIXPANEL.send_event()


if __name__ == "__main__":
    # send_event("Project Initialized")
    # Window.fullscreen = 'auto'
    ProjectNameGUI().run()
