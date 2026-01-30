# This program will collect data and section it into key value pair dictionary arrays.
from Modules import Subroutines, Gold_Target
import json

def get_Seat_Timing(profiles_Data):
    data_Array = {
        'Before Seat': [],
        'Seat Recovery': [],
        'Pause 1': [],
        'Min': [],
        'Pause 2': [],
        'Drive': [],
        'Drive Finished 1': [],
        'Max': [],
        'Drive Finished 2': [],
    }

    for data_Name in data_Array:
        for rower in profiles_Data:
            Data_List = data_Array[data_Name]

            if data_Name == 'Min' or data_Name == 'Max':
                Data_List.append(0.01)
            else:
                Data_List.append(Subroutines.calculate_Average(rower.data[data_Name]))

    return data_Array

def get_Stroke_Timing(profiles_Data, boat_Data, samples=False, sample=1):
    data_Array = {
        'Seat': [],
        'Name': [],
        'Side': [],
        
        '1 Recov': [],
        '25% Recov': [],
        '2 Recov': [],
        '50% Recov': [],
        '3 Recov': [],
        '75% Recov': [],
        '4 Recov': [],
        '1 Hang': [],
        'Min': [],
        '2 Hang': [],
        'C Slip': [],
        '1 Drive': [],
        '70 Max': [],
        '2 Drive': [],
        'Max F': [],
        '3 Drive': [],
        'From 70 Max': [],
        '4 Drive': [],
        'F Slip': [],
        'Pause 1': [],
        'Max': [],
        'Pause 2': [],
        '5 Recov': [],
        'Total Stroke': [],
        'Total Recov': [],
        'Total Drive': [],
        'Effective Drive': [],
    }

    
    for data_Name in data_Array:
        for rower in profiles_Data:
            Data_List = data_Array[data_Name]

            section = Subroutines.section_Data
            def sec_Data(array):
                return section(array, boat_Data)

            if samples:
                stroke_Time = sec_Data(rower.data['Stroke Time'])[sample-1]
                recovery_Time1 = sec_Data(rower.data['Recovery Time 1'])[sample-1]
                recovery_Time2 = sec_Data(rower.data['Recovery Time 2'])[sample-1]
                recovery_Time3 = sec_Data(rower.data['Recovery Time 3'])[sample-1]
                recovery_Time4 = sec_Data(rower.data['Recovery Time 4'])[sample-1]
                hang_Time1 = sec_Data(rower.data['Hang Time 1'])[sample-1]
                hang_Time2 = sec_Data(rower.data['Hang Time 2'])[sample-1]
                c_slip_Time = sec_Data(rower.data['Catch Slip Time'])[sample-1]
                drive_Time1 = sec_Data(rower.data['Drive Time 1'])[sample-1]
                drive_Time2 = sec_Data(rower.data['Drive Time 2'])[sample-1]
                drive_Time3 = sec_Data(rower.data['Drive Time 3'])[sample-1]
                drive_Time4 = sec_Data(rower.data['Drive Time 4'])[sample-1]
                f_slip_Time = sec_Data(rower.data['Finish Slip Time'])[sample-1]
                pause_Time1 = sec_Data(rower.data['Pause Time 1'])[sample-1]
                pause_Time2 = sec_Data(rower.data['Pause Time 2'])[sample-1]
                recovery_Time5 = sec_Data(rower.data['Recovery Time 5'])[sample-1]
            else:
                stroke_Time = float(Subroutines.calculate_Average(rower.data['Stroke Time']))
                recovery_Time1 = float(Subroutines.calculate_Average(rower.data['Recovery Time 1']))
                recovery_Time2 = float(Subroutines.calculate_Average(rower.data['Recovery Time 2']))
                recovery_Time3 = float(Subroutines.calculate_Average(rower.data['Recovery Time 3']))
                recovery_Time4 = float(Subroutines.calculate_Average(rower.data['Recovery Time 4']))   
                hang_Time1 = float(Subroutines.calculate_Average(rower.data['Hang Time 1']))
                hang_Time2 = float(Subroutines.calculate_Average(rower.data['Hang Time 2']))
                c_slip_Time = float(Subroutines.calculate_Average(rower.data['Catch Slip Time']))
                drive_Time1 = float(Subroutines.calculate_Average(rower.data['Drive Time 1']))
                drive_Time2 = float(Subroutines.calculate_Average(rower.data['Drive Time 2']))
                drive_Time3 = float(Subroutines.calculate_Average(rower.data['Drive Time 3']))
                drive_Time4 = float(Subroutines.calculate_Average(rower.data['Drive Time 4']))
                f_slip_Time = float(Subroutines.calculate_Average(rower.data['Finish Slip Time']))
                pause_Time1 = float(Subroutines.calculate_Average(rower.data['Pause Time 1']))
                pause_Time2 = float(Subroutines.calculate_Average(rower.data['Pause Time 2']))
                recovery_Time5 = float(Subroutines.calculate_Average(rower.data['Recovery Time 5']))

            total_recovery_Time = recovery_Time1 + recovery_Time2 + recovery_Time3 + recovery_Time3 + recovery_Time4 + recovery_Time5 + hang_Time1
            effective_Drive_Time = drive_Time1 + drive_Time2 + drive_Time3
            total_Drive = effective_Drive_Time + c_slip_Time + f_slip_Time + hang_Time2

            if data_Name == 'Seat':
                Data_List.append(rower.Seat)
            elif data_Name == 'Name':
                Data_List.append(rower.Name)
            elif data_Name == 'Side':
                Data_List.append(rower.Side)
            elif data_Name == 'Stroke':
                Data_List.append(stroke_Time)
            elif data_Name == '1 Recov':
                Data_List.append(recovery_Time1)
            elif data_Name == '25% Recov':
                Data_List.append(0.01)
            elif data_Name == '2 Recov': 
                Data_List.append(recovery_Time2)
            elif data_Name == '50% Recov':
                Data_List.append(0.01)
            elif data_Name == '3 Recov': 
                Data_List.append(recovery_Time3)
            elif data_Name == '75% Recov':
                Data_List.append(0.01)
            elif data_Name == '4 Recov': 
                Data_List.append(recovery_Time4)
            elif data_Name == '1 Hang':
                Data_List.append(hang_Time1)
            elif data_Name == 'Min':
                Data_List.append(0.01)
            elif data_Name == '2 Hang': 
                Data_List.append(hang_Time2)
            elif data_Name == 'C Slip':
                Data_List.append(c_slip_Time)
            elif data_Name == '1 Drive':
                Data_List.append(drive_Time1)
            elif data_Name == '70 Max':
                Data_List.append(0.01)
            elif data_Name == '2 Drive':
                Data_List.append(drive_Time2)
            elif data_Name == 'Max F':
                Data_List.append(0.01)
            elif data_Name == '3 Drive':
                Data_List.append(drive_Time3)
            elif data_Name == 'From 70 Max':
                Data_List.append(0.01)
            elif data_Name == '4 Drive':
                Data_List.append(drive_Time4)
            elif data_Name == 'F Slip':
                Data_List.append(f_slip_Time)
            elif data_Name == 'Pause 1':
                Data_List.append(pause_Time1)
            elif data_Name == 'Max':
                Data_List.append(0.01)
            elif data_Name == 'Pause 2':
                Data_List.append(pause_Time2)
            elif data_Name == '5 Recov':
                Data_List.append(recovery_Time5)
            elif data_Name == 'Total Stroke':
                Data_List.append(stroke_Time)
            elif data_Name == 'Total Recov':
                Data_List.append(total_recovery_Time)
            elif data_Name == 'Total Drive':
                Data_List.append(total_Drive)
            elif data_Name == 'Effective Drive':
                Data_List.append(effective_Drive_Time)

    return data_Array

