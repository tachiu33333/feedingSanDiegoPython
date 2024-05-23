from datetime import datetime
from datetime import date
import datetime
import pandas as pd
import matplotlib.pyplot as plt
from sklearn import linear_model

#sets up the pages that are going to be used
accomplish = pd.read_excel('accomplishment_2.xlsx', 
                   usecols=['Date', 'Shift', 'Total Boxes Kitted', 
                            'Total Pounds Gleaned', 
                            'Total Pounds of Reclamation', 
                            'Backpack program'], skiprows = [1,2])
golden = pd.read_csv('insight.csv', 
                     usecols=['Current Status', 'Opportunity Name','Opportunity Tags', 'Date', 'Time'], low_memory=False)


#fixes accomplishment
values = {"Total Boxes Kitted": 0, "Total Pounds Gleaned":0, "Total Pounds of Reclamation":0, "Backpack program":0}
accomplish.fillna(value = values, inplace=True)
for i in range(0, len(accomplish)):
    if(type(accomplish.loc[i, "Total Boxes Kitted"]) == str):
        accomplish.loc[i, "Total Boxes Kitted"] = 0
    if(pd.isna(accomplish.at[i, "Date"]) or type(accomplish.at[i, "Date"]) == str):
        accomplish.loc[i, "Date"] = accomplish.loc[i - 1, "Date"]
accomplish["Date"] = pd.to_datetime(accomplish["Date"]).dt.date
accomplish["Shift"] = accomplish["Shift"].str.replace(" ", "")
accomplish['Total Boxes Kitted'] = accomplish['Total Boxes Kitted'].astype(int)


#fixes golden
golden = golden[golden['Current Status'].isin(["Completed"])]
golden = golden.dropna()
golden = golden[golden['Opportunity Tags'].str.contains("food sorting", case = False)]
extras = ["Marketplace", "Pantry", "Driver", "blood drive", "Telethon"]
for i in extras:
    golden = golden[~golden['Opportunity Name'].str.contains(i)]
golden["Date"] = pd.to_datetime(golden["Date"]).dt.date
golden = golden.loc[(golden['Date'] >= datetime.date(2023,1,1))]

#I was too lazy and spent weeks doing this wrong so I did it by hand in the span of 20 minutes.
golden["Time"] = golden["Time"].replace("6:45 AM", "Morning")
golden["Time"] = golden["Time"].replace("7:00 AM", "Morning")
golden["Time"] = golden["Time"].replace("7:30 AM", "Morning")
golden["Time"] = golden["Time"].replace("8:00 AM", "Morning")
golden["Time"] = golden["Time"].replace("8:30 AM", "Morning")
golden["Time"] = golden["Time"].replace("8:45 AM", "Morning")
golden["Time"] = golden["Time"].replace("8:50 AM", "Morning")
golden["Time"] = golden["Time"].replace("9:00 AM", "Morning")
golden["Time"] = golden["Time"].replace("9:30 AM", "Morning")
golden["Time"] = golden["Time"].replace("10:00 AM", "Morning")
golden["Time"] = golden["Time"].replace("10:30 AM", "Morning")
golden["Time"] = golden["Time"].replace("11:00 AM","Afternoon")
golden["Time"] = golden["Time"].replace("12:00 PM","Afternoon")
golden["Time"] = golden["Time"].replace("1:00 PM", "Afternoon")
golden["Time"] = golden["Time"].replace("1:30 PM", "Afternoon")
golden["Time"] = golden["Time"].replace("2:00 PM", "Afternoon")
golden["Time"] = golden["Time"].replace("2:30 PM", "Afternoon")
golden["Time"] = golden["Time"].replace("3:00 PM", "Afternoon")
golden["Time"] = golden["Time"].replace("3:30 PM", "MidAfternoon")
golden["Time"] = golden["Time"].replace("3:50 PM", "MidAfternoon")
golden["Time"] = golden["Time"].replace("3:55 PM", "MidAfternoon")
golden["Time"] = golden["Time"].replace("6:00 PM", "Evening")
golden["Time"] = golden["Time"].replace("6:45 PM", "Evening")
shift = ["Morning", "Mid Afternoon", "Afternoon", "Evening"]

#fixes the rest of accomplishment
for i in range(len(accomplish)):
    golden_copy = golden[golden["Date"] == accomplish["Date"][i]]
    golden_copy = golden_copy[golden_copy["Time"] == accomplish["Shift"][i]]
    accomplish.at[i, "# of volunteers"] = len(golden_copy)


accomplish = accomplish[accomplish["# of volunteers"] != 0]

#makes the sheets
golden.to_excel('GoldenPackage.xlsx', index = False)
accomplish.to_excel('AccomplishmentPackage.xlsx', index = False)


#makes the plots for me
#accomplish.plot(kind = 'scatter', x = '# of volunteers', y = "Total Pounds Gleaned")
#plt.savefig("boxestrial.png")

#seperate plot
#plt.scatter(accomplish['# of volunteers'],accomplish['Total Pounds Gleaned'], color = 'lightcoral')
#plt.title('# of volunteers vs Total Pounds Gleaned')
#plt.ylabel('Total Pounds Gleaned')
#plt.xlabel('# of volunteers')
#plt.box(False)
#plt.show()

#sets up total
#print(accomplish["Total Boxes Kitted"].sum())


#accomplishment stats
print(accomplish.describe())

X = accomplish[['Total Pounds Gleaned', 'Total Boxes Kitted', 'Total Pounds of Reclamation', 'Backpack program']]
y = accomplish['# of volunteers']

regr = linear_model.LinearRegression()
regr.fit(X, y)

#predict the # of volunteer base on the number of gleaned, reclaimed, kitted, and backpacks:
predictedCO2 = regr.predict([[4000, 0, 0, 200]])

print(predictedCO2)
print(regr.coef_)