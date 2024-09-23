import os
import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt

#Creating Bold Graph Edges and Fonts
plt.rcParams["font.weight"] = "bold"
plt.rcParams["axes.labelweight"] = "bold"
plt.rcParams["axes.linewidth"] = 1.5
plt.rcParams["axes.titleweight"] = "bold"
plt.rcParams["axes.titlesize"] = 14

#Defining paths
rootPath = os.path.join(Path.home(), "Bishal")
cleanedFolder = os.path.join(rootPath, "Babu", "Cleaned")
filePath = os.path.join(cleanedFolder, "Dumre.csv")
os.makedirs(cleanedFolder, exist_ok=True)


df = pd.read_csv(filePath)

df["Si_ref_058_delta"] = (df["Irradiance_after_Irrad Si-Ref 058"]
			- df["Irradiance_before_Irrad Si-Ref 058"])

df = df.query("-3 < Si_ref_058_delta < 3")
df = df.query("days_on_sun > 0")
df
df["Irrad_Si_Ref_058"] = df["Irradiance_before_Irrad Si-Ref 058"]
df['Eff'] = (df['PeakPower']/df["Irrad_Si_Ref_058"])/0.00022046

df1 = df.query('850 < Irrad_Si_Ref_058 < 950')
df2 = df.query('500 < Irrad_Si_Ref_058 < 600')

plt.figure()
plt.scatter(df1['days_on_sun'], df1['Eff'], c=df1['Temperature_R'], cmap='inferno', marker = 'x', s = 20, linewidth=0.5, label = '(850-950)W/m$\mathregular{^2}$')
plt.scatter(df2['days_on_sun'], df2['Eff'], c=df2['Temperature_R'], cmap='inferno', marker = '+', s = 20, linewidth=0.5, label = '(500-600)W/m$\mathregular{^2}$')
#plt.scatter(df1['days_on_sun'], df1['Eff'], c='b', marker = 'x', s = 20, linewidth=0.5, label = '(850-950)W/m$\mathregular{^2}$')
#plt.scatter(df2['days_on_sun'], df2['Eff'], c='r', marker = '+', s = 20, linewidth=0.5, label = '(500-600)W/m$\mathregular{^2}$')
plt.colorbar(label='Temperature')
plt.legend(loc='upper left', bbox_to_anchor=(0.15, 1.1), fontsize=8, frameon = False, columnspacing=1.25,handlelength=3, ncols = 2)
plt.text(0.55, 1.085, "Efficiency Evolution over Time", ha="center", va="bottom", fontsize = 19, fontweight = 'bold', transform=plt.gca().transAxes)
plt.ylabel('Efficiency (%)', fontsize = 15)
plt.xlabel('Number of Days', fontsize = 15)
plt.grid('on')
plt.xticks(rotation='vertical', fontsize = 8)
plt.tight_layout()
plt.savefig('EffVSdays.png')
plt.close()