def get_Percentage_Stroke_Timing(profiles_Data, boat_Data, samples=False, sample=1):
    data_Array = {
        'Seat': [],
        'Name': [],
        'Side': [],

        '% Effective Drive / Total Drive': [],
        '% Total Drive': [],
        '% Recovery': [],
        '% Hang': [],
        '% Catch Slip': [],
        '% Effective Drive': [],
        '% Finish Slip': [],
        '% Pause': [],
    }

    for data_Name in data_Array:
        for rower in profiles_Data:
            Data_List = data_Array[data_Name]

            section = Subroutines.section_Data
            def sec_Data(array):
                return section(array, boat_Data)

            if samples:
                stroke_Time = sec_Data(rower.data['Stroke Time'])[sample-1]
                recovery_Time1 = sec_Data(rower.data['Recovery Time 1'])[sample-1]
                recovery_Time2 = sec_Data(rower.data['Recovery Time 2'])[sample-1]
                recovery_Time3 = sec_Data(rower.data['Recovery Time 3'])[sample-1]
                recovery_Time4 = sec_Data(rower.data['Recovery Time 4'])[sample-1]
                hang_Time1 = sec_Data(rower.data['Hang Time 1'])[sample-1]
                hang_Time2 = sec_Data(rower.data['Hang Time 2'])[sample-1]
                c_slip_Time = sec_Data(rower.data['Catch Slip Time'])[sample-1]
                drive_Time1 = sec_Data(rower.data['Drive Time 1'])[sample-1]
                drive_Time2 = sec_Data(rower.data['Drive Time 2'])[sample-1]
                drive_Time3 = sec_Data(rower.data['Drive Time 3'])[sample-1]
                f_slip_Time = sec_Data(rower.data['Finish Slip Time'])[sample-1]
                pause_Time1 = sec_Data(rower.data['Pause Time 1'])[sample-1]
                pause_Time2 = sec_Data(rower.data['Pause Time 2'])[sample-1]
                recovery_Time5 = sec_Data(rower.data['Recovery Time 5'])[sample-1]
            else:
                stroke_Time = float(Subroutines.calculate_Average(rower.data['Stroke Time']))
                recovery_Time1 = float(Subroutines.calculate_Average(rower.data['Recovery Time 1']))
                recovery_Time2 = float(Subroutines.calculate_Average(rower.data['Recovery Time 2']))
                recovery_Time3 = float(Subroutines.calculate_Average(rower.data['Recovery Time 3']))
                recovery_Time4 = float(Subroutines.calculate_Average(rower.data['Recovery Time 4']))
                hang_Time1 = float(Subroutines.calculate_Average(rower.data['Hang Time 1']))
                hang_Time2 = float(Subroutines.calculate_Average(rower.data['Hang Time 2']))
                c_slip_Time = float(Subroutines.calculate_Average(rower.data['Catch Slip Time']))
                drive_Time1 = float(Subroutines.calculate_Average(rower.data['Drive Time 1']))
                drive_Time2 = float(Subroutines.calculate_Average(rower.data['Drive Time 2']))
                drive_Time3 = float(Subroutines.calculate_Average(rower.data['Drive Time 3']))
                f_slip_Time = float(Subroutines.calculate_Average(rower.data['Finish Slip Time']))
                pause_Time1 = float(Subroutines.calculate_Average(rower.data['Pause Time 1']))
                pause_Time2 = float(Subroutines.calculate_Average(rower.data['Pause Time 2']))
                recovery_Time5 = float(Subroutines.calculate_Average(rower.data['Recovery Time 5']))

            total_recovery_Time = recovery_Time1 + recovery_Time2 + recovery_Time3 + recovery_Time4 + recovery_Time5 + hang_Time1 + pause_Time2
            effective_Drive_Time = drive_Time1 + drive_Time2 + drive_Time3
            total_Drive = effective_Drive_Time + c_slip_Time + f_slip_Time + hang_Time2 + pause_Time1

            if data_Name == 'Seat':
                Data_List.append(rower.Seat)
            elif data_Name == 'Name':
                Data_List.append(rower.Name)
            elif data_Name == 'Side':
                Data_List.append(rower.Side)
            elif data_Name == '% Effective Drive / Total Drive':
                Data_List.append(round(((effective_Drive_Time / total_Drive) * 100),3))
            elif data_Name == '% Total Drive':
                Data_List.append(round(((total_Drive / stroke_Time) * 100),3))
            elif data_Name == '% Recovery':
                Data_List.append(round(((total_recovery_Time / stroke_Time) * 100),3))
            elif data_Name == '% Hang':
                Data_List.append(round(((hang_Time1 + hang_Time2 / stroke_Time) * 100),3))
            elif data_Name == '% Catch Slip':
                Data_List.append(round(((c_slip_Time / stroke_Time) * 100),3))
            elif data_Name == '% Effective Drive':
                Data_List.append(round(((effective_Drive_Time / stroke_Time) * 100),3))
            elif data_Name == '% Finish Slip':
                Data_List.append(round(((f_slip_Time / stroke_Time) * 100),3))
            elif data_Name == '% Pause':
                Data_List.append(round(((pause_Time1 + pause_Time2 / stroke_Time) * 100),3))

    return data_Array

def get_Rate_Timeline(boat_Data):
    data_Array = {
        'Avg Rate': [],
    }

    Rate_Samples = Subroutines.section_Data(boat_Data.data['Rating'], boat_Data)

    for i in range(len(Rate_Samples)):
        temp_Dict = {str(i + 1): []}
        data_Array.update(temp_Dict)

    avg_Rate_Dict = {'Avg Rate': []}
    sd_Rate_Dict = {'SD': []}
    data_Array.update(avg_Rate_Dict)
    data_Array.update(sd_Rate_Dict)

    for data_Name in data_Array:
        Data_List = data_Array[data_Name]

        if data_Name == 'Avg Rate':
            Data_List.append(round(Subroutines.calculate_Average(Rate_Samples),3))
        elif data_Name == 'SD':
            Data_List.append(round(Subroutines.calcuate_SD(Rate_Samples),3))
        else:
            Data_List.append(round(Rate_Samples[int(data_Name)-1],3))

    return data_Array

def get_ArcLength_Timeline(profiles_Data, boat_Data):
    data_Array = {
        'Seat': [],
        'Name': [],
        'Side': [],
    }

    numof_Samples = len(Subroutines.section_Data(boat_Data.data['Rating'], boat_Data))

    for i in range(numof_Samples):
        temp_Dict = {str(i + 1): []}
        data_Array.update(temp_Dict)

    sd_Arc_Dict = {'SD': []}
    avg_Arc_Dict = {'Avg /deg': []}
    p_avg_Arc_Dict = {'% Avg /deg': []}
    data_Array.update(sd_Arc_Dict)
    data_Array.update(avg_Arc_Dict)
    data_Array.update(p_avg_Arc_Dict)


    for data_Name in data_Array:
        for rower in profiles_Data:
            Data_List = data_Array[data_Name]

            ArcLength_Samples = Subroutines.section_Data(rower.data['ArcLength'], boat_Data)
            arc_Length_Avg = float(Subroutines.calculate_Average(rower.data['ArcLength']))

            if data_Name == 'Seat':
                Data_List.append(rower.Seat)
            elif data_Name == 'Name':
                Data_List.append(rower.Name)
            elif data_Name == 'Side':
                Data_List.append(rower.Side)
            elif data_Name == 'Avg /deg':
                Data_List.append(round(arc_Length_Avg,3))
            elif data_Name == '% Avg /deg':
                crew_Avg = Subroutines.crew_Average('ArcLength', profiles_Data)
                percent_Of_Boat = (arc_Length_Avg / crew_Avg) * 100
                Data_List.append(round(percent_Of_Boat,3))
            elif data_Name == 'SD':
                Data_List.append(round(Subroutines.calcuate_SD(ArcLength_Samples),3))
            elif data_Name != '':
                Data_List.append(round(ArcLength_Samples[int(data_Name) - 1],3))

    return data_Array

def get_GateForceX(profiles_Data, boat_Data):
    data_Array = {
        'Seat': [],
        'Name': [],
        'Side': [],
    }

    numof_Samples = len(Subroutines.section_Data(boat_Data.data['Rating'], boat_Data))

    for i in range(numof_Samples):
        temp_Dict = {str(i + 1): []}
        data_Array.update(temp_Dict)

    sd_GFX_Dict = {'SD': []}
    avg_GFX_Dict = {'Avg /kgf': []}
    p_avg_GFX_Dict = {'% Avg /kgf': []}
    data_Array.update(sd_GFX_Dict)
    data_Array.update(avg_GFX_Dict)
    data_Array.update(p_avg_GFX_Dict)

    for data_Name in data_Array:
        for rower in profiles_Data:
            Data_List = data_Array[data_Name]

            gate_Force_Samples = Subroutines.section_Data(rower.data['MaxGateForceX'], boat_Data)
            gate_Force_Avg = float(Subroutines.calculate_Average(rower.data['MaxGateForceX']))

            if data_Name == 'Seat':
                Data_List.append(rower.Seat)
            elif data_Name == 'Name':
                Data_List.append(rower.Name)
            elif data_Name == 'Side':
                Data_List.append(rower.Side)
            elif data_Name == 'SD':
                Data_List.append(round(Subroutines.calcuate_SD(gate_Force_Samples),3))
            elif data_Name == 'Avg /kgf':
                Data_List.append(round(gate_Force_Avg,3))
            elif data_Name == '% Avg /kgf':
                crew_Avg = Subroutines.crew_Average('MaxGateForceX', profiles_Data)
                percent_Of_Boat = (gate_Force_Avg / crew_Avg) * 100
                Data_List.append(round(percent_Of_Boat,3))
            elif data_Name != '':
                Data_List.append(round(gate_Force_Samples[int(data_Name) - 1],3))

    return data_Array

def get_Wattage(profiles_Data, boat_Data):
    data_Array = {
        'Seat': [],
        'Name': [],
        'Side': [],
    }

    numof_Samples = len(Subroutines.section_Data(boat_Data.data['Rating'], boat_Data))

    for i in range(numof_Samples):
        temp_Dict = {str(i + 1): []}
        data_Array.update(temp_Dict)

    sd1_Watt_Dict = {'SD': []}
    max_Watt_Dict = {'Max /w': []}
    min_Watt_Dict = {'Min /w': []}
    avg_Watt_Dict = {'Avg /w': []}
    sd_Watt_Dict = {'SD (min,max,avg)': []}
    p_avg_Watt_Dict = {'% Avg /w': []}
    data_Array.update(sd1_Watt_Dict)
    data_Array.update(max_Watt_Dict)
    data_Array.update(min_Watt_Dict)
    data_Array.update(avg_Watt_Dict)
    data_Array.update(sd_Watt_Dict)
    data_Array.update(p_avg_Watt_Dict)

    for data_Name in data_Array:
        for rower in profiles_Data:
            Data_List = data_Array[data_Name]

            Watts = rower.data['Rower Swivel Power']
            Wattage_Samples = Subroutines.section_Data(rower.data['Rower Swivel Power'], boat_Data)
            watts_Avg = float(Subroutines.calculate_Average(rower.data['Rower Swivel Power']))

            if data_Name == 'Seat':
                Data_List.append(rower.Seat)
            elif data_Name == 'Name':
                Data_List.append(rower.Name)
            elif data_Name == 'Side':
                Data_List.append(rower.Side)
            elif data_Name == 'SD':
                Data_List.append(round(Subroutines.calcuate_SD(Wattage_Samples),3))
            elif data_Name == 'Max /w':
                Data_List.append(max(Watts))
            elif data_Name == 'Min /w':
                Data_List.append(min(Watts))
            elif data_Name == 'Avg /w':
                Data_List.append(round(watts_Avg,3))
            elif data_Name == 'SD (min,max,avg)':
                Data_List.append(Subroutines.calcuate_SD([max(Watts), watts_Avg, min(Watts)]))
            elif data_Name == '% Avg /w':
                crew_Avg = Subroutines.crew_Average('Rower Swivel Power', profiles_Data)
                percent_Of_Boat = (watts_Avg / crew_Avg) * 100
                Data_List.append(round(percent_Of_Boat,3))
            elif data_Name != '':
                Data_List.append(round(Wattage_Samples[int(data_Name) - 1],3))

    return data_Array

