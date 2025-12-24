import pandas as pd
import numpy as np
import math

years = 24*365.24*3600
days = 24*3600

NPoints = 1000
logTime = False

# Values of interest:
# Age of earth: 4.54 billion years
# Age of Uranium: 5.94 billion years (rough calculation in Mathematica)

# Only for Logtime.
# time to start simulation in seconds ago
startTime = 10*years
# can Do smaller time steps towards the start of the simulation for better accuracy
midTime = 2*years
# time to stop simulation
stopTime = 1

# Toggle to print results as an activity rather than mass
# Useful for making plots to show different equilibria
printActivity = False
printYears = True

# Generate the time axis with NPoints in between each point here, e.g can make
# [1 second, 1 day, 100 days, 1 year, 10 years, 1000 years, 1E10 years]
# and the time array will be Npoints between each of those steps
timePoints = [1,1*days,1*years,50*years,1000*years,1E6*years,1E8*years,4.54E9*years]
timePoints = sorted(timePoints)
# Generates log timescale in seconds if logTime true.
if logTime: timeArr = np.logspace(np.log10(stopTime),np.log10(startTime), num = NPoints+1)
else:
    timeArr = np.linspace(timePoints[0],timePoints[1],NPoints+1)
    for it in range(len(timePoints)-2):
        timeArr = np.append(timeArr,np.linspace(timePoints[it+1],timePoints[it+2],NPoints+1))

# Open the decay info to generate the chains
df = pd.read_csv("DecayInfo.csv",sep=r'\s*,\s*',engine = 'python')
inputfile = open("input.txt")
outputfile = open("Data.csv",'w')

# Gotta love a bunch of lists
isotopes = []
elements = []
masses = []
daughters = []

# Read the input file
inputs = 0
outputfile.write("File generated from the following inputs:\n")
outputfile.write("# isotope Symbol mass(kg)\n")
for i in inputfile.readlines():
    if i[0] == '#': continue
    params = i.split()
    isotopes.append(int(params[0]))
    elements.append(params[1])
    masses.append(float(params[2]))
    inputs+=1
    outputfile.write(i)

for i in range(inputs):
    Z = df.loc[df['symbol'] == elements[i], 'Z'].iloc[0]
    N = isotopes[i]-int(Z)
    singleDf = df[(df['symbol']==elements[i]) & (df['N']==N)]
    decayMode = singleDf["decaymode"].iloc[0]
    daughters.append([[N+Z,singleDf["symbol"].iloc[0],0.693/float(singleDf["half_life_s"].iloc[0]),masses[i]]])
    while(True):
        # Go down decay chain until we reach a stable element
        if decayMode == 'STABLE': break
        elif decayMode == 'A':
            Z-=2
            N-=2
        elif decayMode == 'B-':
            N-=1
            Z+=1
        elif 'EC+B+':
            N+=1
            Z+=1
        else:
            print("Unkown Decay Mode: {}, exiting".format(decayMode))
            exit()
        singleDf = df[(df['Z']==Z) & (df['N']==N)]
        decayMode = singleDf["decaymode"].iloc[0]
        symbol = singleDf["symbol"].iloc[0]
        daughters[i].append([N+Z,singleDf["symbol"].iloc[0],0.693/float(singleDf["half_life_s"].iloc[0]),0])
totalIsotopes = 0
for i in daughters:
    totalIsotopes += len(i)
outputfile.write("All daughters to be considered: {}".format(totalIsotopes))
# outputfile.write("\ndecayConstant")
# for i in daughters:
#     for j in i:
#         outputfile.write(",{:.4E}".format(j[2]))
outputfile.write(",\nDecayConstant")
for i in daughters:
    for j in i:
        if j[2]<1E-50:outputfile.write(",STABLE")
        else:outputfile.write(",{}".format(j[2]))

outputfile.write(",\ntime")
for i in daughters:
    for j in i:
        outputfile.write(",{}{}".format(j[0],j[1]))

outputfile.write("\n")
oldTime=0
# loop over all time points
if printYears: print("Time being given in years")
else: print("Time beeing given in Seconds")
if printActivity: print("Results are given as activities")
else: print("Results are given as masses")
for it, time in enumerate(timeArr):
    # print(time)
    # First column in output file is the time point
    if printYears: outputfile.write("{}".format(timeArr[it]/years))
    else: outputfile.write("{}".format(timeArr[it]))
    # Each input has it's own list of all elements in the decay chain
    # len(daughters) = number of input lines
    for itInput, inputDaughter in enumerate(daughters):
        # print(inputDaughter)
        # Initialize array for time step for all daughters in one decay chain
        NAtoms = [0 for i in inputDaughter]
        for itDaughter, Daughter in enumerate(inputDaughter):
            # Determine first product term in general solution (over ever parent generation decay constants)
            prod1 = 1
            for i in range(itDaughter):
                prod1*=inputDaughter[i][2]
            # Determine sum term in solution
            sum1 = 0
            for i in range(itDaughter+1):
                prod2 = 1
                for j in range(itDaughter+1):
                    if i == j:
                        continue
                    prod2 *= (inputDaughter[j][2]-inputDaughter[i][2])
                sum1+=(math.exp(-1*inputDaughter[i][2]*time)/prod2)
            # store result as either activity or mass for one isotope on decay chain
            if printActivity: NAtoms[itDaughter]=masses[itInput]*prod1*sum1*Daughter[2]
            else:NAtoms[itDaughter]=masses[itInput]*prod1*sum1
        # Write the results of this time step
        for N in NAtoms:
            outputfile.write(",{:.7E}".format(N))
    outputfile.write('\n')
