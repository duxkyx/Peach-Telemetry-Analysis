from Modules import Subroutines, Gold_Target, sort_Data
import Modules.Variables as Variables
from random import randint
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sb

# Subroutines import
section_List = Subroutines.section_List
get_Line_Colour = Subroutines.get_Line_Colour
get_Line_Style = Subroutines.get_Line_Style

average_Array_into_Sections = Subroutines.average_Array_into_Sections
average_Array_into_One = Subroutines.average_Array_into_One
find_Seat = Subroutines.find_seat_Position_In_Array

# Variable import
seat_colours = Variables.seat_colours
sample_colours = Variables.sample_colours
markers = Variables.markers
bar_colours = Variables.bar_colours
seat_bar_colours = Variables.seat_bar_colours
session_colours = Variables.session_colours
seat_effective_colours = Variables.seat_effective_colours

# Creates a graph of 8 averaged lines per 1/8th of data in the array.
def plot_Sample_Curve(x, y, boat_Data):
    sectioned_x = section_List(x, boat_Data)
    sectioned_y = section_List(y, boat_Data)
    avg_sections_x = average_Array_into_Sections(sectioned_x)
    avg_sections_y = average_Array_into_Sections(sectioned_y)

    graph, ax = plt.subplots()

    increment = 0
    for array in avg_sections_x:
        colour = ''
        try:
            colour = sample_colours[str(increment+1)]
        except:
            colour = '#%02x%02x%02x' % (randint(0,255), randint(0,255), randint(0,255))
        ax.plot(array, avg_sections_y[increment], label='Sample: 0'+str(increment+1), color=colour or hex(randint(0,255)), linestyle='solid', linewidth=2)

        increment += 1

    return graph

# Plots the average curve for each rower into one grid from their own full arrays.
def plot_Crew_Curve(x, y, profiles, individual, Selected_Seat):
    graph, ax = plt.subplots()

    def plot(rower):
        avg_sections_x = average_Array_into_One(rower.data[x])
        avg_sections_y = average_Array_into_One(rower.data[y])
        ax.plot(avg_sections_x, avg_sections_y, label=str(rower.Seat), color=get_Line_Colour(rower.Seat), linestyle=get_Line_Style(rower.Seat), linewidth=0.5)

    if individual:
        plot(profiles[int(Selected_Seat)-1])
    else:
        for rower in profiles:
            plot(rower)

    return graph

# Plots the session progression plot (M/S, Rate, Avg Watts)
def get_Session_Graph(recording_sections):
    graph, axis1 = plt.subplots()

    plt.grid(linestyle='--', linewidth=0.5)

    axis2 = axis1.twinx()

    handles = []

    axis1.set(ylim=(10,60), xlabel='Strokes', ylabel='Stroke Rate (str/min)')
    axis2.set(ylim=(2,7), ylabel='Rowing Speed (m/s)')

    count = 0
    for session in recording_sections:
        boat_Data = session[1] # Session [boat_Data]

        strokes = []
        meters_per_second = boat_Data.data['Meters/s']
        stroke_rate = boat_Data.data['Rating']
        #avg_Watts = boat_Data.data['Average Power']

        counter = 0
        for _ in stroke_rate:
            strokes.append(counter)
            counter += 1

        p1, = axis1.plot(strokes, stroke_rate, c=session_colours[count], label=f'{boat_Data.FileName} Rate (str/min)')
        p2, = axis2.plot(strokes, meters_per_second, c=session_colours[count], label=f'{boat_Data.FileName} Rowing Speed (m/s)')

        """p3, = axis3.plot(strokes, avg_Watts, label='Avg Boat Power (w)', c='g')
        axis3.set(xlim=(None,None), ylabel='Power (w)')
        plt.ylim(100, 350)"""

        handles.append(p1)
        handles.append(p2)

        count += 1

    axis1.legend(handles=handles, loc='upper left')
        
    return graph