def get_Crew_Report(recording_sections):
    data_Array = {
        'Seat': [],
        'Crew List': [],
        'Height (m)': [],
        'Weight (kg)': [],
        'Inboard (cm)': [],
        'Oar Length (cm)': [],
    }

    x = {
        'Telemetry Serial': [],
        'File Name': [],
        'Date': [],
        'Strokes': [],
        'File Distance': [],
        'Recorded Distance': [],
        'Recording Time': [],
        'Category': [],
    }

    for session in recording_sections:
        profiles = session[0]
        boat_Data = session[1]

        time_in_minutes = divmod(boat_Data.timeElapsed, 60)
        time_Formatted = f'{str(int(time_in_minutes[0]))}:{str(round(time_in_minutes[1],1))}'

        x['Telemetry Serial'].append(boat_Data.Serial)
        x['File Name'].append(boat_Data.FileName)
        x['Date'].append(boat_Data.Date)
        x['Strokes'].append(boat_Data.tStrokes)
        x['File Distance'].append(str(round(boat_Data.Distance)) + ' m')
        x['Recorded Distance'].append(str(round(Subroutines.get_Sum(boat_Data.data['Distance / Stroke']))) + ' m')
        x['Recording Time'].append(time_Formatted + ' s')
        x['Category'].append(boat_Data.Category)

        for rower in profiles:
            seat = rower.Seat
            name = rower.Name
            height = rower.Height
            weight = rower.Weight
            inboard = boat_Data.Inboard
            oarlength = boat_Data.OarLength

            data_Array['Seat'].append(seat)
            data_Array['Crew List'].append(name)
            data_Array['Height (m)'].append(height)
            data_Array['Weight (kg)'].append('hidden')
            data_Array['Inboard (cm)'].append(inboard)
            data_Array['Oar Length (cm)'].append(oarlength)

    return x, data_Array

def get_Session_Summary(recording_sessions):
    table_One = {
        'Data Sample': [],
        'Distance Segment': [],
        'Rate': [],
        'Rate Variation': [],
        'Sample Time': [],
        'Strokes Count': [],
        'Dist / Stroke': [],
        'Speed m/s': [],
        'Speed m/s Variation': [],
        '500m Pace': [],
        '2000m Pace': [],
    } 

    averageFunc = Subroutines.calculate_Average
    getSD = Subroutines.calcuate_SD
    getVariation = Subroutines.calculate_Variation

    # Containers for data to average / varation / standard deviation
    rate_Container = []
    sample_Time_Container = []
    variation_Speed_Container = []
    rate_Variation_Container = []
    stroke_Count_Container = []
    mps_Container = []
    dps_Container = []
    
    if len(recording_sessions) == 1:
        boat_Data = recording_sessions[0][1]
        def sectionFunc(array, b=False):
            return Subroutines.section_Data(array, boat_Data, b)

        Rate_Samples = sectionFunc(boat_Data.data['Rating'], True)
        Rate_Sections = Subroutines.section_List(boat_Data.data['Rating'], boat_Data)
        Stroke_Time_Samples = sectionFunc(boat_Data.data['Stroke Time'])
        Meters_Per_Second_Samples = sectionFunc(boat_Data.data['Meters/s'])
        Meters_Per_Second_Sections = Subroutines.section_List(boat_Data.data['Meters/s'], boat_Data)
        StrokeTime_Sectioned = Subroutines.section_List(boat_Data.data['Stroke Time'], boat_Data)
        Distance_Per_Stroke_Samples = sectionFunc(boat_Data.data['Distance / Stroke'], boat_Data)

        for index in range(len(Rate_Sections)):
            sample = index+1
            Rate = Rate_Samples[0][index]
            Rate_Variation = getVariation(Rate_Sections[index])
            Sample_Time = Stroke_Time_Samples[index]
            Stroke_Count = Rate_Samples[1][index]
            Sample_Distance = Subroutines.get_Meters_in_Sample(boat_Data, sample)
            Sample_Distance_Text = Subroutines.get_Meters_Sample_Text(boat_Data, sample)
            Meters_Per_Second = Meters_Per_Second_Samples[index]
            Distance_Per_Stroke = Distance_Per_Stroke_Samples[index]
            Meters_Per_Second_Variation = getVariation(Meters_Per_Second_Sections[index])

            rate_Container.append(Rate)
            sample_Time_Container.append(Sample_Time)
            variation_Speed_Container.append(Meters_Per_Second_Variation)
            rate_Variation_Container.append(Rate_Variation)
            stroke_Count_Container.append(Stroke_Count)
            mps_Container.append(Meters_Per_Second)
            dps_Container.append(Distance_Per_Stroke)

            Sample_Time = Subroutines.get_Sum(StrokeTime_Sectioned[index])

            # Time and Split calculations
            Mutliplier = 500 / Sample_Distance
            Split = divmod(Sample_Time * Mutliplier, 60)
            Time_Over_2KM = divmod(Sample_Time * (Mutliplier * 4), 60)
            string_split = f'{str(int(Split[0]))}:{str(round(Split[1],1))}'
            string_Time_Over_2KM = f'{str(int(Time_Over_2KM[0]))}:{str(round(Time_Over_2KM[1],1))}'
            Pace_500M = string_split
            Pace_2000M = string_Time_Over_2KM

            table_One['Data Sample'].append('Sample: 0'+str(index+1))
            table_One['Rate'].append(Rate)
            table_One['Rate Variation'].append(Rate_Variation)
            table_One['Sample Time'].append(str(round(Sample_Time,3)) + ' s')
            table_One['Strokes Count'].append(Stroke_Count)
            table_One['Distance Segment'].append(Sample_Distance_Text)
            table_One['Dist / Stroke'].append(str(round(Distance_Per_Stroke,3)) + ' m')
            table_One['Speed m/s'].append(str(round(Meters_Per_Second,3)) + ' s')
            table_One['500m Pace'].append(Pace_500M)
            table_One['2000m Pace'].append(Pace_2000M)
            table_One['Speed m/s Variation'].append(str(round(Meters_Per_Second_Variation,3)) + ' s')
    else:
        for session in recording_sessions:
            boat_Data = session[1]

            Rate_List = boat_Data.data['Rating']
            Stroke_Time_List = boat_Data.data['Stroke Time']
            MPS_List = boat_Data.data['Meters/s']
            DPS_List = boat_Data.data['Distance / Stroke']

            Rate = averageFunc(Rate_List)
            Rate_Variation = getVariation(Rate_List)
            Sample_Time = Subroutines.get_Sum(Stroke_Time_List)
            Stroke_Count = len(Rate_List)
            Sample_Distance = round(boat_Data.Distance,2)
            Meters_Per_Second = averageFunc(MPS_List)
            Distance_Per_Stroke = averageFunc(DPS_List)
            Meters_Per_Second_Variation = getVariation(MPS_List)

            rate_Container.append(Rate)
            sample_Time_Container.append(Sample_Time)
            variation_Speed_Container.append(Meters_Per_Second_Variation)
            rate_Variation_Container.append(Rate_Variation)
            stroke_Count_Container.append(Stroke_Count)
            mps_Container.append(Meters_Per_Second)
            dps_Container.append(Distance_Per_Stroke)

            # Time and Split calculations
            Mutliplier = 500 / Sample_Distance
            Split = divmod(Sample_Time * Mutliplier, 60)
            Time_Over_2KM = divmod(Sample_Time * (Mutliplier * 4), 60)
            string_split = f'{str(int(Split[0]))}:{str(round(Split[1],1))}'
            string_Time_Over_2KM = f'{str(int(Time_Over_2KM[0]))}:{str(round(Time_Over_2KM[1],1))}'
            Pace_500M = string_split
            Pace_2000M = string_Time_Over_2KM

            table_One['Data Sample'].append(boat_Data.FileName)
            table_One['Rate'].append(Rate)
            table_One['Rate Variation'].append(Rate_Variation)
            table_One['Sample Time'].append(str(round(Sample_Time,3)) + ' s')
            table_One['Strokes Count'].append(Stroke_Count)
            table_One['Distance Segment'].append(str(Sample_Distance) + ' m')
            table_One['Dist / Stroke'].append(str(round(Distance_Per_Stroke,3)) + ' m')
            table_One['Speed m/s'].append(str(round(Meters_Per_Second,3)) + ' s')
            table_One['500m Pace'].append(Pace_500M)
            table_One['2000m Pace'].append(Pace_2000M)
            table_One['Speed m/s Variation'].append(str(round(Meters_Per_Second_Variation,3)) + ' s')

    # Sets up bottom section.
    table_One['Data Sample'].append('Average')
    table_One['Data Sample'].append('Variation')
    table_One['Data Sample'].append('SD')

    # Gets averages
    table_One['Rate'].append(averageFunc(rate_Container))
    table_One['Rate Variation'].append(averageFunc(rate_Variation_Container))
    table_One['Sample Time'].append(averageFunc(sample_Time_Container))
    table_One['Strokes Count'].append(averageFunc(stroke_Count_Container))
    table_One['Distance Segment'].append('')
    table_One['Dist / Stroke'].append(averageFunc(dps_Container))
    table_One['Speed m/s'].append(averageFunc(mps_Container))
    table_One['Speed m/s Variation'].append(averageFunc(variation_Speed_Container))
    table_One['500m Pace'].append('')
    table_One['2000m Pace'].append('')

    # Gets variations
    table_One['Rate'].append(getVariation(rate_Container))
    table_One['Rate Variation'].append(getVariation(rate_Variation_Container))
    table_One['Sample Time'].append(getVariation(sample_Time_Container))
    table_One['Strokes Count'].append(getVariation(stroke_Count_Container))
    table_One['Distance Segment'].append('')
    table_One['Dist / Stroke'].append(getVariation(dps_Container))
    table_One['Speed m/s'].append(getVariation(mps_Container))
    table_One['Speed m/s Variation'].append(getVariation(variation_Speed_Container))
    table_One['500m Pace'].append('')
    table_One['2000m Pace'].append('')

    # Get SD
    table_One['Rate'].append(getSD(rate_Container))
    table_One['Rate Variation'].append(getSD(rate_Variation_Container))
    table_One['Sample Time'].append(getSD(sample_Time_Container))
    table_One['Strokes Count'].append(getSD(stroke_Count_Container))
    table_One['Distance Segment'].append('')
    table_One['Dist / Stroke'].append(getSD(dps_Container))
    table_One['Speed m/s'].append(getSD(mps_Container))
    table_One['Speed m/s Variation'].append(getSD(variation_Speed_Container))
    table_One['500m Pace'].append('')
    table_One['2000m Pace'].append('')

    return table_One


