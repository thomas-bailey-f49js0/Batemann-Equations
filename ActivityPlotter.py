import matplotlib.pyplot as pl
import matplotlib.colors as mcolors
import random
import numpy as np
import pandas as pd
import seaborn as sns


inputfile = open("Data.csv")

headerLine = 0
for i in inputfile.readlines():
    headerLine+=1
    if 'DecayConstant' in i:
        decayConstants = i.split(',')
        del decayConstants[0]
    if 'time' in i:
        isotopes = i.split(',')
        del isotopes[0]
        break

df = pd.read_csv("Data.csv",header = headerLine-1,dtype = np.float64)
df['time'] = df['time']/24/365.24/3600
df = df.set_index('time')
# print(decayConstants)
for it, i in enumerate(df.columns):
    if decayConstants[it] == "STABLE": df[i]=0
    else: df[i] = float(decayConstants[it])*df[i]*6.022E26/int(i[0:3])*2.7027E-5
    # print(df[i])
sns.set_theme()
# sns.lineplot([df['238U'],df['234U'],df['235U'],df['236U'],df['210Pb']])
# sns.lineplot(df)
sns.lineplot([df['238U'],df['235U'],df['234U'],df['231Pa'],df['230Th']])

# # pl.yscale('log')
# # pl.xscale('log')
pl.xlabel('Time (ya)')
pl.ylabel('Activity ($\mu$Ci)')
pl.show()
