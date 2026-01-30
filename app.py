# Peach Telemetry data analysis program | Developed by Ben Loggie
# This file runs the front end of the Shiny webpage.

import time
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import string
import random
import json
from ipyleaflet import Map, Polyline
from shinywidgets import output_widget, render_widget  
from requests import get
from pathlib import Path
from shiny import *
from Modules import Initialize, Excel_Export, sort_Data, Subroutines, Database, Gold_Target, Plot, Email
import Modules.Variables as Variables

# Variables
seat_colours = Variables.seat_colours
sample_colours = Variables.sample_colours
markers = Variables.markers
bar_colours = Variables.bar_colours
session_colours = Variables.session_colours

# Themes
my_theme = (
    ui.Theme("shiny")
    .add_defaults(
        shp_maroon="#800000",
        bg_grey='#474545',
    )
    .add_mixins(
        background_color='$bg_grey',
        headings_color="$shp_maroon",
        nav_pills_link_active_bg="$shp_maroon",
        nav_link_color = "$shp_maroon",
        nav_link_hover_color = "$shp_maroon",
        progress_bar_bg = "$shp_maroon",
    )
)

# Main UI
app_ui = ui.page_sidebar(
    ui.sidebar(
        ui.card(
            ui.card_header('Authentication'),
            ui.input_text(id='username', label='Username'),
            ui.input_password(id='password', label='Password'),
            ui.input_action_button(id='Login', label='Login')
        ),
        ui.card(
            ui.layout_column_wrap(
                ui.output_text_verbatim(id='software_information'),
            ),
            full_screen=True
        ),   
        ui.input_dark_mode(mode='light')
    ),

    # Main Content
    ui.navset_card_pill(  

        ui.nav_panel("Upload",
            ui.card(
                ui.card_header('Upload file'),
                ui.input_selectize(  
                    "selectedCategory",  
                    "Select a boat category:",  
                    {
                        "U19_M8+": "U19_M8+", 
                        "U19_W8+": "U19_W8+", 
                        "U19_M4-": "U19_M4-",
                        "U19_W4-": "U19_W4-",
                    },  
                ),  
                ui.input_file(id="file1", label="Choose .txt File", accept=[".txt"], multiple=True, button_label='Browse', placeholder='No file selected.'),
                ui.input_action_button(id='Execute', label='Load file'),
                full_screen=True
            ),      
        ),

        ui.nav_panel("Overview",
            ui.card(
                ui.output_data_frame(id='session_Report'),
                full_screen=True
            ),
            ui.card(
                ui.output_data_frame(id='session_Report_Crew'),
                full_screen=True
            ),
            ui.card(
                output_widget("map"),
                full_screen=True
            ),
        ),

        ui.nav_panel("Session Report",
            ui.card(
                ui.card_header("Session description & distribution of samples."),
                ui.output_plot(id='session_Rate_MS_Graph'),
                ui.output_data_frame(id='session_Summary'),
                #ui.output_data_frame(id='session_Summary_GPS'),
                ui.output_plot(id='session_Acceleration_Curve'),
                ui.output_plot(id='session_Boat_Speed_Curve'),
                ui.accordion(
                    ui.accordion_panel("Stroke Rate",
                        ui.card(
                            ui.card_header('Rate'), 
                            ui.output_data_frame(id='rate_Data'), 
                            full_screen=True
                        ),         
                        ui.card(
                            ui.layout_column_wrap( 
                                ui.input_numeric("rateminvalue", "Min Y Axis", None, min=0, max=500),  
                                ui.input_numeric("ratemaxvalue", "Max Y Axis", None, min=0, max=500), 
                            ),
                            ui.output_plot(id='rate_plot'),
                            full_screen=True
                        ),                  
                    ),

                    ui.accordion_panel("Power",
                        ui.output_text_verbatim(id='StatsForNerdsText'),
                        ui.card(
                            ui.card_header('Raw Power data'), 
                            ui.output_data_frame(id='watt_Data'), 
                            full_screen=True
                        ),     
                        ui.card(
                            ui.layout_column_wrap(
                                ui.input_numeric("wattsminvalue", "Min Y Axis", None, min=50, max=500),  
                                ui.input_numeric("wattsmaxvalue", "Max Y Axis", None, min=50, max=500),  
                                ui.input_switch("plot_Individual_Wattage", "Plot Individual Curve", False),  
                                ui.input_numeric("selected_Seat_Wattage", "Select Seat", 1, min=1, max=8), 
                            ),
                            ui.output_plot(id='wattage_plot'),
                            full_screen=True
                        ), 
                    ),

                    ui.accordion_panel("Arc Length",
                        ui.card(
                            ui.card_header('Arc Length'), 
                            ui.output_data_frame(id='raw_ArcLength'), 
                            full_screen=True
                        ),         
                        ui.card(
                            ui.layout_column_wrap( 
                                ui.input_numeric("arclengthminvalue", "Min Y Axis", 80, min=0, max=500),  
                                ui.input_numeric("arclengthmaxvalue", "Max Y Axis", 100, min=0, max=500), 
                                ui.input_switch("plot_Individual_ArcLength", "Plot Individual Curve", False),  
                                ui.input_numeric("selected_Seat_Length", "Select Seat", 1, min=1, max=8),  
                            ),
                            ui.output_plot(id='arclength_plot'),
                            full_screen=True
                        ),                  
                    ),

                    ui.accordion_panel("Peak Force",
                        ui.card(
                            ui.card_header('Raw Force data'), 
                            ui.output_data_frame(id='force_Data'), 
                            full_screen=True
                        ),     
                        ui.card(
                            ui.layout_column_wrap(
                                ui.input_numeric("forceminvalue", "Min Y Axis", None, min=50, max=500),  
                                ui.input_numeric("forcemaxvalue", "Max Y Axis", None, min=50, max=500), 
                                ui.input_switch("plot_Individual_PeakForce", "Plot Individual Curve", False),  
                                ui.input_numeric("selected_Seat_PeakForce", "Select Seat", 1, min=1, max=8), 
                            ),
                            ui.output_plot(id='force_plot'),
                            full_screen=True
                        ), 
                    ),
                    
                ),
            ),
        ),    

        ui.nav_panel("Individual Report", 
            ui.card(
                ui.card_header("This page shows one rowers data for various samples."),
                ui.layout_column_wrap(
                    ui.input_numeric("rowerSelect_Summary", "Select Seat", 1, min=1, max=8),
                    ui.input_numeric("sample_Select", "Number of Samples", 8, min=2, max=20),  
                ),
                full_screen=True
            ),

            ui.card(
                ui.card_header('Main'),
                ui.output_data_frame(id='rower_Summary_1'), 
                full_screen=True
            ),
            ui.card(
                ui.card_header('Power'),
                ui.output_data_frame(id='rower_Summary_2'), 
                full_screen=True
            ),
            ui.card(
                ui.card_header('Gold Target'),
                ui.output_data_frame(id='rower_Summary_3'), 
                full_screen=True
            ),

            ui.card(
                ui.layout_column_wrap(
                    ui.card(
                        ui.output_plot(id='handle_Force_Curve'),
                        full_screen=True
                    )
                ),
                ui.layout_column_wrap(
                    ui.card(
                        ui.input_switch(id='oar_angle_key', label='Show Legend'),
                        ui.output_plot(id='oar_Angle'),
                        full_screen=True
                    ),
                    ui.card(
                        ui.input_switch(id='wattage_key', label='Show Legend'),
                        ui.output_plot(id='wattage_Linear'),
                        full_screen=True
                    )
                ),

                ui.layout_column_wrap(
                    ui.card(
                        ui.output_plot(id='work_per_stroke'),
                        full_screen=True
                    ),
                    ui.card(
                        ui.output_plot(id='PercentageForce'),
                        full_screen=True
                    )
                ),
            ),

            ui.card(
                ui.layout_column_wrap(
                    ui.input_select(  
                        "curve_p_x_axis",  
                        "X Axis",  
                        {"1A": "Normalized Time", "1B": "GateAngle"},  
                    ),   
                ),
                ui.output_text_verbatim(id="curve_p_data"),  
                ui.output_plot(id='personal_power_curve_plot'),
                full_screen=True
            ),
            ui.card(
                ui.layout_column_wrap(
                    ui.input_select(  
                        "velt_x_axis",  
                        "X Axis",  
                        {"1A": "GateAngle", "1B": "Normalized Time"},  
                    ),   
                ),
                ui.output_text_verbatim(id="velt_p_data"),  
                ui.output_plot(id='velt_individual'),
                full_screen=True
            ),
        ),

        ui.nav_panel("Crew Sampled Report",
            ui.card(
                ui.card_header("This section shows a segment of the session compared to other rowers."),
                ui.layout_column_wrap(
                    ui.input_numeric("sample_Select_Crew", "Select Sample to Analyse (8 Samples)", 1, min=1, max=8), 
                    ui.output_text_verbatim(id='Crew_Sampled_Output'),
                ),
                full_screen=True
            ),
            ui.card(
                ui.card_header("Angles"),
                ui.output_data_frame(id='crew_Sample_Summary_1'),
                full_screen=True
            ),
            ui.card(
                ui.card_header("Power"),
                ui.output_data_frame(id='crew_Sample_Summary_2'),
                full_screen=True
            ),
            ui.card(
                ui.card_header("Syncronisation (ms) - How far away the rower is (in ms) from the stroke seat at each point of the stroke. (+ -> Later) (- -> Earlier)"),
                ui.output_data_frame(id='crew_Report_Syncronisation'),
                ui.layout_column_wrap(
                    ui.input_numeric("stroke_Seat_Selected_Syncronisation", "Select Timing Seat", 8, min=1, max=8),
                    ui.input_numeric("rower_Selected_Syncronisation", "Select Seat", 1, min=1, max=8),
                    ui.input_switch("plot_Individual_Syncronisation", "Plot Individual Seats", False),  
                    ui.input_switch("Sample_Show_Legend_Syncronisation", "Show Legend", True),  
                ),
                ui.card(
                    ui.output_plot(id='Syncronisation_Sample'),
                    full_screen=True
                )
            ),
            ui.card(
                ui.card_header("Ratios"),
                ui.output_data_frame(id='stroke_Percentages_Sample'),
                ui.card(
                    ui.input_switch("ratio_Sample_Show_Legend", "Show Legend", False),
                    ui.output_plot(id='Stroke_Ratios_Sample'),
                    full_screen=True
                )
            ),
        ),

        ui.nav_panel("Crew Averages Report", 
            ui.card(
                ui.card_header('Rower Averaged Angles'), 
                ui.output_data_frame(id='crew_Average_Angles_Data'), 
                full_screen=True
            ),                          

            ui.card(
                ui.card_header('Rower Averaged Power'), 
                ui.output_data_frame(id='crew_Average_Power_Data'), 
                ui.output_plot(id='Wattage_RugPlot'),
                full_screen=True
            ),        

            ui.card(
                ui.card_header("Syncronisation (ms) - How far away the rower is (in ms) from the stroke seat at each point of the stroke. (+ -> Later) (- -> Earlier)"),
                ui.output_data_frame(id='crew_avg_Report_Syncronisation'),
                ui.layout_column_wrap(
                    ui.input_numeric("stroke_Seat_Selected_Average_Syncronisation", "Select Timing Seat", 8, min=1, max=8),
                    ui.input_numeric("rower_Selected_Syncronisation_Average", "Select Seat", 1, min=1, max=8), 
                    ui.input_switch("plot_Individual_Syncronisation_Average", "Plot Individual Seat", False),  
                    ui.input_switch("Average_Show_Legend_Syncronisation", "Show Legend", True),
                ),
                ui.card(
                    ui.output_plot(id='Syncronisation_Average'),
                    full_screen=True
                )
            ),     

            ui.card(
                ui.card_header('Rower Averaged Stroke Breakdown Percentage'), 
                ui.output_data_frame(id='raw_Percentage_Timing'), 
                ui.card(
                    ui.input_switch("ratio_Average_Show_Legend", "Show Legend", False),
                    ui.output_plot(id='ratios_plot'),
                    full_screen=True
                )            
            ),                                 

            ui.card(
                ui.layout_column_wrap(
                    ui.input_numeric("curvemin_y_value", "Min Y Axis", -40, min=-100, max=500),  
                    ui.input_numeric("curvemax_y_value", "Max Y Axis", 140, min=-100, max=500),  
                    ui.input_numeric("curvemin_x_value", "Min X Axis", None, min=0, max=500),  
                    ui.input_numeric("curvemax_x_value", "Max X Axis", None, min=0, max=500),   
                ),
                ui.layout_column_wrap(
                    ui.input_switch("Plot_Individual_Switch", "Plot Individual Curves", False),  
                    ui.input_numeric("rowerSelectGroup", "Select Seat", 1, min=1, max=8), 
                    ui.input_select(  
                        "group_curve_x_axis",  
                        "X Axis",  
                        {"1A": "Normalized Time", "1B": "GateAngle"},  
                    ),   
                ),
                ui.output_plot(id='power_curve_plot'),
                full_screen=True
            ),  

            ui.card(
                ui.layout_column_wrap(
                    ui.input_numeric("vel_min_y_value", "Min Y Axis", -200, min=-300, max=500),  
                    ui.input_numeric("vel_max_y_value", "Max Y Axis", 200, min=-300, max=500),  
                    ui.input_numeric("vel_min_x_value", "Min X Axis", None, min=0, max=500),  
                    ui.input_numeric("vel_max_x_value", "Max X Axis", None, min=0, max=500),  
                ),
                ui.layout_column_wrap(
                    ui.input_switch("vel_plot_individual_switch", "Plot Individual Curves", False),  
                    ui.input_numeric("vel_rower_select", "Select Seat", 1, min=1, max=8), 
                    ui.input_select(  
                        "vel_x_axis",  
                        "X Axis",  
                        {"1A": "GateAngle", "1B": "Normalized Time"},  
                    ),   
                ),
                ui.output_plot(id='GateAngleVel'),
                full_screen=True
            ),

            ui.card(
                ui.card_header('Raw Stroke Timing data'), 
                ui.output_data_frame(id='raw_Timing_Data'), 
                full_screen=True
            ),    
        ),

        ui.nav_panel("Seat Data",
            ui.card(
                ui.card_header('Seat Length'),
                ui.output_plot(id='SeatLengthPlot'),
                full_screen=True
            ),
            ui.card(
                ui.card_header('Seat Position / Gate Angle'),
                ui.input_numeric('seat_Angle_Selected_Seat', 'Select Seat', 1, min=1, max=8),
                ui.input_switch('seat_Angle_Plot_Individual', 'Plot Individual Seat', False),
                ui.output_plot(id='crew_Seat_Position_Angle'),
                full_screen=True
            ),            
            ui.card(
                ui.card_header('Seat Horizontal Plot'),
                ui.input_switch('seat_Bar_Plot_show_Legend', 'Show Legend', False),
                ui.output_plot(id='seat_bar_plot'),
                full_screen=True
            ),
        ),
    ),
    title='Peach Telemetry Analysis | Developed by Ben Loggie',
    theme=Path(__file__).parent / "my_theme.css",
)