def get_Rower_Summary(boat_Data, rower):
    table_One = {
        'Data Sample': [],
        'Distance Segment': [],
        'Rate': [],
        'Recovery Time': [],
        'Drive Time': [],
        'Rhythm %': [],
        'Position of Max F %': [],
        'Catch Force Gradient': [],
        'Finish Force Gradient': [],
        'Catch': [],
        'Effective Start': [],
        '70% Max F': [],
        'Max F': [],
        'From 70% Max F': [],
        'Effective End': [],
        'Finish': [],
        'ArcLength': [],
        'Effective Length': [],
        '% Effective / Arc': [],
        'Catch Slip': [],
        'Finish Slip': [],
    }

    table_Two = {
        'Data Sample': [],
        'Distance Segment': [],
        'Max Force': [],
        'Avg Force': [],
        'Avg / Max Force': [],
        'Max Power': [],
        'Avg Power': [],
        'Avg w/kg': [],
        'Min Power': [],
        'Variation (min, max)': [],
        'SD': [],
    }

    table_Three = {
        'Criteria': [],
        'Gold Target': [],
        'Actual Data': [],
        '% of Target': [],
    }

    def sectionFunc(array, b=False):
        return Subroutines.section_Data(array, boat_Data, b)

    averageFunc = Subroutines.calculate_Average
    getSD = Subroutines.calcuate_SD
    getVariation = Subroutines.calculate_Variation
    getPercentage = Subroutines.calculate_Percentage

    # Turns the rowers data into sections of 8.
    Rate_Samples = sectionFunc(boat_Data.data['Rating'], True)
    RowingPower_Samples = sectionFunc(rower.data['Rower Swivel Power'])
    RowingPower_Sections = Subroutines.section_List(rower.data['Rower Swivel Power'], boat_Data)
    DriveTime_Sections = sectionFunc(rower.data['Total Drive Time'])
    RecoveryTime_Sections = sectionFunc(rower.data['Total Recovery Time'])
    PositionMaxF_Sections = sectionFunc(rower.data['Position_Of_MaxF'])
    Catch_Force_Gradient_Samples = sectionFunc(rower.data['Catch Force Gradient'])
    Finish_Force_Gradient_Samples = sectionFunc(rower.data['Finish Force Gradient'])
    Angle_70MaxF_Samples = sectionFunc(rower.data['Angle_70MaxGateForceX'])
    Angle_MaxF_Samples = sectionFunc(rower.data['Angle_MaxGateForceX'])
    Angle_From70MaxF_Samples = sectionFunc(rower.data['Angle_From70MaxGateForceX'])
    MinAngle_Samples = sectionFunc(rower.data['MinAngle'])
    MaxAngle_Samples = sectionFunc(rower.data['MaxAngle'])
    Angle_Effective_Start_Samples = sectionFunc(rower.data['Effective MinAngle'])
    Angle_Effective_End_Samples = sectionFunc(rower.data['Effective MaxAngle'])
    ArcLength_Samples = sectionFunc(rower.data['ArcLength'])
    EffectiveLength_Samples = sectionFunc(rower.data['Effective Length'])
    CatchSlip_Samples = sectionFunc(rower.data['CatchSlip'])
    FinishSlip_Samples = sectionFunc(rower.data['FinishSlip'])

    MaxForce_Samples = sectionFunc(rower.data['MaxGateForceX'])
    AvgForce_Samples = sectionFunc(rower.data['AvgGateForceX'])
    AvgMax_Samples = sectionFunc(rower.data['Average Force / Max Force'])

    # Gets the total time per sample
    StrokeTime_Sectioned = Subroutines.section_List(rower.data['Stroke Time'], boat_Data)
    StrokeTime_Samples = []
    for section in StrokeTime_Sectioned:
        StrokeTime_Samples.append(Subroutines.get_Sum(section))

    MaxRowingPower_Array = []
    for section in RowingPower_Sections:
        MaxRowingPower_Array.append(max(section))
    
    MinRowingPower_Array = []
    for section in RowingPower_Sections:
        MinRowingPower_Array.append(min(section))

    EffecLengthPercent = []
    VariationPower_Container = []
    Watts_per_Kilo_Container = []
    Rhythm_Container = []
    
    sections = len(RowingPower_Samples)
    for index in range(sections):
        effl = Subroutines.calculate_Percentage(ArcLength_Samples[index], EffectiveLength_Samples[index])
        EffecLengthPercent.append(effl)

    for index in range(sections):
        rhythm = getPercentage(RecoveryTime_Sections[index] + DriveTime_Sections[index], DriveTime_Sections[index])
        Rhythm_Container.append(rhythm)
        table_One['Data Sample'].append('Sample: 0'+str(index+1))
        table_One['Distance Segment'].append(Subroutines.get_Meters_Sample_Text(boat_Data, index+1))
        table_One['Rate'].append(round(Rate_Samples[0][index],3))
        table_One['Position of Max F %'].append(round(PositionMaxF_Sections[index],3))
        table_One['Catch Force Gradient'].append(round(Catch_Force_Gradient_Samples[index],3))
        table_One['Finish Force Gradient'].append(round(Finish_Force_Gradient_Samples[index],3))
        table_One['70% Max F'].append(round(Angle_70MaxF_Samples[index],3))
        table_One['Max F'].append(round(Angle_MaxF_Samples[index],3))
        table_One['From 70% Max F'].append(round(Angle_From70MaxF_Samples[index],3))
        table_One['Drive Time'].append(round(DriveTime_Sections[index],3))
        table_One['Recovery Time'].append(round(RecoveryTime_Sections[index],3))
        table_One['Rhythm %'].append(round(rhythm,3))
        table_One['Effective End'].append(round(Angle_Effective_End_Samples[index],3))
        table_One['Effective Start'].append(round(Angle_Effective_Start_Samples[index],3))
        table_One['Catch'].append(round(MinAngle_Samples[index],3))
        table_One['Finish'].append(round(MaxAngle_Samples[index],3))
        table_One['ArcLength'].append(round(ArcLength_Samples[index],3))
        table_One['Effective Length'].append(round(EffectiveLength_Samples[index],3))
        table_One['% Effective / Arc'].append(round(EffecLengthPercent[index],3))
        table_One['Catch Slip'].append(round(CatchSlip_Samples[index],3))
        table_One['Finish Slip'].append(round(FinishSlip_Samples[index],3))

        max_Power = max(RowingPower_Sections[index])
        min_Power = min(RowingPower_Sections[index])
        avg_Power = RowingPower_Samples[index]
        watts_Per_Kilo = avg_Power / rower.Weight
        variation_Power = getVariation([max_Power, min_Power])
        VariationPower_Container.append(variation_Power)
        Watts_per_Kilo_Container.append(watts_Per_Kilo)

        table_Two['Data Sample'].append('Sample: 0'+str(index+1))
        table_Two['Distance Segment'].append(Subroutines.get_Meters_Sample_Text(boat_Data, index+1))
        table_Two['Max Force'].append(round(MaxForce_Samples[index],3))
        table_Two['Avg Force'].append(round(AvgForce_Samples[index],3))
        table_Two['Avg / Max Force'].append(str(round(AvgMax_Samples[index],3)) + '%')
        table_Two['Max Power'].append(max_Power)
        table_Two['Avg Power'].append(round(avg_Power,3))
        table_Two['Avg w/kg'].append(watts_Per_Kilo)
        table_Two['Min Power'].append(min_Power)
        table_Two['Variation (min, max)'].append(variation_Power)
        table_Two['SD'].append(getSD([max(RowingPower_Sections[index]), RowingPower_Samples[index], min(RowingPower_Sections[index])]))

    table_One['Data Sample'].append('Average')
    table_One['Data Sample'].append('Variation')
    table_One['Data Sample'].append('SD')

    table_Two['Data Sample'].append('Average')
    table_Two['Data Sample'].append('Variation')
    table_Two['Data Sample'].append('SD')

    # Calculating averages from samples.
    table_One['Distance Segment'].append('')
    table_One['Rate'].append(averageFunc(Rate_Samples[0]))
    table_One['Recovery Time'].append(averageFunc(RecoveryTime_Sections))
    table_One['Drive Time'].append(averageFunc(DriveTime_Sections))
    table_One['Rhythm %'].append(averageFunc(Rhythm_Container))
    table_One['Position of Max F %'].append(averageFunc(PositionMaxF_Sections))
    table_One['Catch Force Gradient'].append(averageFunc(Catch_Force_Gradient_Samples))
    table_One['Finish Force Gradient'].append(averageFunc(Finish_Force_Gradient_Samples))
    table_One['70% Max F'].append(averageFunc(Angle_70MaxF_Samples))
    table_One['Max F'].append(averageFunc(Angle_MaxF_Samples))
    table_One['From 70% Max F'].append(averageFunc(Angle_From70MaxF_Samples))
    table_One['Effective End'].append(averageFunc(Angle_Effective_End_Samples))
    table_One['Effective Start'].append(averageFunc(Angle_Effective_Start_Samples))
    table_One['Catch'].append(averageFunc(MinAngle_Samples))
    table_One['Finish'].append(averageFunc(MaxAngle_Samples))
    table_One['ArcLength'].append(averageFunc(ArcLength_Samples))
    table_One['Effective Length'].append(averageFunc(EffectiveLength_Samples))
    table_One['% Effective / Arc'].append(averageFunc(EffecLengthPercent))
    table_One['Catch Slip'].append(averageFunc(CatchSlip_Samples))
    table_One['Finish Slip'].append(averageFunc(FinishSlip_Samples))

    table_Two['Distance Segment'].append('')
    table_Two['Max Force'].append(averageFunc(MaxForce_Samples))
    table_Two['Avg Force'].append(averageFunc(AvgForce_Samples))
    table_Two['Avg / Max Force'].append(averageFunc(AvgMax_Samples))
    table_Two['Max Power'].append(averageFunc(MaxRowingPower_Array))
    table_Two['Avg Power'].append(averageFunc(RowingPower_Samples))
    table_Two['Avg w/kg'].append(averageFunc(Watts_per_Kilo_Container))
    table_Two['Min Power'].append(averageFunc(MinRowingPower_Array))
    table_Two['Variation (min, max)'].append(averageFunc(VariationPower_Container))
    table_Two['SD'].append(getSD([averageFunc(MaxRowingPower_Array), averageFunc(RowingPower_Samples), averageFunc(MinRowingPower_Array)]))

    # Calculating variation between data.
    table_One['Distance Segment'].append('')
    table_One['Rate'].append(getVariation(Rate_Samples[0]))
    table_One['Recovery Time'].append(getVariation(RecoveryTime_Sections))
    table_One['Drive Time'].append(getVariation(DriveTime_Sections))
    table_One['Rhythm %'].append(getVariation(Rhythm_Container))
    table_One['Position of Max F %'].append(getVariation(PositionMaxF_Sections))
    table_One['Catch Force Gradient'].append(getVariation(Catch_Force_Gradient_Samples))
    table_One['Finish Force Gradient'].append(getVariation(Finish_Force_Gradient_Samples))
    table_One['70% Max F'].append(getVariation(Angle_70MaxF_Samples))
    table_One['From 70% Max F'].append(getVariation(Angle_From70MaxF_Samples))
    table_One['Max F'].append(getVariation(Angle_MaxF_Samples))
    table_One['Effective End'].append(getVariation(Angle_Effective_End_Samples))
    table_One['Effective Start'].append(getVariation(Angle_Effective_Start_Samples))
    table_One['Catch'].append(getVariation(MinAngle_Samples))
    table_One['Finish'].append(getVariation(MaxAngle_Samples))
    table_One['ArcLength'].append(getVariation(ArcLength_Samples))
    table_One['Effective Length'].append(getVariation(EffectiveLength_Samples))
    table_One['% Effective / Arc'].append(getVariation(EffecLengthPercent))
    table_One['Catch Slip'].append(getVariation(CatchSlip_Samples))
    table_One['Finish Slip'].append(getVariation(FinishSlip_Samples))

    table_Two['Distance Segment'].append('')
    table_Two['Max Force'].append(getVariation(MaxForce_Samples))
    table_Two['Avg Force'].append(getVariation(AvgForce_Samples))
    table_Two['Avg / Max Force'].append(getVariation(AvgMax_Samples))
    table_Two['Max Power'].append(getVariation(MaxRowingPower_Array))
    table_Two['Avg Power'].append(getVariation(RowingPower_Samples))
    table_Two['Avg w/kg'].append(getVariation(Watts_per_Kilo_Container))
    table_Two['Min Power'].append(getVariation(MinRowingPower_Array))
    table_Two['Variation (min, max)'].append(getVariation(VariationPower_Container))
    table_Two['SD'].append('')

    # Calculating Standard Deviation from samples.
    table_One['Distance Segment'].append('')
    table_One['Rate'].append(getSD(Rate_Samples[0]))
    table_One['Recovery Time'].append(getSD(RecoveryTime_Sections))
    table_One['Drive Time'].append(getSD(DriveTime_Sections))
    table_One['Rhythm %'].append(getSD(Rhythm_Container))
    table_One['Position of Max F %'].append(getSD(PositionMaxF_Sections))
    table_One['Catch Force Gradient'].append(getSD(Catch_Force_Gradient_Samples))
    table_One['Finish Force Gradient'].append(getSD(Finish_Force_Gradient_Samples))
    table_One['70% Max F'].append(getSD(Angle_70MaxF_Samples))
    table_One['Max F'].append(getSD(Angle_MaxF_Samples))
    table_One['From 70% Max F'].append(getSD(Angle_From70MaxF_Samples))
    table_One['Effective End'].append(getSD(Angle_Effective_End_Samples))
    table_One['Effective Start'].append(getSD(Angle_Effective_Start_Samples))
    table_One['Catch'].append(getSD(MinAngle_Samples))
    table_One['Finish'].append(getSD(MaxAngle_Samples))
    table_One['ArcLength'].append(getSD(ArcLength_Samples))
    table_One['Effective Length'].append(getSD(EffectiveLength_Samples))
    table_One['% Effective / Arc'].append(getSD(EffecLengthPercent))
    table_One['Catch Slip'].append(getSD(CatchSlip_Samples))
    table_One['Finish Slip'].append(getSD(FinishSlip_Samples))

    table_Two['Distance Segment'].append('')
    table_Two['Max Force'].append(getSD(MaxForce_Samples))
    table_Two['Avg Force'].append(getSD(AvgForce_Samples))
    table_Two['Avg / Max Force'].append(getSD(AvgMax_Samples))
    table_Two['Max Power'].append(getSD(MaxRowingPower_Array))
    table_Two['Avg Power'].append(getSD(RowingPower_Samples))
    table_Two['Avg w/kg'].append(getSD(Watts_per_Kilo_Container))
    table_Two['Min Power'].append(getSD(MinRowingPower_Array))
    table_Two['Variation (min, max)'].append(getSD(VariationPower_Container))
    table_Two['SD'].append('')

    # Gold medal targets
    target_Data = Gold_Target.get_Target(boat_Data.Category)
    get_Percentage = Subroutines.calculate_Percentage

    table_Three['Criteria'].append('Name')
    table_Three['Gold Target'].append(rower.Name)
    table_Three['Actual Data'].append('')
    table_Three['% of Target'].append('')

    target_Power = target_Data['Power']
    actual_Power = averageFunc(rower.data['Rower Swivel Power'])
    table_Three['Criteria'].append('2KM Power (w)')
    table_Three['Gold Target'].append(target_Power)
    table_Three['Actual Data'].append(actual_Power)
    table_Three['% of Target'].append(get_Percentage(target_Power, actual_Power))

    target_Length = target_Data['Arc Length']
    actual_Length = averageFunc(rower.data['ArcLength'])
    table_Three['Criteria'].append('Arc Length °')
    table_Three['Gold Target'].append(target_Length)
    table_Three['Actual Data'].append(actual_Length)
    table_Three['% of Target'].append(get_Percentage(target_Length, actual_Length))

    target_Catch = target_Data['Catch Angle']
    actual_Catch = averageFunc(rower.data['MinAngle'])
    table_Three['Criteria'].append('Catch Angle °')
    table_Three['Gold Target'].append(target_Catch)
    table_Three['Actual Data'].append(actual_Catch)
    table_Three['% of Target'].append(get_Percentage(target_Catch, actual_Catch))

    target_Finish = target_Data['Finish Angle']
    actual_Finish = averageFunc(rower.data['MaxAngle'])
    table_Three['Criteria'].append('Finish Angle °')
    table_Three['Gold Target'].append(target_Finish)
    table_Three['Actual Data'].append(actual_Finish)
    table_Three['% of Target'].append(get_Percentage(target_Finish, actual_Finish))

    target_CSlip = target_Data['Catch Slip']
    actual_CSlip = averageFunc(rower.data['CatchSlip'])
    table_Three['Criteria'].append('Catch Slip °')
    table_Three['Gold Target'].append(target_CSlip)
    table_Three['Actual Data'].append(actual_CSlip)
    table_Three['% of Target'].append(get_Percentage(target_CSlip, actual_CSlip))

    target_FSlip = target_Data['Finish Slip']
    actual_FSlip = averageFunc(rower.data['FinishSlip'])
    table_Three['Criteria'].append('Finish Slip °')
    table_Three['Gold Target'].append(target_FSlip)
    table_Three['Actual Data'].append(actual_FSlip)
    table_Three['% of Target'].append(get_Percentage(target_FSlip, actual_FSlip))

    target_EffectiveArc = target_Data['Effective Length']
    actual_EffectiveArc = averageFunc(rower.data['Effective Length'])
    table_Three['Criteria'].append('Effective Arc °')
    table_Three['Gold Target'].append(target_EffectiveArc)
    table_Three['Actual Data'].append(actual_EffectiveArc)
    table_Three['% of Target'].append(get_Percentage(target_EffectiveArc, actual_EffectiveArc))

    target_EffectiveCatch = target_Catch + target_CSlip
    actual_EffectiveCatch = averageFunc(rower.data['Effective MinAngle'])
    table_Three['Criteria'].append('Effective Catch °')
    table_Three['Gold Target'].append(target_EffectiveCatch)
    table_Three['Actual Data'].append(actual_EffectiveCatch)
    table_Three['% of Target'].append(get_Percentage(target_EffectiveCatch, actual_EffectiveCatch))

    target_EffectiveFinish = target_Finish - target_FSlip
    actual_EffectiveFinish = averageFunc(rower.data['Effective MaxAngle'])
    table_Three['Criteria'].append('Effective Finish °')
    table_Three['Gold Target'].append(target_EffectiveFinish)
    table_Three['Actual Data'].append(actual_EffectiveFinish)
    table_Three['% of Target'].append(get_Percentage(target_EffectiveFinish, actual_EffectiveFinish))

    target_PositionMaxF = target_Data['Position of peak force']
    actual_PositionMaxF = averageFunc(rower.data['Position_Of_MaxF'])
    table_Three['Criteria'].append('Position of Max F %')
    table_Three['Gold Target'].append(target_PositionMaxF)
    table_Three['Actual Data'].append(actual_PositionMaxF)
    table_Three['% of Target'].append(get_Percentage(target_PositionMaxF, actual_PositionMaxF))

    target_Avg_MaxF = target_Data['Aver / Max Force']
    actual_Avg_MaxF = averageFunc(rower.data['Average Force / Max Force'])
    table_Three['Criteria'].append('Aver / Max F %')
    table_Three['Gold Target'].append(target_Avg_MaxF)
    table_Three['Actual Data'].append(actual_Avg_MaxF)
    table_Three['% of Target'].append(get_Percentage(target_Avg_MaxF, actual_Avg_MaxF))

    return table_One, table_Two, table_Three



