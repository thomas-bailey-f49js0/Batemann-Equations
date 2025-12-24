import matplotlib.pyplot as pl
import matplotlib.colors as mcolors
import random
import numpy as np
import pandas as pd
import seaborn as sns
from collections import defaultdict

# Activity of 1kg of 238U is 12.46 MBq or .337 mCi
def generate_random_color():
    return "#{:02x}{:02x}{:02x}".format(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

# colors = [generate_random_color() for _ in range(totalIsotopes)]

# Read in data file and identify where data actually is after header lines
inputfile = open("Data.csv")
headerLine = 0
for i in inputfile.readlines():
    headerLine+=1
    if 'time' in i: break

# Import to pandas dataframe
df = pd.read_csv("Data.csv",header = headerLine-1,dtype = np.float64)
df = df.set_index('time')
def get_base_name(col):
    return col.split('.')[0]
# Group columns by base name
col_map = defaultdict(list)
for col in df.columns:
    base = get_base_name(col)
    col_map[base].append(col)
# Sum Duplciates
summed_df = pd.DataFrame()
for base, cols in col_map.items():
    summed_df[base] = df[cols].sum(axis=1)
# print(summed_df)

# Use Seaborn to plot. Can choose individual columns of summed_df or the whole thing
sns.set_theme()
# sns.lineplot([summed_df['238U'],summed_df['234Th'],summed_df['234Pa'],summed_df['234U']])



scaleToMBq = 12.46/summed_df['238U'].iloc[0]
summed_df = summed_df*scaleToMBq

# sns.lineplot([summed_df['238U'],summed_df['235U'],summed_df['234U'],summed_df['231Pa'],summed_df['230Th']])
# sns.lineplot(summed_df)
# ax = sns.lineplot([summed_df['238U'],summed_df['234Th'],summed_df['234Pa'],summed_df['234U'],summed_df['230Th']])
ax = sns.lineplot([summed_df['238U'],summed_df['234U'],summed_df['235U'],summed_df['236U']])

# Axis options
pl.yscale('log')
# pl.xscale('log')

# Get current x-tick positions (in seconds)
xticks = pl.gca().get_xticks()
# Convert seconds to years
sec_to_year = 1 / 31536000
# These can be useful if you want to plot bh halflives or something similar
# xtick_labels = [f"{tick * sec_to_year:.0f}" for tick in xticks]
# xtick_labels = [i-1 for i in range(8)]

# Set the new tick labels
# pl.gca().set_xticklabels(xtick_labels)
# for i in range(6):
#     pl.axvline((i+1)*15900*31536000,color = 'k')

# Can use this to show when something reaches secular equilibrium
# pl.axhline(3.27E4/7.04E8,color = 'k',label = "Equilibrium Point")


pl.xlabel("Time (years)",fontsize = 24)
pl.ylabel("Mass (kg)",fontsize = 24)
pl.setp(ax.get_legend().get_texts(), fontsize='18') # for legend text

pl.show()