# Boat Acceleration
def session_Acceleration_Curve(recording_sections):
    graph, axis = plt.subplots()

    count = 0
    for session in recording_sections:
        boat_Data = session[1]

        Acceleration = boat_Data.data['Acceleration']
        Noralized_Time = boat_Data.data['Normalized Time']
        
        Acceleration_Average = average_Array_into_One(Acceleration)
        Normalized_Time_Average = average_Array_into_One(Noralized_Time)

        axis.plot(Normalized_Time_Average, Acceleration_Average, c=session_colours[count], label=f'{boat_Data.FileName} Acceleration')
        count += 1
    
    plt.axis([None, None, -10, 10])
    plt.legend(loc='lower left')
    plt.title('Boat Acceleration (m/s^2)')
    plt.ylabel('m/s^2')
    plt.xlabel('Normalized Time %')
    plt.grid(linestyle='--', linewidth=0.5)

    return graph

# Rowing Speed
def session_Boat_Speed_Curve(recording_sections):
    graph, ax = plt.subplots()

    index = 0
    for session in recording_sections:
        boat_Data = session[1]
        #meters_s = Subroutines.section_Data(boat_Data.data['Meters/s'], boat_Data, 8)
        ms = boat_Data.data['Meters/s']
        plt.plot(ms, label=f'{boat_Data.FileName} Rowing Speed m/s', color=session_colours[index], linestyle='solid')
        index += 1

    ax.axhline(y=6.25, label='Gold Target', color='#800000', linestyle='--')

    plt.axis([None, None, 2.5, 8])
    plt.legend(loc='lower left')
    plt.title('Rowing Speed (m/s)')
    plt.ylabel('m/s')
    plt.xlabel('Samples')
    plt.grid(linestyle='--', linewidth=0.5)
    return graph
            
# Plots 8 sampled force curves for each selected seat.
def individual_Handle_Force(profiles, boat_Data, selected_Rower):
    GateForceX = profiles[find_Seat(selected_Rower, profiles)].data['GateForceX']
    Gate_Angles = profiles[find_Seat(selected_Rower, profiles)].data['GateAngle']
    graph = plot_Sample_Curve(Gate_Angles, GateForceX, boat_Data)
    plt.axis([None, None, None, None])
    plt.legend(loc='upper left')
    plt.title('Gate Force')
    plt.ylabel('Kg')
    plt.xlabel('Gate Angle (Deg)')
    plt.grid(linestyle='--', linewidth=0.5)
    return graph

# Plots the oar angle through the 8 segments
def individual_Oar_Angle(profiles, boat_Data, selected_Rower, show_Key=False):
    graph, ax = plt.subplots()
    def plot_Line(rower):
        ArcLength_Samples = Subroutines.section_Data(rower.data['ArcLength'], boat_Data)
        MinAngle_Samples = Subroutines.section_Data(rower.data['MinAngle'], boat_Data)
        MaxAngle_Samples = Subroutines.section_Data(rower.data['MaxAngle'], boat_Data)

        abs_MinAngles = []
        for angle in MinAngle_Samples:
            abs_MinAngles.append(abs(angle))

        plt.plot(ArcLength_Samples, label='Arc Length', color='#4169e1', linestyle='solid', marker='.')
        plt.plot(abs_MinAngles, label='Catch Angle [Positive]', color='#6495ed', linestyle='solid', marker='.')
        plt.plot(MaxAngle_Samples, label='Finish Angle', color='#b0c4de', linestyle='solid', marker='.')

    plot_Line(profiles[find_Seat(selected_Rower, profiles)])
    ax.axhline(y=Gold_Target.get_Target(boat_Data.Category)['Arc Length'], label='Gold Target', color='#800000', linestyle='--')
    ax.axhline(y=abs(Gold_Target.get_Target(boat_Data.Category)['Catch Angle']), color='#800000', linestyle='--')
    ax.axhline(y=Gold_Target.get_Target(boat_Data.Category)['Finish Angle'], color='#800000', linestyle='--')

    plt.axis([None, None, 20, 100])
    if show_Key:
        plt.legend(loc='center left')
    plt.title('Arc Length (deg)')
    plt.ylabel('Deg')
    plt.xlabel('Samples')
    plt.grid(linestyle='--', linewidth=0.5)
    return graph