def get_Crew_Summary(profiles, boat_Data, sample=1, average=False):
    index = sample-1
    table_One = {
        'Seat': [],
        'Name': [],
        'Recovery Time': [],
        'Drive Time': [],
        'Rhythm %': [],
        'Position of Max F %': [],
        'Catch Force Gradient': [],
        'Finish Force Gradient': [],
        'Catch': [],
        'Effective Start': [],
        '70% Max F': [],
        'Max F': [],
        'From 70% Max F': [],
        'Effective End': [],
        'Finish': [],
        'ArcLength': [],
        'Effective Length': [],
        '% Effective / Arc': [],
        'Catch Slip': [],
        'Finish Slip': [],
    }

    table_Two = {
        'Seat': [],
        'Name': [],
        'Max Force': [],
        'Avg Force': [],
        'Avg / Max Force': [],
        'Max Power': [],
        'Avg Power': [],
        'Avg w/kg': [],
        'Min Power': [],
        'Variation (min, max)': [],
        'SD': [],
    }
    
    output_data = []

    def sectionFunc(array, b=False):
        sections = boat_Data.Samples
        return Subroutines.section_Data(array, boat_Data, b)

    averageFunc = Subroutines.calculate_Average
    getSD = Subroutines.calcuate_SD
    getVariation = Subroutines.calculate_Variation
    getPercentage = Subroutines.calculate_Percentage
    
    RecoveryTime_Container = []
    DriveTime_Container = []
    Rhythm_Contianer = []
    PositionMaxF_Container = []
    CatchForceGradient_Container = []
    FinishForceGradient_Container = []
    Angle70MaxF_Container = []
    AngleMaxF_Container = []
    AngleFrom70MaxF_Container = []
    MinAngles_Container = []
    MaxAngles_Container = []
    EffectiveStart_Container = []
    EffectiveEnd_Container = []
    ArcLength_Container = []
    Effective_Length_Container = []
    Effective_Length_Percent_Container = []
    CatchSlip_Container = []
    FinishSlip_Container = []

    Max_Force_Container = []
    Avg_Force_Container = []
    AvgMaxForce_Container = []

    Max_Power_Container = []
    Average_Power_Container = []
    Watt_Per_Kilo_Container = []
    Min_Power_Container = []
    Variation_Power_Container = []

    # Data for Text Output
    if not average:
        Rate_Samples = sectionFunc(boat_Data.data['Rating'], True)
        Distance_Segment = Subroutines.get_Meters_Sample_Text(boat_Data, index+1)

        StrokeTime_Sectioned = Subroutines.section_List(boat_Data.data['Stroke Time'], boat_Data)
        StrokeTime_Samples = []
        for section in StrokeTime_Sectioned:
            StrokeTime_Samples.append(Subroutines.get_Sum(section))

        Rate = Rate_Samples[0][index]
        Strokes = Rate_Samples[1][index]

        # Calculate Splits
        Distance = Subroutines.get_Meters_in_Sample(boat_Data, sample)
        Time = StrokeTime_Samples[index]
        Mutliplier = 500 / Distance
        Split = divmod(Time * Mutliplier, 60)
        Time_Over_2KM = divmod(Time * (Mutliplier * 4), 60)

        string_split = f'{str(int(Split[0]))}:{str(round(Split[1],1))}'
        string_Time_Over_2KM = f'{str(int(Time_Over_2KM[0]))}:{str(round(Time_Over_2KM[1],1))}'

        output_data = [Distance_Segment, round(Time), Strokes, Rate, string_Time_Over_2KM, string_split]

    for rower in profiles:
        if not average:
            # Turns the rowers data into sections of 8 based off their recoring in distance.
            DriveTime_Samples = sectionFunc(rower.data['Total Drive Time'])
            RecoveryTime_Samples = sectionFunc(rower.data['Total Recovery Time'])
            RowingPower_Samples = sectionFunc(rower.data['Rower Swivel Power'])
            RowingPower_Sections = Subroutines.section_List(rower.data['Rower Swivel Power'], boat_Data)
            PositionMaxF_Sections = sectionFunc(rower.data['Position_Of_MaxF'])
            Catch_Force_Gradient_Samples = sectionFunc(rower.data['Catch Force Gradient'])
            Finish_Force_Gradient_Samples = sectionFunc(rower.data['Finish Force Gradient'])
            Angle70MaxF_Samples = sectionFunc(rower.data['Angle_70MaxGateForceX'])
            AngleMaxF_Samples = sectionFunc(rower.data['Angle_MaxGateForceX'])
            Angle_From70MaxF_Samples = sectionFunc(rower.data['Angle_From70MaxGateForceX'])
            MinAngle_Samples = sectionFunc(rower.data['MinAngle'])
            MaxAngle_Samples = sectionFunc(rower.data['MaxAngle'])
            EffectiveStart_Samples = sectionFunc(rower.data['Effective MinAngle'])
            EffectiveEnd_Samples = sectionFunc(rower.data['Effective MaxAngle'])
            ArcLength_Samples = sectionFunc(rower.data['ArcLength'])
            EffectiveLength_Samples = sectionFunc(rower.data['Effective Length'])
            CatchSlip_Samples = sectionFunc(rower.data['CatchSlip'])
            FinishSlip_Samples = sectionFunc(rower.data['FinishSlip'])
            Max_Force_Samples = sectionFunc(rower.data['MaxGateForceX'])
            Avg_Force_Samples = sectionFunc(rower.data['AvgGateForceX'])
            MaxAvg_Force_Samples = sectionFunc(rower.data['Average Force / Max Force'])

            # Defining data
            RecoveryTime = RecoveryTime_Samples[index]
            DriveTime = DriveTime_Samples[index]
            Rhythm = getPercentage(RecoveryTime + DriveTime, DriveTime)
            PositionMaxF = PositionMaxF_Sections[index]
            CatchForceGradient = Catch_Force_Gradient_Samples[index]
            FinishForceGradient = Finish_Force_Gradient_Samples[index]
            Angle70MaxF = Angle70MaxF_Samples[index]
            AngleMaxF = AngleMaxF_Samples[index]
            AngleFrom70MaxF = Angle_From70MaxF_Samples[index]
            Catch = MinAngle_Samples[index]
            Finish = MaxAngle_Samples[index]
            EffectiveStart = EffectiveStart_Samples[index]
            EFfectiveEnd = EffectiveEnd_Samples[index]
            ArcLength = ArcLength_Samples[index]
            Effective_Length = EffectiveLength_Samples[index]
            Effective_Length_Percentage = getPercentage(ArcLength_Samples[index], EffectiveLength_Samples[index])
            CatchSlip = CatchSlip_Samples[index]
            FinishSlip = FinishSlip_Samples[index]

            MaxForce = Max_Force_Samples[index]
            AvgForce = Avg_Force_Samples[index]
            MaxAvgForce = MaxAvg_Force_Samples[index]
            MaxPower = max(RowingPower_Sections[index])
            AvgPower = RowingPower_Samples[index]
            MinPower = min(RowingPower_Sections[index])
            watts_Per_Kilo = AvgPower / rower.Weight
            Power_Variation = getVariation([MaxPower, MinPower])
            Variation_Power_Container.append(Power_Variation)
            Watt_Per_Kilo_Container.append(watts_Per_Kilo)
        else:
            DriveTime_Avg = averageFunc(rower.data['Total Drive Time'])
            RecoveryTime_Avg = averageFunc(rower.data['Total Recovery Time'])
            Rowing_Power_List = rower.data['Rower Swivel Power']
            RowingPower_Avg = averageFunc(Rowing_Power_List)
            PositionMaxF_Avg = averageFunc(rower.data['Position_Of_MaxF'])
            Catch_Force_Gradient_Avg = averageFunc(rower.data['Catch Force Gradient'])
            Finish_Force_Gradient_Avg = averageFunc(rower.data['Finish Force Gradient'])
            Angle70MaxF_Avg = averageFunc(rower.data['Angle_70MaxGateForceX'])
            AngleMaxF_Avg = averageFunc(rower.data['Angle_MaxGateForceX'])
            Angle_From70MaxF_Avg = averageFunc(rower.data['Angle_From70MaxGateForceX'])
            MinAngle_Avg = averageFunc(rower.data['MinAngle'])
            MaxAngle_Avg = averageFunc(rower.data['MaxAngle'])
            EffectiveStart_Avg = averageFunc(rower.data['Effective MinAngle'])
            EffectiveEnd_Avg = averageFunc(rower.data['Effective MaxAngle'])
            ArcLength_Avg = averageFunc(rower.data['ArcLength'])
            EffectiveLength_Avg = averageFunc(rower.data['Effective Length'])
            CatchSlip_Avg = averageFunc(rower.data['CatchSlip'])
            FinishSlip_Avg = averageFunc(rower.data['FinishSlip'])
            Max_Force_Avg = averageFunc(rower.data['MaxGateForceX'])
            Avg_Force_Avg = averageFunc(rower.data['AvgGateForceX'])
            MaxAvg_Force_Avg = averageFunc(rower.data['Average Force / Max Force'])

            # Defining data
            DriveTime = DriveTime_Avg
            RecoveryTime = RecoveryTime_Avg
            Rhythm = getPercentage(RecoveryTime + DriveTime, DriveTime)
            PositionMaxF = PositionMaxF_Avg
            CatchForceGradient = Catch_Force_Gradient_Avg
            FinishForceGradient = Finish_Force_Gradient_Avg
            Angle70MaxF = Angle70MaxF_Avg
            AngleMaxF = AngleMaxF_Avg
            AngleFrom70MaxF = Angle_From70MaxF_Avg
            Catch = MinAngle_Avg
            Finish = MaxAngle_Avg
            EffectiveStart = EffectiveStart_Avg
            EFfectiveEnd = EffectiveEnd_Avg
            ArcLength = ArcLength_Avg
            Effective_Length = EffectiveLength_Avg
            Effective_Length_Percentage = getPercentage(ArcLength_Avg, EffectiveLength_Avg)
            CatchSlip = CatchSlip_Avg
            FinishSlip = FinishSlip_Avg

            MaxForce = Max_Force_Avg
            AvgForce = Avg_Force_Avg
            MaxAvgForce = MaxAvg_Force_Avg
            MaxPower = max(Rowing_Power_List)
            AvgPower = RowingPower_Avg
            MinPower = min(Rowing_Power_List)
            watts_Per_Kilo = AvgPower / rower.Weight
            Power_Variation = getVariation([MaxPower, MinPower])
            Variation_Power_Container.append(Power_Variation)
            Watt_Per_Kilo_Container.append(watts_Per_Kilo)

        # Saving data
        RecoveryTime_Container.append(RecoveryTime)
        DriveTime_Container.append(DriveTime)
        Rhythm_Contianer.append(Rhythm)
        PositionMaxF_Container.append(PositionMaxF)
        CatchForceGradient_Container.append(CatchForceGradient)
        FinishForceGradient_Container.append(FinishForceGradient)
        Angle70MaxF_Container.append(Angle70MaxF)
        AngleMaxF_Container.append(AngleMaxF)
        AngleFrom70MaxF_Container.append(AngleFrom70MaxF)
        MinAngles_Container.append(Catch)
        MaxAngles_Container.append(Finish)
        EffectiveStart_Container.append(EffectiveStart)
        EffectiveEnd_Container.append(EFfectiveEnd)
        ArcLength_Container.append(ArcLength)
        Effective_Length_Container.append(Effective_Length)
        Effective_Length_Percent_Container.append(Effective_Length_Percentage)
        CatchSlip_Container.append(CatchSlip)
        FinishSlip_Container.append(FinishSlip)
        Max_Force_Container.append(MaxForce)
        Avg_Force_Container.append(AvgForce)
        AvgMaxForce_Container.append(MaxAvgForce)
        Max_Power_Container.append(MaxPower)
        Average_Power_Container.append(AvgPower)
        Min_Power_Container.append(MinPower)

        # Setting data.
        table_One['Seat'].append(rower.Seat)
        table_One['Name'].append(rower.Name)
        table_One['Drive Time'].append(round(DriveTime,3))
        table_One['Recovery Time'].append(round(RecoveryTime,3))
        table_One['Rhythm %'].append(round(Rhythm,3))
        table_One['Position of Max F %'].append(round(PositionMaxF,3))
        table_One['Catch Force Gradient'].append(round(CatchForceGradient,3))
        table_One['Finish Force Gradient'].append(round(FinishForceGradient,3))
        table_One['70% Max F'].append(round(Angle70MaxF,3))
        table_One['Max F'].append(round(AngleMaxF,3))
        table_One['From 70% Max F'].append(round(AngleFrom70MaxF,3))
        table_One['Effective Start'].append(round(EffectiveStart,3))
        table_One['Effective End'].append(round(EFfectiveEnd,3))
        table_One['Catch'].append(round(Catch,3))
        table_One['Finish'].append(round(Finish,3))
        table_One['ArcLength'].append(round(ArcLength,3))
        table_One['Effective Length'].append(round(Effective_Length,3))
        table_One['% Effective / Arc'].append(round(Effective_Length_Percentage,3))
        table_One['Catch Slip'].append(round(CatchSlip,3))
        table_One['Finish Slip'].append(round(FinishSlip,3))

        table_Two['Seat'].append(rower.Seat)
        table_Two['Name'].append(rower.Name)
        table_Two['Max Force'].append(round(MaxForce,3))
        table_Two['Avg Force'].append(round(AvgForce,3))
        table_Two['Avg / Max Force'].append(str(round(MaxAvgForce,3)) + '%')
        table_Two['Max Power'].append(MaxPower)
        table_Two['Avg Power'].append(round(AvgPower,3))
        table_Two['Avg w/kg'].append(round(watts_Per_Kilo,3))
        table_Two['Min Power'].append(MinPower)
        table_Two['Variation (min, max)'].append(Power_Variation)
        table_Two['SD'].append(getSD([MaxPower, AvgPower, MinPower]))


    table_One['Seat'].append('Average')
    table_One['Name'].append('')
    table_One['Seat'].append('Variation')
    table_One['Name'].append('')
    table_One['Seat'].append('SD')
    table_One['Name'].append('')

    table_Two['Seat'].append('Average')
    table_Two['Name'].append('')
    table_Two['Seat'].append('Variation')
    table_Two['Name'].append('')
    table_Two['Seat'].append('SD')
    table_Two['Name'].append('')

    # Calculating averages from all rowers.
    table_One['Drive Time'].append(averageFunc(DriveTime_Container))
    table_One['Recovery Time'].append(averageFunc(RecoveryTime_Container))
    table_One['Rhythm %'].append(averageFunc(Rhythm_Contianer))
    table_One['Position of Max F %'].append(averageFunc(PositionMaxF_Container))
    table_One['Catch Force Gradient'].append(averageFunc(CatchForceGradient_Container))
    table_One['Finish Force Gradient'].append(averageFunc(FinishForceGradient_Container))
    table_One['70% Max F'].append(averageFunc(Angle70MaxF_Container))
    table_One['Max F'].append(averageFunc(AngleMaxF_Container))
    table_One['From 70% Max F'].append(averageFunc(AngleFrom70MaxF_Container))
    table_One['Catch'].append(averageFunc(MinAngles_Container))
    table_One['Finish'].append(averageFunc(MaxAngles_Container))
    table_One['Effective Start'].append(averageFunc(EffectiveStart_Container))
    table_One['Effective End'].append(averageFunc(EffectiveEnd_Container))
    table_One['ArcLength'].append(averageFunc(ArcLength_Container))
    table_One['Effective Length'].append(averageFunc(Effective_Length_Container))
    table_One['% Effective / Arc'].append(averageFunc(Effective_Length_Percent_Container))
    table_One['Catch Slip'].append(averageFunc(CatchSlip_Container))
    table_One['Finish Slip'].append(averageFunc(FinishSlip_Container))

    table_Two['Max Force'].append(averageFunc(Max_Force_Container))
    table_Two['Avg Force'].append(averageFunc(Avg_Force_Container))
    table_Two['Avg / Max Force'].append(averageFunc(AvgMaxForce_Container))
    table_Two['Max Power'].append(averageFunc(Max_Power_Container))
    table_Two['Avg Power'].append(averageFunc(Average_Power_Container))
    table_Two['Avg w/kg'].append(averageFunc(Watt_Per_Kilo_Container))
    table_Two['Min Power'].append(averageFunc(Min_Power_Container))
    table_Two['Variation (min, max)'].append(averageFunc(Variation_Power_Container))
    table_Two['SD'].append(getSD([averageFunc(Max_Power_Container), averageFunc(Average_Power_Container), averageFunc(Min_Power_Container)]))

    # Calculating variation between data.
    table_One['Drive Time'].append(getVariation(DriveTime_Container))
    table_One['Recovery Time'].append(getVariation(RecoveryTime_Container))
    table_One['Rhythm %'].append(getVariation(Rhythm_Contianer))
    table_One['Position of Max F %'].append(getVariation(PositionMaxF_Container))
    table_One['Catch Force Gradient'].append(getVariation(CatchForceGradient_Container))
    table_One['Finish Force Gradient'].append(getVariation(FinishForceGradient_Container))
    table_One['70% Max F'].append(getVariation(Angle70MaxF_Container))
    table_One['Max F'].append(getVariation(AngleMaxF_Container))
    table_One['From 70% Max F'].append(getVariation(AngleFrom70MaxF_Container))
    table_One['Catch'].append(getVariation(MinAngles_Container))
    table_One['Finish'].append(getVariation(MaxAngles_Container))
    table_One['Effective Start'].append(getVariation(EffectiveStart_Container))
    table_One['Effective End'].append(getVariation(EffectiveEnd_Container))
    table_One['ArcLength'].append(getVariation(ArcLength_Container))
    table_One['Effective Length'].append(getVariation(Effective_Length_Container))
    table_One['% Effective / Arc'].append(getVariation(Effective_Length_Percent_Container))
    table_One['Catch Slip'].append(getVariation(CatchSlip_Container))
    table_One['Finish Slip'].append(getVariation(FinishSlip_Container))

    table_Two['Max Force'].append(getVariation(Max_Force_Container))
    table_Two['Avg Force'].append(getVariation(Avg_Force_Container))
    table_Two['Avg / Max Force'].append(getVariation(AvgMaxForce_Container))
    table_Two['Max Power'].append(getVariation(Max_Power_Container))
    table_Two['Avg Power'].append(getVariation(Average_Power_Container))
    table_Two['Avg w/kg'].append(getVariation(Watt_Per_Kilo_Container))
    table_Two['Min Power'].append(getVariation(Min_Power_Container))
    table_Two['Variation (min, max)'].append(getVariation(Variation_Power_Container))
    table_Two['SD'].append('')

    # Calculating Standard Deviation from samples.
    table_One['Drive Time'].append(getSD(DriveTime_Container))
    table_One['Recovery Time'].append(getSD(RecoveryTime_Container))
    table_One['Rhythm %'].append(getSD(Rhythm_Contianer))
    table_One['Position of Max F %'].append(getSD(PositionMaxF_Container))
    table_One['Catch Force Gradient'].append(getSD(CatchForceGradient_Container))
    table_One['Finish Force Gradient'].append(getSD(FinishForceGradient_Container))
    table_One['70% Max F'].append(getSD(Angle70MaxF_Container))
    table_One['Max F'].append(getSD(AngleMaxF_Container))
    table_One['From 70% Max F'].append(getSD(AngleFrom70MaxF_Container))
    table_One['Catch'].append(getSD(MinAngles_Container))
    table_One['Finish'].append(getSD(MaxAngles_Container))
    table_One['Effective Start'].append(getSD(EffectiveStart_Container))
    table_One['Effective End'].append(getSD(EffectiveEnd_Container))
    table_One['ArcLength'].append(getSD(ArcLength_Container))
    table_One['Effective Length'].append(getSD(Effective_Length_Container))
    table_One['% Effective / Arc'].append(getSD(Effective_Length_Percent_Container))
    table_One['Catch Slip'].append(getSD(CatchSlip_Container))
    table_One['Finish Slip'].append(getSD(FinishSlip_Container))

    table_Two['Max Force'].append(getSD(Max_Force_Container))
    table_Two['Avg Force'].append(getSD(Avg_Force_Container))
    table_Two['Avg / Max Force'].append(getSD(AvgMaxForce_Container))
    table_Two['Max Power'].append(getSD(Max_Power_Container))
    table_Two['Avg Power'].append(getSD(Average_Power_Container))
    table_Two['Avg w/kg'].append(getSD(Watt_Per_Kilo_Container))
    table_Two['Min Power'].append(getSD(Min_Power_Container))
    table_Two['Variation (min, max)'].append(getSD(Variation_Power_Container))
    table_Two['SD'].append('')

    return table_One, table_Two, output_data


