import pandas as pd

try:
	from src.data_prep import NJPADataLoader
except ModuleNotFoundError:
	from data_prep import NJPADataLoader

dataframe = NJPADataLoader().load()

# First variable I am checking: FTE1 (Full-Time Equivalent) employment 1
# Full-Time Equivalent is a way to statistically combine full-time and part-time headcounts into 
# one number for each store. This is crucial to check because the entire paper is built on this 
# variable and if it is incorrect it will cause a lot of problems later. (DiD, regressions) 
# FTE1 is the first full-time equivalent employment as it is the data collected during the first survey 
# before the minimum wage increase. 
#The formula for FTE is: FTE1 = EMPFT + NMGRS + 0.5*EMPPT
#EMPFT = Full-Time Employee
#EMPPT = Part-Time Employee
#NMGRS = Number of Managers
#Card and Krueger assumed each part-time employee 
# as half a worker and assumed each part time employee contributes about half the labor
#  of a full time employee

#Python Technique I will use to check: Vectorized Column Arithmetic and Groupby
dataframe["FTE1"] = (dataframe["EMPFT"] + dataframe["NMGRS"]) + 0.5 * dataframe["EMPPT"]
#It may look like I am multiplying a list by a number but with pandas a Series allows me to apply an operation to every element inside of it. 
#EMPFT has 6 missing values and EMPPT has 4 (out of 410 stores), so a small number of stores will have FTE1 = NaN. When computing .mean() by state, pandas automatically excludes these missing rows from the average (this is the default skipna=True behavior) rather than treating them as zero.
#Now I must sort my results by state because Card and Kreuger took data from both New Jersey and Pennsylvania (they used Pennsylvania as a control group) 
print(dataframe.groupby("STATE")["FTE1"].mean())