# Plots the Wattage timeline for individual rowers
def individual_Wattage(profiles, boat_Data, selected_Rower, show_Key=False):
    graph, ax = plt.subplots()
    def plot_Line(rower):
        Wattage_Samples = Subroutines.section_Data(rower.data['Rower Swivel Power'], boat_Data)
        Wattage_Sections = Subroutines.section_List(rower.data['Rower Swivel Power'], boat_Data)

        MaxRowingPower_Array = []
        for section in Wattage_Sections:
            MaxRowingPower_Array.append(max(section))
        
        MinRowingPower_Array = []
        for section in Wattage_Sections:
            MinRowingPower_Array.append(min(section))

        plt.plot(MaxRowingPower_Array, label='Max Power', color='#4169e1', linestyle='solid', marker='.')
        plt.plot(Wattage_Samples, label='Average Power', color='#6495ed', linestyle='solid', marker='.')
        plt.plot(MinRowingPower_Array, label='Min Power', color='#b0c4de', linestyle='solid', marker='.')


    plot_Line(profiles[find_Seat(selected_Rower, profiles)])
    ax.axhline(y=Gold_Target.get_Target(boat_Data.Category)['Power'], label='2KM Power - Gold Target', color='#800000', linestyle='--')

    plt.axis([None, None, 100, 500])
    if show_Key:
        plt.legend(loc='upper left')
    plt.title('Power (w)')
    plt.ylabel('watts')
    plt.xlabel('Samples')
    plt.grid(linestyle='--', linewidth=0.5)
    return graph

# Plots the work per stroke timeline for individual rowers
def individual_Work_Per_Stroke(profiles, boat_Data, selected_Rower):
    graph, ax = plt.subplots()
    seat_Data = profiles[find_Seat(selected_Rower, profiles)].data
    work_per_stroke = seat_Data['Work Per Stroke']
    sectioned_WPS = Subroutines.section_Data(work_per_stroke, boat_Data)

    ax.plot(sectioned_WPS, color='#800000', marker='.')

    plt.title('Work Per Stroke (Including water resistance)')
    plt.ylabel('Work Done (J)')
    plt.xlabel('Samples')
    plt.grid(linestyle='--', linewidth=0.5)

    return graph

# Plots the individual curve for % stroketime and % force
def individual_Percentage_Force(profiles, boat_Data, selected_Rower):
    graph, ax = plt.subplots()
    seat_Data = profiles[find_Seat(selected_Rower, profiles)].data
    percentageForceList = Subroutines.average_Array_into_One(seat_Data['PercentageForce'])
    percentageAngleList = Subroutines.average_Array_into_One(seat_Data['PercentageAngle'])
    percentage70MaxF = Subroutines.calculate_Average(seat_Data['Percentage70%MaxForce'])

    positionCSlip = Subroutines.calculate_Average(seat_Data['Position_Of_CSlip'])
    position70MaxF = Subroutines.calculate_Average(seat_Data['Position_Of_70MaxF'])
    positionMaxF = Subroutines.calculate_Average(seat_Data['Position_Of_MaxF'])
    positionFrom70MaxF = Subroutines.calculate_Average(seat_Data['Position_Of_From70MaxF'])
    positionFSlip = Subroutines.calculate_Average(seat_Data['Posititon_Of_FSlip'])

    all_Rowers_Percentage_Force = []
    all_Rowers_Percentage_GateAngle = []
    for rower in profiles:
        rower_Avg_ForcePercentage = Subroutines.average_Array_into_One(rower.data['PercentageForce'])
        rower_Avg_GatePercentage = Subroutines.average_Array_into_One(rower.data['PercentageAngle'])
        all_Rowers_Percentage_Force.append(rower_Avg_ForcePercentage)
        all_Rowers_Percentage_GateAngle.append(rower_Avg_GatePercentage)

    crew_Avg_PercentageForce = Subroutines.average_Array_into_One(all_Rowers_Percentage_Force)
    crew_Avg_Percentage_Angle = Subroutines.average_Array_into_One(all_Rowers_Percentage_GateAngle)

    ax.plot(percentageAngleList, percentageForceList, label='Actual Data', color='#800000', marker='.')
    ax.plot(crew_Avg_Percentage_Angle, crew_Avg_PercentageForce, label='Crew Avg', color='#b0c4de')
    
    ax.hlines(y=percentage70MaxF, xmin=min(crew_Avg_Percentage_Angle), xmax=max(crew_Avg_Percentage_Angle), label='70% Max', linestyles='--', colors='#bac3c2')
    ax.annotate(text='70% Max', xy=(10, percentage70MaxF), xytext=(10, percentage70MaxF))
    
    ax.vlines(x=positionCSlip, ymin=0, ymax=100, linestyles='--', colors='#bac3c2')
    ax.annotate(text='Catch Slip', xy=(positionCSlip, 10), xytext=(positionCSlip, 10))

    ax.vlines(x=position70MaxF, ymin=0, ymax=100, linestyles='--', colors='#bac3c2')
    ax.annotate(text='Upto 70Max F', xy=(position70MaxF, 10), xytext=(position70MaxF, 10))

    ax.vlines(x=positionMaxF, ymin=0, ymax=100, linestyles='--', colors='#bac3c2')
    ax.annotate(text='Max F', xy=(positionMaxF, 10), xytext=(positionMaxF, 10))

    ax.vlines(x=positionFrom70MaxF, ymin=0, ymax=100, linestyles='--', colors='#bac3c2')
    ax.annotate(text='From 70% Max F', xy=(positionFrom70MaxF, 10), xytext=(positionFrom70MaxF, 10))

    ax.vlines(x=positionFSlip, ymin=0, ymax=100, linestyles='--', colors='#bac3c2')
    ax.annotate(text='Finish Slip', xy=(positionFSlip, 10), xytext=(positionFSlip, 10))


    plt.axis([0,100, 0, 100])
    plt.legend(loc='upper right')
    plt.title('Handle Force (% of max)')
    plt.xlabel('Drive Time (%)')
    plt.grid(linestyle='--', linewidth=0.5)

    return graph

