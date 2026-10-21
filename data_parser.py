import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


short_run_cutoff = 14  # days to maturity cutoff for short run bills
year_day_count = 365.25  # days in a year for annualizing yield


# Treasury security price data parser
variable_names = ['CUSIP', 'SECURITY TYPE', 'RATE', 'MATURITY DATE', 'CALL DATE', 'BUY', 'SELL', 'END OF DAY']

df = pd.read_csv('10-14-26_securityprice.csv', header=None, names=variable_names, index_col=False)
df = df.drop(columns=['CALL DATE', 'END OF DAY'])  # no callable bonds in the sample 
df = df[df['SECURITY TYPE'] != 'TIPS']  # filter out TIPS securities
df = df[df['SECURITY TYPE'] != 'MARKET BASED FRN']  # filter out FRNs securities
df = df[(df['BUY'] > 0) & (df['SELL'] > 0)]  # filter out securities with no price data

# confirm data is loaded correctly
print(df.head())

# EDA for which price data to use
print(df.describe())

# # calcualting time to maturity
start_date = pd.to_datetime('10/14/2026')
df['MATURITY DATE'] = pd.to_datetime(df['MATURITY DATE'], errors='coerce')
df['TIME TO MATURITY'] = (df['MATURITY DATE'] - start_date).dt.days

print(df[['TIME TO MATURITY']].describe())

# calculating price (midpoint of buy and sell)
df['PRICE'] = (df['BUY'] + df['SELL']) / 2 

print(df[['PRICE']].describe())

# isolate just bills
bills = df[df['SECURITY TYPE'] == 'MARKET BASED BILL']

# drop very short term bills (less than short_run_cutoff days to maturity)
bills = bills[bills['TIME TO MATURITY'] >= short_run_cutoff].copy()

# finding annulaized yield for each security
bills['ZERO RATE'] = np.log(100 / bills['PRICE']) * (year_day_count / bills['TIME TO MATURITY'])

print(bills.head())

scatterplot = sns.scatterplot(data=bills, x="TIME TO MATURITY", y="ZERO RATE")
plt.title("Zero Rate Curve for Treasury Bills")
plt.xlabel("Time to Maturity (days)")
plt.ylabel("Zero Rate (annualized)")

plt.savefig("Zero_Rate_Curve.png")