# Batemann-Equations
Calculator for buildup of decay products using general analytical solution of the Batemann Equations

This collection of programs was made to make plots showing decays and buildups of actinides
Made by Thomas Bailey in 2025
The main programs is the AnalyticalAbundances.py file. It allows for Daughters to
have an initial abundance, but doesn't take that into account during
calculations. Instead each daughter that has an inital abundance has a
decay chain that it starts and during plotting the total abundance of any
duplicate isotopes are summed. I've also added two toggles, one where the
time written will be in years rather than seconds and one where the data
will be written as activities rather than masses. The Activities toggle is 
useful for showing when various pairs are in secular or transient equilibrium

Note that none of these have any branching ratios implemented and assume 100% to
the dominant mode. (Which is a pretty decent approximation for most of these and
certainly good enough for anything I've ever cared about)

Each one of these takes 2 input files.
   1. The first is a user defined input.txt. Comments in it are pretty straight
      forward. You can use # to comment out any input lines
   2. DecayInfo.csv File generated from I think NNDC. Contains all of the
      for lead through uranium. If you want to get a new file with more elements
      then you will need to go in and manually change the half life associated
      with each instance of STABLE for the decay mode. I make their half lives
      1E100 seconds and call it a day.

Finally there is the plotting program called ActivityPlotter.py. This program loads the
Output file (Data.csv) into a pandas dataframe. It will sum duplicate columns to
account for the possibility of daughters having an initial abundance.

This was originally made to generate plots for my PhD Thesis and defense presentation