# Plots GateForce X all the strokes for an individual rower.
def individual_Force_All_Strokes(profiles, boat_Data, selected_Rower, axis):
    graph, ax = plt.subplots()
    seat_Data = profiles[find_Seat(selected_Rower, profiles)].data

    GateForceX = seat_Data['GateForceX']
    Max_GateForceX = seat_Data['MaxGateForceX']
    Normalized_Time = seat_Data['Normalized Time']
    GateAngles = seat_Data['GateAngle']
    AngleMaxF = seat_Data['Angle_MaxGateForceX']

    index = 0
    for force_List in GateForceX:
        if axis == '1A':
            ax.plot(Normalized_Time[index], force_List, color='#0000f7', linewidth=0.1)
            plt.xlabel('Normalized Time (%)')
        elif axis == '1B':
            ax.plot(GateAngles[index], force_List, color='#0000f7', linewidth=0.1)
            plt.xlabel('GateAngle (deg)')
        index += 1

    plt.ylabel('GateForceX (kgf)')
    plt.grid(linestyle='--', linewidth=0.5)

    return graph

# Plots GateAngleVelocity all strokes for an indiviual rower.
def individual_GateAngleVel_All_Strokes(profiles, boat_Data, selected_Rower, axis):
    graph, ax = plt.subplots()

    seat_Data = profiles[find_Seat(selected_Rower, profiles)].data

    Normalized_Time = seat_Data['Normalized Time']
    GateAngles = seat_Data['GateAngle']
    GateAngleVel = seat_Data['GateAngleVel']

    index = 0
    for angleVelocity_List in GateAngleVel:
        if axis == '1B':
            ax.plot(Normalized_Time[index], angleVelocity_List, color='#0000f7', linewidth=0.1)
            plt.xlabel('Normalized Time (%)')
        elif axis == '1A':
            ax.plot(GateAngles[index], angleVelocity_List, color='#0000f7', linewidth=0.1)
            plt.xlabel('GateAngle (deg)')
        index += 1

    plt.ylabel('GateAngelVel (deg/s)')
    plt.grid(linestyle='--', linewidth=0.5)

    return graph

