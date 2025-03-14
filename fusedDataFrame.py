from datetime import datetime
from datetime import date
import datetime
import pandas as pd
import matplotlib.pyplot as plt
from sklearn import linear_model
from statistics import linear_regression

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
    #if len(golden_copy)
    if len(golden_copy) < 15:
        accomplish.at[i, "# of volunteers"] = "Small"
    elif len(golden_copy) < 30:
        accomplish.at[i, "# of volunteers"] = "Medium"
    else:
        accomplish.at[i, "# of volunteers"] = "Large"

#print(len(accomplish))
#accomplish = accomplish[accomplish["# of volunteers"] > 14]
print(len(accomplish[accomplish["# of volunteers"] == "Small"]))
#print(len(accomplish))
#accomplish = accomplish[accomplish["# of volunteers"] < 30]
#print(len(accomplish))
#accomplish = accomplish[accomplish['Total Pounds Gleaned'] != 0]
#accomplish = accomplish[accomplish['Total Boxes Kitted'] != 0]
#accomplish = accomplish[accomplish['Total Pounds of Reclamation'] != 0]
#accomplish = accomplish[accomplish['Backpack program'] != 0]

#makes the sheets
golden.to_excel('GoldenPackage.xlsx', index = False)
accomplish.to_excel('AccomplishmentPackage.xlsx', index = False)


#makes the plots for me
#accomplish.plot(kind = 'scatter', x = '# of volunteers', y = "Total Pounds Gleaned")
#plt.savefig("gleantrial.png")

#accomplish.plot(kind = 'scatter', x = '# of volunteers', y = 'Total Boxes Kitted')
#plt.savefig("boxestrial.png")

#accomplish.plot(kind = 'scatter', x = '# of volunteers', y = 'Total Pounds of Reclamation')
#plt.savefig("reclaimtrial.png")

#accomplish.plot(kind = 'scatter', x = '# of volunteers', y = 'Backpack program')
#plt.savefig("backpacktrial.png")



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
#print(accomplish.describe())


#predict the # of volunteer base on the number of gleaned, reclaimed, kitted, and backpacks:
#X = accomplish[['Total Pounds Gleaned', 'Total Boxes Kitted', 'Total Pounds of Reclamation', 'Backpack program']]
#X = accomplish[['Total Pounds Gleaned']]
#y = accomplish['# of volunteers']

#regr = linear_model.LinearRegression()
#regr.fit(X, y)

#predictedCO2 = regr.predict([[4000, 0, 0, 400]])
#predictedCO2 = regr.predict([[4000]])

#print(predictedCO2)
#print(regr.coef_)

#predict the # of volunteer base on the number of gleaned, reclaimed, kitted, and backpacks:
#A = accomplish[['Total Pounds Gleaned']]
#b = accomplish['# of volunteers']

#regre = linear_model.LinearRegression()
#regre.fit(A, b)

#predictedCO = regre.predict([[100]])

#print(predictedCO)
