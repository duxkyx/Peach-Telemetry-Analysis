# Peach Telemetry data analysis program | Developed by Ben Loggie
# This program file will export all the data calculated form initialize.py to a excel format.

from Modules import sort_Data
import pandas as pd

def generate_Excel(profiles_List, boat_Data, file_Name, serial):
    Wattage = pd.DataFrame(sort_Data.get_Wattage(profiles_List, 8))
    StrokeTiming = pd.DataFrame(sort_Data.get_Stroke_Timing(profiles_List))
    StrokeTimingPercentage = pd.DataFrame(sort_Data.get_Percentage_Stroke_Timing(profiles_List))
    Angles = pd.DataFrame(sort_Data.get_Angles_Data(profiles_List))
    PowerPercentage = pd.DataFrame(sort_Data.get_Power_Percentage(profiles_List, 8))
    Boat_Data_Frame = pd.DataFrame(sort_Data.get_Boat_Data(boat_Data, serial))

    directory = 'Storage/Excel/' + file_Name + '.xlsx'
    
    with pd.ExcelWriter(directory) as writer:
        Boat_Data_Frame.to_excel(writer, 'Information', index=False)
        StrokeTiming.to_excel(writer, 'Stroke Timing', index=False)
        StrokeTimingPercentage.to_excel(writer, '% Stroke Timing', index=False)
        Angles.to_excel(writer, 'Angles', index=False)
        Wattage.to_excel(writer, 'Wattage', index=False)
        PowerPercentage.to_excel(writer, '% of Total Power', index=False)

    return directory

    