# Crew Syncronisation Spider Diagram
def plot_Crew_Syncronisation(profiles, boat_Data, selected_Stroke_Seat, selected_Seat, plot_Individual, show_Key, sample=False, selected_Sample=1):
    circle = np.linspace(0, 2*np.pi, 14, endpoint=False).tolist()
    closed_circle = circle.copy()
    closed_circle.append(0.0)
    graph = plt.subplot(polar=True)

    graph.set_theta_offset(np.pi / 2)
    graph.set_theta_direction(-1)

    attributes = ['25% Recov', '50% Recov', '75% Recov', 'Hang Start', 'Min Angle', 'Hang End', 'Effective Start', 'Upto 70% Max F', 'Max F', 'From 70% Max F', 'Effective End', 'Pause Start', 'Max Angle', 'Release']
    plt.xticks(ticks=circle, labels=attributes)
    plt.yticks(ticks=[-200, -150, -100, -50, 0, 50, 100], labels=['-200', '-150', '-100', '-50', '0', '50', '100'])
    plt.ylim(-200,100)

    if sample:
        data = sort_Data.get_Crew_Syncronisation(profiles, boat_Data, selected_Stroke_Seat, True, selected_Sample)
    else:
        data = sort_Data.get_Crew_Syncronisation(profiles, boat_Data, selected_Stroke_Seat)
    
    def plot(rower):
        data_Holder = []
        index = Subroutines.find_seat_Position_In_Array(rower.Seat, profiles)

        for key in data:
            if key in attributes:
                value = data[key][index]
                data_Holder.append(value)

        # This loops the data back to the origin of the radar graph.
        data_Holder.append(data['25% Recov'][index])

        graph.plot(closed_circle, data_Holder, label=str(rower.Seat), color=seat_colours[rower.Seat], linestyle=Subroutines.get_Line_Style(rower.Seat), marker=markers[rower.Seat])

    if not plot_Individual:
        for rower in profiles:
            plot(rower)
    else:
        plot(profiles[Subroutines.find_seat_Position_In_Array(str(selected_Seat), profiles)])
        plot(profiles[Subroutines.find_seat_Position_In_Array(str(selected_Stroke_Seat), profiles)])
        
    if show_Key:
        plt.legend(loc='upper left')
    return graph

# Gate Angle Bar Plot
def plot_Crew_Stroke_Bar(profiles, boat_Data, show_Legend=False, sample=False, selected_Sample=1):
    data_Array = {}

    if sample:
        array = sort_Data.get_Stroke_Timing(profiles, boat_Data, True, selected_Sample)
    else:
        array = sort_Data.get_Stroke_Timing(profiles, boat_Data)

    index_Array = []
    for rower in profiles:
        index_Array.append(f'{rower.Name} | {rower.Seat}')

    blacklist = ['Seat', 'Side', 'Total Stroke', 'Total Recov', 'Total Drive', 'Effective Drive']
    for column in array:
        if not column in blacklist:
            content_List = []
            for element in array[column]:
                content_List.append(element)

            new_Array = {column: content_List}
            data_Array.update(new_Array)

    df = pd.DataFrame(data_Array, index=index_Array)
    graph = df.plot(kind='barh', legend=show_Legend, stacked=True, xlabel='Time (s)', ylabel='Seats', color=bar_colours)
    
    if sample:
        graph.set_title(f'Ratios | Sample: {selected_Sample}/{8} | {Subroutines.get_Meters_Sample_Text(boat_Data, selected_Sample)}')
    else:
        graph.set_title('Ratios | Recording Average')

    return graph