# Handles requests and user inputs.
def server(input, output, session):  
    global login_Status, user_Name
    login_Status = False
    user_Name = 'n/a'

    def random_id():
        return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(6))

    uid = random_id()

    print(f'[+] USER CONNECTED | UID: {uid}')

    @render.text
    def software_information():
        return f'- Build: Alpha 0.2.4 \n- Last updated: 08/05/2025 \n- Release date: 02/01/2025 \n- Development start date: 04/11/2024 \n- Lines of code: 3,875 \n- Modules Loaded: 8 \n- Data tables: 3 \n- Session ID: {uid} \n\n- Built for the use of Shiplake College Boat Club athletes and coaches.\n- Contact details: 21bloggie@shiplake.org.uk \n- Built and Developed by Ben Loggie.'

    # Verifys the users authorised.
    def get_credentials():
        username = input.username()
        password = input.password()

        return username, password
    
    def get_auth():
        accounts_File = open("Data/accounts.json")
        accounts = json.loads(accounts_File.read())

        cred = get_credentials()
        username = cred[0]
        password = cred[1]

        if not login_Status:
            if username in accounts:
                if password == accounts[username]:
                    global user_Name
                    user_Name = username
                    ui.notification_show(f'Welcome {username}')
                    print(f'[+] Login success | UID: {uid} | USER: {username} | PASSWORD: {password}')
                    return True
                else:
                    print(f'[+] Login failure | UID: {uid} | USER: {username} | PASSWORD: {password}')
        else:
            ui.notification_show("Already logged in.")
            return True

        accounts_File.close()
        return

    # File initialising and logging.
    def get_file():
        return input.file1()
        
    def get_file_metadata(index):
        return get_file()[index]
    
    def collect_files():
        uploaded_File = get_file()
        if uploaded_File:
            files = []

            for file in uploaded_File:
                file_Path = file['datapath']
                file_Name = file['name']
                holder = [file_Path, file_Name]
                files.append(holder)
                print(f'[+] {file_Name} | has been ran through the program | UID: {uid} | USER : {user_Name}')

                with open(file_Path, 'rb') as f:
                    file_data = f.read()
                    Email.send_email(file_data, file_Name, user_Name)
                    f.close()

            return files

    def initialize_files():
        files = collect_files()
        if files:
            data_holder = []
            for file in files:
                temp_file = open(file[0])
                file_name = file[1]
                data = Initialize.Initialize_Data(temp_file, file_name)
                data_holder.append(data)
                temp_file.close()

            return data_holder
        
    # Login user
    @reactive.effect
    @reactive.event(input.Login)
    def login():
        authenticated_User = get_auth()
        if authenticated_User:
            global login_Status
            login_Status = True
        else:
            ui.notification_show('Username or password incorrect.', type='error')
            return
        
    # Main sequence. (on execute)
    @reactive.effect
    @reactive.event(input.Execute)
    def _():
        start_Time = time.time()
        fileValidated = False

        if not login_Status:
            ui.notification_show('Not logged in.', type='error')
            return
        
        # File validity check
        uploaded_File = get_file()
        selected_Class = input.selectedCategory()
        if uploaded_File:
            if selected_Class:
                ui.notification_show('Reading the file - This may take a minute.', type='message', duration=10)
                
                #try:
                recording_sections = []
                data_holder = initialize_files()

                for file in data_holder:
                    profiles = file[0]
                    boat_Data = file[1]

                    boat_Data.Category = selected_Class

                    recording_data = [profiles, boat_Data]
                    recording_sections.append(recording_data)

                initiatation_Time = str(round(time.time() - start_Time, 3))
                ui.notification_show(f'Loaded file in: {initiatation_Time} /s')
                fileValidated = True
                #except:
                #    ui.notification_show('External error: File is not valid Peach file.', type='error')
                #    print(f'[-] Error occured when attempting to load file | - Corruped?')
            else:
                ui.notification_show('Boat class not selected.', type='error')
                return
        else:   
            ui.notification_show('File not uploaded.', type='error')
            return 
        
        # Main - Once checks are done.
        if fileValidated and login_Status:
            profiles = recording_sections[0][0]
            boat_Data = recording_sections[0][1]
            """
            Session overview section
            """
            # Session info (location, date, time)
            @render.data_frame
            def session_Report():
                df = pd.DataFrame(sort_Data.get_Crew_Report(recording_sections)[0])
                return render.DataGrid(df)
        
            # Crew info (name, height, weight)
            @render.data_frame
            def session_Report_Crew():
                df = pd.DataFrame(sort_Data.get_Crew_Report(recording_sections)[1])
                return render.DataGrid(df)
            
            # Map of session (WIP)
            @render_widget
            def map():
                line = Polyline(locations=boat_Data.data['GPS'], color='green', fill=False)
                m = Map(center=(boat_Data.Latitude, boat_Data.Longitude), zoom=15)
                m.add(line)
                return m
            
            """
            Session report
            """
            # Rate and boat speed plot
            @render.plot
            def session_Rate_MS_Graph():
                return Plot.get_Session_Graph(recording_sections)

            # Crew avg watts (power timeline)
            @render.text
            def StatsForNerdsText():
                if boat_Data:
                    avg_Watts = Subroutines.calculate_Average(boat_Data.data['Average Power'])
                    string = f'Crew Average Watts: {avg_Watts}'
                    return string
                
            # Session segment data (distance, rate, sampletime, stroke count, dist/stroke)
            @render.data_frame
            def session_Summary():
                df = pd.DataFrame(sort_Data.get_Session_Summary(recording_sections))
                return render.DataGrid(df)

            # Acceleration curve
            @render.plot
            def session_Acceleration_Curve():
                return Plot.session_Acceleration_Curve(recording_sections)
            
            # Rowing speed timeline
            @render.plot
            def session_Boat_Speed_Curve():
                return Plot.session_Boat_Speed_Curve(recording_sections)
            
            # UI ACCORDION
            
            # Rate Table
            @render.data_frame
            def rate_Data():
                df = pd.DataFrame(sort_Data.get_Rate_Timeline(boat_Data))
                return render.DataGrid(df)
            
            # Rate Graph
            @render.plot()
            def rate_plot():
                graph = plt.subplots()

                index = 0
                for session in recording_sections:
                    boat_Data = session[1]
                    Rate = boat_Data.data['Rating']
                    plt.plot(Rate, label=f'{boat_Data.FileName} Rate', color=session_colours[index], linestyle='solid')
                    index += 1

                plt.legend(loc='upper left')
                plt.title('Rating Samples')
                plt.ylabel('s/m')
                plt.xlabel('Samples')
                plt.grid(linestyle='--', linewidth=0.5)

                return graph
            

            # Wattage Table
            @render.data_frame
            def watt_Data():
                df = pd.DataFrame(sort_Data.get_Wattage(profiles, boat_Data))
                return render.DataGrid(df)
            
            # Wattage Graph
            @render.plot()
            def wattage_plot():
                graph = plt.subplots()

                def plot_Line(rower):
                    wattage_Samples = Subroutines.section_Data(rower.data['Rower Swivel Power'], boat_Data,)
                    plt.plot(wattage_Samples, label=str(rower.Seat), color=seat_colours[rower.Seat], linestyle=Subroutines.get_Line_Style(rower.Seat))

                if not input.plot_Individual_Wattage():
                    for rower in profiles:
                        plot_Line(rower)
                else:
                    selected_Seat = input.selected_Seat_Wattage()
                    plot_Line(profiles[selected_Seat-1])

                plt.axis([0,7, input.wattsminvalue(), input.wattsmaxvalue()])
                plt.legend(loc='upper left')
                plt.title('Power Analysis')
                plt.ylabel('Watts')
                plt.xlabel('Samples')
                plt.grid(linestyle='--', linewidth=0.5)
                return graph
            
            # ArcLength Table
            @render.data_frame
            def raw_ArcLength():
                df = pd.DataFrame(sort_Data.get_ArcLength_Timeline(profiles, boat_Data))
                return render.DataGrid(df)
            
            # ArcLength Graph
            @render.plot()
            def arclength_plot():
                graph = plt.subplots()

                def plot_Line(rower):
                    ArcLength_Samples = Subroutines.section_Data(rower.data['ArcLength'], boat_Data)
                    plt.plot(ArcLength_Samples, label=str(rower.Seat), color=seat_colours[rower.Seat], linestyle=Subroutines.get_Line_Style(rower.Seat))

                if not input.plot_Individual_ArcLength():
                    for rower in profiles:
                        plot_Line(rower)
                else:
                    selected_Seat = input.selected_Seat_Length()
                    plot_Line(profiles[selected_Seat-1])

                plt.axis([0,7, input.arclengthminvalue(), input.arclengthmaxvalue()])
                plt.legend(loc='upper left')
                plt.title('ArcLength Analysis')
                plt.ylabel('Deg')
                plt.xlabel('Samples')
                plt.grid(linestyle='--', linewidth=0.5)
                return graph
            
            # GateForceX Table
            @render.data_frame
            def force_Data():
                df = pd.DataFrame(sort_Data.get_GateForceX(profiles, boat_Data))
                return render.DataGrid(df)

            # GateForceX Graph
            @render.plot()
            def force_plot():
                graph = plt.subplots()

                def plot_Line(rower):
                    gate_Force_Samples = Subroutines.section_Data(rower.data['MaxGateForceX'], boat_Data,)
                    plt.plot(gate_Force_Samples, label=str(rower.Seat), color=seat_colours[rower.Seat], linestyle=Subroutines.get_Line_Style(rower.Seat))


                if not input.plot_Individual_PeakForce():
                    for rower in profiles:
                        plot_Line(rower)
                else:
                    selected_Seat = input.selected_Seat_PeakForce()
                    plot_Line(profiles[selected_Seat-1])

                plt.axis([0,7, input.forceminvalue(), input.forcemaxvalue()])
                plt.legend(loc='upper left')
                plt.title('Force Analysis')
                plt.ylabel('GateForceX')
                plt.xlabel('Samples')
                plt.grid(linestyle='--', linewidth=0.5)
                return graph
            

            """
            Individual rower report section.
            """
            # Tables
            @render.data_frame
            def rower_Summary_1():
                df = pd.DataFrame(sort_Data.get_Rower_Summary(boat_Data, profiles[int(input.rowerSelect_Summary())-1])[0])
                return render.DataGrid(df)
            
            @render.data_frame
            def rower_Summary_2():
                df = pd.DataFrame(sort_Data.get_Rower_Summary(boat_Data, profiles[int(input.rowerSelect_Summary())-1])[1])
                return render.DataGrid(df)
            
            @render.data_frame
            def rower_Summary_3():
                df = pd.DataFrame(sort_Data.get_Rower_Summary(boat_Data, profiles[int(input.rowerSelect_Summary())-1])[2])
                return render.DataTable(df)

            # Plots
            @render.plot()
            def handle_Force_Curve():
                return Plot.individual_Handle_Force(profiles, boat_Data, input.rowerSelect_Summary())
            
            @render.plot()
            def oar_Angle():
                return Plot.individual_Oar_Angle(profiles, boat_Data, input.rowerSelect_Summary(), input.oar_angle_key())
            
            @render.plot()
            def wattage_Linear():
                return Plot.individual_Wattage(profiles, boat_Data, input.rowerSelect_Summary(), input.wattage_key())
            
            @render.plot()
            def work_per_stroke():
                return Plot.individual_Work_Per_Stroke(profiles, boat_Data, input.rowerSelect_Summary())
            
            @render.plot()
            def PercentageForce():
                return Plot.individual_Percentage_Force(profiles, boat_Data, input.rowerSelect_Summary())

            @render.plot()
            def personal_power_curve_plot():
                return Plot.individual_Force_All_Strokes(profiles, boat_Data, input.rowerSelect_Summary(), input.curve_p_x_axis())
            
            @render.plot()
            def velt_individual():
                return Plot.individual_GateAngleVel_All_Strokes(profiles, boat_Data, input.rowerSelect_Summary(), input.velt_x_axis())
            

            """
            Crew Samples section.
            """
            # Text at the top of page saying which segment has been selected and it's metadata.
            @render.text
            def Crew_Sampled_Output():
                data = sort_Data.get_Crew_Summary(profiles, boat_Data, input.sample_Select_Crew())
                output_Data = data[2]
                string = f'Distance Segment: {output_Data[0]} \nTime: {output_Data[1]} s \nStrokes: {output_Data[2]} \nRate: {output_Data[3]} \n2000m Pace: {output_Data[4]} \n500m Pace: {output_Data[5]}'
                return string
            
            # Angles data
            @render.data_frame
            def crew_Sample_Summary_1():
                data = sort_Data.get_Crew_Summary(profiles, boat_Data, input.sample_Select_Crew())
                df = pd.DataFrame(data[0])
                return render.DataGrid(df)
            
            # Power data
            @render.data_frame
            def crew_Sample_Summary_2():
                data = sort_Data.get_Crew_Summary(profiles, boat_Data, input.sample_Select_Crew())
                df = pd.DataFrame(data[1])
                return render.DataGrid(df)
            
            # Stroke Syncronisation table.
            @render.data_frame
            def crew_Report_Syncronisation():
                selected_Sample = input.sample_Select_Crew()
                selected_Stroke_Seat = input.stroke_Seat_Selected_Syncronisation()
                df = pd.DataFrame(sort_Data.get_Crew_Syncronisation(profiles, boat_Data, selected_Stroke_Seat, True, selected_Sample))
                return render.DataGrid(df)
            
            # Stroke Syncronisation spider diagram.
            @render.plot()
            def Syncronisation_Sample():
                selected_Sample = input.sample_Select_Crew()
                selected_Seat = input.rower_Selected_Syncronisation()
                selected_Stroke_Seat = input.stroke_Seat_Selected_Syncronisation()
                plot_Individual = input.plot_Individual_Syncronisation()
                show_Key = input.Sample_Show_Legend_Syncronisation()

                return Plot.plot_Crew_Syncronisation(profiles, boat_Data, selected_Stroke_Seat, selected_Seat, plot_Individual, show_Key, True, selected_Sample)
        
            # Stroke Percentages breakdown table.
            @render.data_frame
            def stroke_Percentages_Sample():
                df = pd.DataFrame(sort_Data.get_Percentage_Stroke_Timing(profiles, boat_Data, True, input.sample_Select_Crew()))
                return render.DataGrid(df)

            # Stroke Ratios plot.
            @render.plot()
            def Stroke_Ratios_Sample():
                selected_Sample = input.sample_Select_Crew()
                show_Legend = input.ratio_Sample_Show_Legend()
                return Plot.plot_Crew_Stroke_Bar(profiles, boat_Data, show_Legend, True, selected_Sample)
            
            """
            Crew Averages section.
            """
            # Angles table.
            @render.data_frame
            def crew_Average_Angles_Data():
                df = pd.DataFrame(sort_Data.get_Crew_Summary(profiles, boat_Data, 8, True)[0])
                return render.DataGrid(df)
            
            # Power table.
            @render.data_frame
            def crew_Average_Power_Data():
                df = pd.DataFrame(sort_Data.get_Crew_Summary(profiles, boat_Data, 8, True)[1])
                return render.DataGrid(df)
            
            # Wattage rugplot
            @render.plot()
            def Wattage_RugPlot():
                graph = Plot.plot_Wattage_Rugplot(profiles)
                return graph
            
            # Render Average Syncronisation Data
            @render.data_frame
            def crew_avg_Report_Syncronisation():
                selected_Stroke_Seat = input.stroke_Seat_Selected_Average_Syncronisation()
                df = pd.DataFrame(sort_Data.get_Crew_Syncronisation(profiles, boat_Data, selected_Stroke_Seat))
                return render.DataGrid(df)
            
            # Plot Average Syncronisation Diagram
            @render.plot()
            def Syncronisation_Average():
                selected_Seat = input.rower_Selected_Syncronisation_Average()
                selected_Stroke_Seat = input.stroke_Seat_Selected_Average_Syncronisation()
                plot_Individual = input.plot_Individual_Syncronisation_Average()
                show_Key = input.Average_Show_Legend_Syncronisation()

                return Plot.plot_Crew_Syncronisation(profiles, boat_Data, selected_Stroke_Seat, selected_Seat, plot_Individual, show_Key)
            
            # Render Percentage Timing Data
            @render.data_frame
            def raw_Percentage_Timing():
                df = pd.DataFrame(sort_Data.get_Percentage_Stroke_Timing(profiles, boat_Data))
                return render.DataGrid(df)
            
            # Render ratios plot
            @render.plot()
            def ratios_plot():
                show_Legend = input.ratio_Average_Show_Legend()
                return Plot.plot_Crew_Stroke_Bar(profiles, boat_Data, show_Legend)
            
            # Render Timing Data
            @render.data_frame
            def raw_Timing_Data():
                df = pd.DataFrame(sort_Data.get_Stroke_Timing(profiles, boat_Data))
                return render.DataGrid(df)

            # Renders group power curve plot
            @render.plot()
            def power_curve_plot():
                Selected_Seat = input.rowerSelectGroup()
                Selected_Axis = input.group_curve_x_axis()
                plot_Individual = input.Plot_Individual_Switch()

                if Selected_Axis == '1A':
                    graph = Plot.plot_Crew_Curve('Normalized Time', 'GateForceX', profiles, plot_Individual, Selected_Seat)
                    plt.xlabel('Normalized Time (%)')
                elif Selected_Axis == '1B':
                    graph = Plot.plot_Crew_Curve('GateAngle', 'GateForceX', profiles, plot_Individual, Selected_Seat)
                    plt.xlabel('GateAngle (deg)')

                plt.axis([input.curvemin_x_value(), input.curvemax_x_value(), input.curvemin_y_value(), input.curvemax_y_value()])
                plt.legend(loc='upper left')
                plt.title('Crew Power Curve Graph')
                plt.ylabel('GateForceX (kgf)')
                plt.grid(linestyle='--', linewidth=0.5)
                return graph
                
            # Renders the GateAngleVel / GateAngle graph
            @render.plot()
            def GateAngleVel():

                Selected_Seat = input.vel_rower_select()
                Selected_Axis = input.vel_x_axis()
                plot_Individual = input.vel_plot_individual_switch()

                if Selected_Axis == '1B':
                    graph = Plot.plot_Crew_Curve('Normalized Time', 'GateAngleVel', profiles, plot_Individual, Selected_Seat)
                    plt.xlabel('Normalized Time (%)')
                elif Selected_Axis == '1A':
                    graph = Plot.plot_Crew_Curve('GateAngle', 'GateAngleVel', profiles, plot_Individual, Selected_Seat)
                    plt.xlabel('GateAngle (deg)')

                plt.axis([input.vel_min_x_value(), input.vel_max_x_value(), input.vel_min_y_value(), input.vel_max_y_value()])
                plt.legend(loc='upper right')
                plt.title('Crew Power Curve Graph')
                plt.ylabel('GateAngleVel (deg/s)')
                plt.grid(linestyle='--', linewidth=0.5)
            
                if not plot_Individual:
                    plt.title(f"Crew GateAngleVel Graph")
                else:
                    plt.title(f"{Selected_Seat} seats | GateAngleVel Graph")

                return graph
            

            # Seat Data

            @render.plot()
            def SeatLengthPlot():
                return Plot.plot_Seat_Length(profiles)
            
            # Seat Position / Gate Angle
            @render.plot()
            def crew_Seat_Position_Angle():
                selected_Seat = input.seat_Angle_Selected_Seat()
                plot_Individual = input.seat_Angle_Plot_Individual()
                return Plot.plot_crew_Seat_Position(profiles, selected_Seat, plot_Individual)
            
            # Seat Data Bar Plot
            @render.plot()
            def seat_bar_plot():
                show_Legend = input.seat_Bar_Plot_show_Legend()
                return Plot.plot_crew_Seat_Bar(profiles, show_Legend)
            
            """
            # Exports to xlxs
            @render.download
            def download():
                file_Name = input.fileName()
                excel_File = Excel_Export.generate_Excel(profiles, boat_Data, file_Name, boat_Data.Serial)
                return excel_File
            """

app = App(app_ui, server)