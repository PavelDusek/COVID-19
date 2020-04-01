# coding: utf-8
import json
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

width, height, my_dpi = 1296, 670, 100
with open('params.json') as f: json_data = f.read()
params = json.loads(json_data)
params
dates, intercept, index, r2, r2_last_week = [], [], [], [], []
for date, values in params.items():
    if not date.endswith("_for_last_week"):
        dates.append(date)
        intercept.append( values['Intercept'] )
        index.append( values['index'] )
        r2.append( values['R2'] )
        r2_last_week.append( np.nan )
    
param_df = pd.DataFrame( { 'dates': dates, 'intercept': intercept, 'exponent': index, 'R2': r2, 'R2_last_week': r2_last_week } )

#fill in the R2 for the "last week model"
for date, values in params.items():
    if date.endswith("_for_last_week"):
        date_ = date.replace("_for_last_week", "")
        param_df.loc[ param_df['dates'] == date_, 'R2_last_week' ] = values['R2']

param_df['R2_last_week'] = param_df['R2_last_week'] * 100 #convert to percent

f = plt.figure( figsize=(width/100, height/100), dpi=my_dpi )
sns.scatterplot(
    x='intercept',
    y='exponent',
    size='Exponential model fit (R2) [%] for last week data',
    data=param_df.rename(columns={'R2_last_week': 'Exponential model fit (R2) [%] for last week data'}),
)

previous_point = np.array([np.nan, np.nan])
for index, row in param_df.sort_values(by='dates').iterrows():
    plt.text( row['intercept'] + 0.001, row['exponent'] + 0.001, row['dates'], horizontalalignment='left', size='medium', color='black')
    this_point = np.array( [ row['intercept'], row['exponent'] ] )
    if previous_point.all():
        delta = this_point - previous_point
        x, y = (previous_point)+ 0.125 * delta
        dx, dy = delta * 0.65
        plt.arrow(x, y, dx, dy, fc="gray", ec="gray", width=0.00005, head_width=0.001, head_length=0.002 )
    previous_point = this_point
plt.title("https://github.com/PavelDusek/COVID-19\nCOVID-19 in the Czech Republic\nEvolution of the Exponential Model Parameters by Date")
plt.ylim( bottom = np.min( param_df['exponent'] ) - 0.01, top = np.max( param_df['exponent'] ) + 0.01 )
plt.xlim( left = np.min( param_df['intercept'] ) - 0.03, right = np.max( param_df['intercept'] ) + 0.07 )
#plt.show()
plt.savefig( 'exponential.png', dpi=my_dpi )
plt.savefig( 'exponential.svg', dpi=my_dpi )