# Seat Position / Gate Angle
def plot_crew_Seat_Position(profiles, selected_Seat, plot_Individual):
    graph, ax = plt.subplots()

    def plot_Rower(rower):
        seat_data = rower.data
        seat_Posn = seat_data['SeatPosn']
        gate_Angle = seat_data['GateAngle']
        gate_Force = seat_data['GateForceX']

        avg_Seat_Posn = Subroutines.average_Array_into_One(seat_Posn)
        avg_Gate_Angle = Subroutines.average_Array_into_One(gate_Angle)
        avg_Gate_Force = Subroutines.average_Array_into_One(gate_Force)

        effective_Drive_Posn = []
        effective_Gate_Angle = []
        recovery_Drive_Posn = []
        recovery_Gate_Angle = []

        iteration = 0
        found_Lock = False
        for force in avg_Gate_Force:
            current_Seat_Posn = avg_Seat_Posn[iteration]
            current_Gate_Angle = avg_Gate_Angle[iteration]
            if (force >= 30 and (not found_Lock) or (force >= 15 and (found_Lock))):
                found_Lock = True
                effective_Drive_Posn.append(current_Seat_Posn)
                effective_Gate_Angle.append(current_Gate_Angle)
            else:
                recovery_Drive_Posn.append(current_Seat_Posn)
                recovery_Gate_Angle.append(current_Gate_Angle)
            
            iteration += 1

        ax.scatter(recovery_Gate_Angle, recovery_Drive_Posn, color=seat_colours[rower.Seat], label=f'{str(rower.Seat)} | {rower.Name}')
        ax.scatter(effective_Gate_Angle, effective_Drive_Posn, color=seat_effective_colours[rower.Seat])

    if not plot_Individual:
        for rower in profiles:
            plot_Rower(rower)
    else:
        plot_Rower(profiles[Subroutines.find_seat_Position_In_Array(selected_Seat, profiles)])

    plt.ylabel('Seat Posn')
    plt.xlabel('Gate Angle')
    plt.grid(linestyle='--', linewidth=0.5)
    plt.legend(loc='upper left')

    return graph

# Seat Bar Plot
def plot_crew_Seat_Bar(profiles, show_Legend):
    data_Array = {}
    
    array = sort_Data.get_Seat_Timing(profiles)

    index_Array = []
    for rower in profiles:
        index_Array.append(f'{rower.Name} | {rower.Seat}')

    for column in array:
        content_List = []
        for element in array[column]:
            content_List.append(element)

        new_Array = {column: content_List}
        data_Array.update(new_Array)

    df = pd.DataFrame(data_Array, index=index_Array)

    if show_Legend:
        graph = df.plot(kind='barh', legend=True, stacked=True, xlabel='Time (s)', ylabel='Seats', color=seat_bar_colours)
    else:
        graph = df.plot(kind='barh', legend=False, stacked=True, xlabel='Time (s)', ylabel='Seats', color=seat_bar_colours)

    return graph

# Seat Length Plot
def plot_Seat_Length(profiles):
    graph, ax = plt.subplots(nrows=len(profiles), ncols=1, figsize=(1,1))

    index = 0
    for rower in profiles:
        sb.rugplot(data=rower.data['SeatLength'], ax=ax[index], height=1, color='grey')

        avg = Subroutines.calculate_Average(rower.data['SeatLength'])
        for line in ax[index].lines:
            line.set_alpha(0.2)

        ax[index].text(45-2, 0.02, f"{rower.Name} | Avg: {avg} cm", va='bottom', ha='right', fontsize=10, color='black')

        ax[index].axvline(avg, color='black', linewidth=4)
        ax[index].set_xlim(45, 65)
        ax[index].set_ylabel(f'{rower.Seat}')
        ax[index].set_yticks([])
        ax[index].set_xticks([])
        index += 1
    return graph


# Wattage rugplot
def plot_Wattage_Rugplot(profiles):
    graph, ax = plt.subplots(nrows=len(profiles), ncols=1, figsize=(1,1))

    index = 0
    for rower in profiles:
        sb.rugplot(data=rower.data['Rower Swivel Power'], ax=ax[index], height=1, color='grey')

        avg = round(Subroutines.calculate_Average(rower.data['Rower Swivel Power']),1)
        for line in ax[index].lines:
            line.set_alpha(0.2)

        ax[index].text(2, 0.02, f"{rower.Name} | Avg: {avg} watts", va='bottom', ha='right', fontsize=10, color='black')

        ax[index].axvline(avg, color='black', linewidth=4)
        ax[index].set_xlim(100, 500)
        ax[index].set_ylabel(f'{rower.Seat}')
        ax[index].set_yticks([])
        ax[index].set_xticks([])
        index += 1
    return graph