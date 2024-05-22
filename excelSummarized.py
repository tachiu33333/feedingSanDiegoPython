import datetime
import pandas as pd
import time
import matplotlib.pyplot as plt
df = pd.read_excel('FullSheet.xlsx')
roll = df["# of mesh bags"]
weight = df["Total Weight"]
kit = df["Total kits and backpacks"]
shifts = 583
total_rolls = 192000/roll.sum()*26
total_weight = weight.sum().sum()
total_kit = kit.sum().sum()
df_dict = {"Total rolls": [float(total_rolls)],"Total Weight":[float(total_weight)], 
           "Total number of kits/backpacks": [float(total_kit)], "average rolls": [float(total_rolls/shifts)],
           "Average Weight": [float(total_weight/shifts)], "Average kit/backpacks": [float(total_kit/shifts)]}

ref = pd.DataFrame.from_dict(df_dict)
ref.to_excel('Summary.xlsx', index = False)

#efficiency of certain days/shift