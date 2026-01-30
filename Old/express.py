# Peach Telemetry data analysis program | Developed by Ben Loggie
# This file runs the front end of the Shiny webpage.

# Module import
from shiny.express import *
from shiny.ui import *
from shiny import reactive

import pandas as pd
import matplotlib.pyplot as plt
import os

from Modules import Initialize, Excel_Export, sort_Data, Subroutines

# Predefined identifiers
colours = {'1': '#34fc49', '2': '#fc2e04', '3': '#0000f7', '4': '#000000', '5': '#3c752a', '6': '#a42904', '7': '#2afcff', '8': '#fe9d29'}
session_Files = 'Storage/Sessions'

# User interface
with ui.card(id='Main'):
    with ui.card(id='LoginPage'):
        ui.input_text(id='login_Username', label='Enter Username')
        ui.input_password(id='login_Password', label='Enter password')
        ui.input_action_button(id='Enter_Credentials', label='Login')
    

    with ui.accordion():
        ui.accordion_panel(title='Test')

        

def insert_Element(element, location):
    ui.insert_ui(element, selector=location)

def load_Session_Page(fileData):
    a = 2

def load_Session_Selector():
    insert_Element(ui.card(id='Sessions'), '#Main')
    insert_Element(ui.card_header('Select a session'), '#Sessions')

    def create_File_Card(fileName, iteration):
        insert_Element(ui.card(id='Holder'), '#Sessions')
        insert_Element(ui.card_header(fileName), '#Holder')
        insert_Element(ui.input_action_button(id=f'Action_{iteration}', label='Load File'), '#Holder')

        @reactive.effect
        @reactive.event(input[f'Action_{iteration}'])
        def _():
            file = open(f'{session_Files}/{fileName}')
            ui.notification_show(f'Loading {fileName}', duration=4)
            ui.remove_ui(selector='#Sessions')
            file_Data = Initialize.Initialize_Data(file, 8)
            load_Session_Page(file_Data)

    iteration = 0
    for file in os.listdir(session_Files):
        create_File_Card(file, str(iteration))
        iteration += 1

# Login page check
@reactive.effect
@reactive.event(input.Enter_Credentials)
def check():
    Username = input.login_Username()
    Password = input.login_Password()
    if Username == 'a' and Password == 'a':
        ui.notification_show('Login success!', duration=2)
        ui.remove_ui(selector='#LoginPage')
        load_Session_Selector()
    else:
        ui.notification_show('Login failed!', duration=2)