def get_Crew_Syncronisation(profiles, boat_Data, stroke_Seat, samples=False, sample=1):
    data_Array = {
        'Seat': [],
        'Name': [],
        'Side': [],
        '25% Recov': [],
        '50% Recov': [],
        '75% Recov': [],
        'Hang Start': [],
        'Min Angle': [],
        'Hang End': [],
        'Effective Start': [],
        'Upto 70% Max F': [],
        'Max F': [],
        'From 70% Max F': [],
        'Effective End': [],
        'Pause Start': [],
        'Max Angle': [],
        'Release': [],
        'Syncronisation Average': [],
        'SD': [],
    }

    def sectionFunc(array):
        return Subroutines.section_Data(array, boat_Data)

    avg = Subroutines.calculate_Average
    sd = Subroutines.calcuate_SD

    Stroke_25_Recov = 0
    Stroke_50_Recov = 0
    Stroke_75_Recov = 0
    Stroke_Hang = 0
    Stroke_Min = 0
    Stroke_Catch = 0
    Stroke_Effective_Drive = 0
    Stroke_70Max_F = 0
    Stroke_MaxF = 0
    Stroke_From70Max_F = 0
    Stroke_FSlip = 0
    Stroke_Finish = 0
    Stroke_Max = 0
    Stroke_Recovery = 0

    for rower in profiles:
        if int(rower.Seat) == stroke_Seat:
            if samples:
                Stroke_25_Recov = sectionFunc(rower.data['Time_To_25%'])[sample-1]
                Stroke_50_Recov = sectionFunc(rower.data['Time_To_50%'])[sample-1]
                Stroke_75_Recov = sectionFunc(rower.data['Time_To_75%'])[sample-1]
                Stroke_Hang = sectionFunc(rower.data['Time_To_Hang'])[sample-1]
                Stroke_Min = sectionFunc(rower.data['Time_To_Min'])[sample-1]
                Stroke_Catch = sectionFunc(rower.data['Time_To_Catch'])[sample-1]
                Stroke_Effective_Drive = sectionFunc(rower.data['Time_To_Effective_Start'])[sample-1]
                Stroke_70Max_F = sectionFunc(rower.data['Time_To_70Max'])[sample-1]
                Stroke_MaxF = sectionFunc(rower.data['Time_To_MaxF'])[sample-1]
                Stroke_From70Max_F = sectionFunc(rower.data['Time_To_From70Max'])[sample-1]
                Stroke_FSlip = sectionFunc(rower.data['Time_To_Effective_End'])[sample-1]
                Stroke_Finish = sectionFunc(rower.data['Time_To_Finish'])[sample-1]
                Stroke_Max = sectionFunc(rower.data['Time_To_Max'])[sample-1]
                Stroke_Recovery = sectionFunc(rower.data['Time_To_Recovery'])[sample-1]
            else:
                Stroke_25_Recov = avg(rower.data['Time_To_25%'])
                Stroke_50_Recov = avg(rower.data['Time_To_50%'])
                Stroke_75_Recov = avg(rower.data['Time_To_75%'])
                Stroke_Hang = avg(rower.data['Time_To_Hang'])
                Stroke_Min = avg(rower.data['Time_To_Min'])
                Stroke_Catch = avg(rower.data['Time_To_Catch'])
                Stroke_Effective_Drive = avg(rower.data['Time_To_Effective_Start'])
                Stroke_70Max_F = avg(rower.data['Time_To_70Max'])
                Stroke_MaxF = avg(rower.data['Time_To_Max'])
                Stroke_From70Max_F = avg(rower.data['Time_To_From70Max'])
                Stroke_FSlip = avg(rower.data['Time_To_Effective_End'])
                Stroke_Finish = avg(rower.data['Time_To_Finish'])
                Stroke_Max = avg(rower.data['Time_To_Max'])
                Stroke_Recovery = avg(rower.data['Time_To_Recovery'])

    for rower in profiles:
        if samples:
            Recov_25_Time = sectionFunc(rower.data['Time_To_25%'])[sample-1]
            Recov_50_Time = sectionFunc(rower.data['Time_To_50%'])[sample-1]
            Recov_75_Time = sectionFunc(rower.data['Time_To_75%'])[sample-1]
            Hang_Time = sectionFunc(rower.data['Time_To_Hang'])[sample-1]
            Min_Time = sectionFunc(rower.data['Time_To_Min'])[sample-1]
            Catch_Time = sectionFunc(rower.data['Time_To_Catch'])[sample-1]
            Effective_Drive_Time = sectionFunc(rower.data['Time_To_Effective_Start'])[sample-1]
            MaxF70_Time = sectionFunc(rower.data['Time_To_70Max'])[sample-1]
            MaxF_Time = sectionFunc(rower.data['Time_To_MaxF'])[sample-1]
            MaxFrom70_Time = sectionFunc(rower.data['Time_To_From70Max'])[sample-1]
            FSlip_Time = sectionFunc(rower.data['Time_To_Effective_End'])[sample-1]
            Finish_Time = sectionFunc(rower.data['Time_To_Finish'])[sample-1]
            Max_Time = sectionFunc(rower.data['Time_To_Max'])[sample-1]
            Recovery_Time = sectionFunc(rower.data['Time_To_Recovery'])[sample-1]
        else:
            Recov_25_Time = avg(rower.data['Time_To_25%'])
            Recov_50_Time = avg(rower.data['Time_To_50%'])
            Recov_75_Time = avg(rower.data['Time_To_75%'])
            Hang_Time = avg(rower.data['Time_To_Hang'])
            Min_Time = avg(rower.data['Time_To_Min'])
            Catch_Time = avg(rower.data['Time_To_Catch'])
            Effective_Drive_Time = avg(rower.data['Time_To_Effective_Start'])
            MaxF70_Time = avg(rower.data['Time_To_70Max'])
            MaxF_Time = avg(rower.data['Time_To_Max'])
            MaxFrom70_Time = avg(rower.data['Time_To_From70Max'])
            FSlip_Time = avg(rower.data['Time_To_Effective_End'])
            Finish_Time = avg(rower.data['Time_To_Finish'])
            Max_Time = avg(rower.data['Time_To_Max'])
            Recovery_Time = avg(rower.data['Time_To_Recovery'])

        Recov_25_Difference = round((Recov_25_Time-Stroke_25_Recov),3)
        Recov_50_Difference = round((Recov_50_Time-Stroke_50_Recov),3)
        Recov_75_Difference = round((Recov_75_Time-Stroke_75_Recov),3)
        Hang_Difference = round((Hang_Time-Stroke_Hang),3)
        Min_Difference = round((Min_Time-Stroke_Min),3)
        Catch_Difference = round((Catch_Time-Stroke_Catch),3)
        Effective_Drive_Difference = round((Effective_Drive_Time-Stroke_Effective_Drive),3)
        MaxF70_Difference = round((MaxF70_Time-Stroke_70Max_F),3)
        MaxF_Difference = round((MaxF_Time-Stroke_MaxF),3)
        MaxFrom70_Difference = round((MaxFrom70_Time-Stroke_From70Max_F),3)
        FSlip_Difference = round((FSlip_Time-Stroke_FSlip),3)
        Finish_Difference = round((Finish_Time-Stroke_Finish),3)
        Max_Difference = round((Max_Time-Stroke_Max),3)
        Recovery_Difference = round((Recovery_Time-Stroke_Recovery),3)

        list_of_Differences = [Recov_25_Difference, Recov_50_Difference, Recov_75_Difference, Hang_Difference, Min_Difference, Catch_Difference, Effective_Drive_Difference, MaxF70_Difference, MaxF_Difference, FSlip_Difference, Finish_Difference, Max_Difference, Recovery_Difference]
        
        for data_Name in data_Array:
            data_List = data_Array[data_Name]
            if data_Name == 'Seat':
                data_List.append(rower.Seat)
            elif data_Name == 'Name':
                data_List.append(rower.Name)
            elif data_Name == 'Side':
                data_List.append(rower.Side)
            elif data_Name == '25% Recov':
                data_List.append(Recov_25_Difference)
            elif data_Name == '50% Recov':
                data_List.append(Recov_50_Difference)
            elif data_Name == '75% Recov': 
                data_List.append(Recov_75_Difference)
            elif data_Name == 'Hang Start':
                data_List.append(Hang_Difference)
            elif data_Name == 'Min Angle':
                data_List.append(Min_Difference)
            elif data_Name == 'Hang End': 
                data_List.append(Catch_Difference)
            elif data_Name == 'Effective Start':
                data_List.append(Effective_Drive_Difference)
            elif data_Name == 'Upto 70% Max F':
                data_List.append(MaxF70_Difference)
            elif data_Name == 'Max F':
                data_List.append(MaxF_Difference)
            elif data_Name == 'From 70% Max F':
                data_List.append(MaxFrom70_Difference)
            elif data_Name == 'Effective End': 
                data_List.append(FSlip_Difference)
            elif data_Name == 'Pause Start':
                data_List.append(Finish_Difference)
            elif data_Name == 'Max Angle':
                data_List.append(Max_Difference)
            elif data_Name == 'Release':
                data_List.append(Recovery_Difference)
            elif data_Name == 'Syncronisation Average':
                data_List.append(avg(list_of_Differences))
            elif data_Name == 'SD':
                data_List.append(sd(list_of_Differences))

    return data_Array

def get_Boat_Data(boat_Data, serial):
    data_Array = {
        'Seats': [],
        'Rating': [],
        'Dist/Stroke': [],
        'Distance': [],
        'Avg /w': [],
        'T Strokes': [],
        'Time': [],
        'Serial': [],
    }

    for data_Name in data_Array:
        Data_List = data_Array[data_Name]
        if data_Name == 'Seats':
            Data_List.append(boat_Data.Seats)
        elif data_Name == 'Rating':
            Data_List.append(Subroutines.calculate_Average(boat_Data.data['Rating']))
        elif data_Name == 'Dist/Stroke':
            Data_List.append(Subroutines.calculate_Average(boat_Data.data['Distance / Stroke']))
        elif data_Name == 'Distance':
            Data_List.append(boat_Data.Distance)
        elif data_Name == 'Avg /w':
            Data_List.append(Subroutines.calculate_Average(boat_Data.data['Average Power']))
        elif data_Name == 'T Strokes':
            Data_List.append(boat_Data.tStrokes)
        elif data_Name == 'Time':
            Data_List.append(boat_Data.timeElapsed)
        elif data_Name == 'Serial':
            Data_List.append(serial)
    
    return data_Array