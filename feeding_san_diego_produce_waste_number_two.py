
import pandas as pd

#mostly cleaning data from the volunteer data list
df = pd.read_csv('new_volunteer_data.csv', low_memory=False)
#extra 1 remove to see rest of data.
#62 last columns were removed due to absolutely no data being there and can be answered by other columns.
df.drop(columns=df.columns[-64:],axis=1,inplace=True)
df.drop(columns=df.columns[:2], axis=1,inplace=True)
df.drop(columns=df.columns[1:9], axis=1,inplace=True)
df.drop(columns=df.columns[2:17], axis=1,inplace=True)

#ensures all the participants have actualy done
df = df[df["Current Status"] == "Completed"]
df = df[df["Opportunity Tags"].str.contains("Food Sorting", case = False, na=False)]


df.drop(["Opportunity Tags","Current Status"], axis = 1, inplace = True)



column_trial = df.loc[:,"Time"]

#column_trial = column_trial.astype(str)

#
column_trial = pd.to_datetime(column_trial).dt.hour

def categorize_time(t):
    if t < 13:
        return 'morning'
    elif t < 16:
        return 'afternoon'
    else:
        return 'evening'


df['Shift'] = column_trial.apply(categorize_time)

df_pivoted = df.pivot_table(index='Date', columns='Shift', values='Volunteer ID', aggfunc='count')

print(df_pivoted)
# with that, we finished the volunteer set up.
    #if possible add in the value of other organizations in how they affect the gleaning process.


a = pd.read_excel("2024.06 June Waste Log.xlsx", sheet_name= 0)
print(a.iloc[:,5])