"""
Main script for wish card app.
:define Functions for constructing login and sign up screens, and building main app.
"""

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
import json
from hoverable import HoverBehavior
from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior
from datetime import datetime
import glob
from pathlib import Path
import random

Builder.load_file('design.kv')

"""
Construct Login screen.
:Define functions of checking username and password.
"""
class LoginScreen(Screen):
    def sign_up(self):
        self.manager.current = "sign_up_screen"
    def login(self, uname, pword):
        with open("users.json") as file:
            users = json.load(file)
            if uname in users:
                if pword == users[uname]['password']:
                    self.manager.current = "login_screen_success"
                else:
                    self.ids.login_wrong.text = "Wrong Password"
            else:
                self.ids.login_wrong.text = "No Username in Our Database"

"""
Construct Success screen.
:Give wish card hint by randomly choose a greeting message from the txt file of the holiday as specified by the user.
"""
class LoginScreenSuccess(Screen):
    def logout(self):
        self.manager.current = "login_screen"
    def get_wishes(self, holiday):
        holiday = holiday.lower()
        available_holiday = glob.glob("wishes/*txt")
        available_holiday = [Path(filename).stem for filename in 
                            available_holiday]
        if holiday in available_holiday:
            with open(f"wishes/{holiday}.txt") as file:
                wishes = file.readlines()
            self.ids.wishes.text = random.choice(wishes)
        else:
            self.ids.wishes.text = "Try another type of wish card!"
"""
Image Button.
"""
class ImageButton(ButtonBehavior, HoverBehavior, Image):
    pass

"""
Construct SignUp screen.
:Define structure for user profile, save the profile to json file.
"""
class SignUpScreen(Screen):
    def add_user(self, uname, pword):
        with open("users.json") as file:
            users = json.load(file)

        users[uname] = {'username': uname,
                        'password': pword,
                        'created': datetime.now().strftime("%Y-%m-%d %H-%M-%S")}

        with open('users.json', 'w') as file:
            json.dump(users, file)

        self.manager.current = "sign_up_screen_success"

"""
Construct SignUp success screeen.
"""
class SignUpScreenSuccess(Screen):
    def login(self):
        self.manager.transition.direction = "right"
        self.manager.current = "login_screen"

"""
RootWidget.
"""
class RootWidget(ScreenManager):
    pass

"""
MainApp.
:Return rootwidget
"""
class MainApp(App):
    def build(self):
        return RootWidget()

if __name__ == "__main__":
    MainApp().run()
    
