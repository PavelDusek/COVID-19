# coding: utf-8
import json
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

with open('params.json') as f: json_data = f.read()
params = json.loads(json_data)
params
dates, intercept, index = [], [], []
for date, values in params.items():
    if not date.endswith("_for_last_week"):
        dates.append(date)
        intercept.append( values['Intercept'] )
        index.append( values['index'] )
    
param_df = pd.DataFrame( { 'dates': dates, 'intercept': intercept, 'exponent': index } )
sns.scatterplot( x='intercept', y='exponent', data=param_df)

previous_point = np.array([np.nan, np.nan])
for index, row in param_df.iterrows():
    plt.text( row['intercept'] + 0.001, row['exponent'] + 0.001, row['dates'], horizontalalignment='left', size='medium', color='black')
    this_point = np.array( [ row['intercept'], row['exponent'] ] )
    if previous_point.all():
        delta = this_point - previous_point
        x, y = (previous_point)+ 0.125 * delta
        dx, dy = delta * 0.75
        plt.arrow(x, y, dx, dy, fc="gray", ec="gray", width=0.00005, head_width=0.001, head_length=0.002 )
    previous_point = this_point
plt.title("https://github.com/PavelDusek/COVID-19\nCOVID-19 in the Czech Republic\nEvolution of the Exponential Model Parameters by Date")
plt.show()
