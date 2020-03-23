# coding: utf-8
import datetime
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.formula.api as smf
import numpy as np
import urllib
import json
import os.path



def exponential_model( data ):
    model = smf.ols( 'log ~ index', data=data )
    result = model.fit()
    params = {
            'index': result.params['index'],
            'Intercept': result.params['Intercept'],
            'R2': result.rsquared_adj,
            'p_index': result.pvalues['index'],
            'p_Intercept': result.pvalues['Intercept'],
            }
    return ( result, params )

params = {}
plt_colors = plt.rcParams['axes.prop_cycle'].by_key()['color']
if os.path.isfile("params.json"):
    with open("params.json") as f:
        json_params = f.read()
        params = json.loads( json_params )

today = datetime.datetime.now().strftime("%Y-%m-%d")
try:
    #try for xlsx
    url = f"https://www.ecdc.europa.eu/sites/default/files/documents/COVID-19-geographic-disbtribution-worldwide-{today}.xlsx"
    df = pd.read_excel(url)
except urllib.error.HTTPError:
    #the file is not xlsx, but xls?
    url = f"https://www.ecdc.europa.eu/sites/default/files/documents/COVID-19-geographic-disbtribution-worldwide-{today}.xls"
    df = pd.read_excel(url)

cz = df.loc[ df['Countries and territories'] == 'Czech_Republic' ]
cz = cz.loc[ cz['Cases'] > 0 ]
cz = cz.sort_values(by='DateRep', ascending=True).reset_index()
cz['index'] = cz.index
cz.loc[:, 'cumsum'] = cz.sort_values(by='DateRep', ascending=True)['Cases'].cumsum()
cz.loc[:, 'log'] = np.log( cz['cumsum'] )

model_data = cz.loc[ cz['log'] > 0]
result, params[today] = exponential_model( data=model_data )
model_data_last_week = model_data.loc[ model_data['DateRep'] >= ( datetime.datetime.now() + datetime.timedelta(days=-8) ) ]
result_last_week, params[f"{today}_for_last_week"] = exponential_model( data=model_data_last_week )

f, ax = plt.subplots( nrows=1, ncols=2 )
ax[0].plot( model_data['index'], model_data['log'], label='Real Data')
ax[0].plot( model_data['index'], result.predict(model_data['index']), label='Model' )
ax[0].plot( model_data_last_week['index'], result_last_week.predict(model_data_last_week['index']), label='Model for the last week' )
ax[0].text( model_data['index'][0], model_data['log'].max() - 0.5, 'R^2 = {:.2f}'.format( result.rsquared_adj ), c=plt_colors[1] )
ax[0].text( model_data['index'][0], model_data['log'].max() - 0.75, 'Cases = e^( {:.3f} * day + {:.3f} )'.format( result.params['index'], result.params['Intercept'] ), c=plt_colors[1])
ax[0].text( model_data['index'][0], model_data['log'].max() - 1, 'R^2 = {:.2f}'.format( result_last_week.rsquared_adj ), c=plt_colors[2] )
ax[0].text( model_data['index'][0], model_data['log'].max() - 1.25, 'Cases = e^( {:.3f} * day + {:.3f} )'.format( result_last_week.params['index'], result_last_week.params['Intercept'] ), c=plt_colors[2])
ax[0].set_ylabel("Log No. cases")
ax[0].legend()

cz['model'] = np.exp( result.params['index'] * cz['index'] + result.params['Intercept'] )

prediction_length = 8 
predict = pd.DataFrame(
    {
        'DateRep': [ cz.iloc[cz.index.max()]['DateRep'] + datetime.timedelta(i) for i in range(1,prediction_length)],
        'index': range( cz.index.max()+1, cz.index.max() + prediction_length ),
    }
)
predict.set_index('index', inplace=True)
predict['index'] = predict.index
predict['Countries and territories'] = ['Czech_Republic'] * len(predict)
predict['GeoId'] = ['CZ'] * len(predict)
predict['Day'] = predict['DateRep'].apply( lambda d: d.day )
predict['Month'] = predict['DateRep'].apply( lambda d: d.month )
predict['Year'] = predict['DateRep'].apply( lambda d: d.year )

cz = pd.concat( [cz, predict] )
ax[1].plot( cz['DateRep'], cz['cumsum'], label='Real Data')

### Just one model ###
cz[f'model'] = np.exp( result.params['index'] * cz['index'] + result.params['Intercept'] )
cz[f'model_last_week'] = np.exp( result_last_week.params['index'] * cz['index'] + result_last_week.params['Intercept'] )
ax[1].plot( cz['DateRep'], cz[f'model'], label=f'Model')
ax[1].plot( cz['DateRep'], cz[f'model_last_week'], label=f'Model for last week data')
### Model by dates ###
## All dates ##
#for day in params.keys():
## Just first and last day ##
#days = params.keys()
#days = [ min(days), max(days) ]
#for day in days: 
#    cz[f'model_{day}'] = np.exp( result.params['index'] * cz['index'] + result.params['Intercept'] )
#    ax[1].plot( cz['DateRep'], cz[f'model_{day}'], label=f'Model based on {day} data')

ax[1].set_ylabel("No. cases")
plt.setp( ax[1].xaxis.get_majorticklabels(), rotation=25 )
ax[1].legend()
plt.suptitle(f"COVID-19 cases, Czech Republic, data from ecdc.europa.eu as of {today}\nmodel prediction, code at https://github.com/PavelDusek/COVID-19")
plt.show()

with open("params.json", "w") as f: f.write( json.dumps( params, indent=4, sort_keys=True ) )


########################################################
# Estimation of Infected Cases based on Mortality Data #
########################################################
# Method described here: https://medium.com/@tomaspueyo/coronavirus-act-today-or-people-will-die-f4d3d9cd99ca

def round_date( date ):
    year = date.year
    month = date.month
    day = date.day
    if date.hour > 12: day = day + 1
    return datetime.datetime( year, month, day )

# Data from https://medium.com/@tomaspueyo/coronavirus-act-today-or-people-will-die-f4d3d9cd99ca
mortality_rate_mean = 0.034
mortality_rate_upper = 0.05
mortality_rate_lower = 0.005

last_date = max( cz.loc[ cz['Deaths'] == cz['Deaths'].max(), 'DateRep'])
deaths = cz.loc[ cz['DateRep'] == last_date, 'Deaths']
deaths = deaths.values[0]
estimated_date = last_date + datetime.timedelta(days=-17.2)

calculated_date = estimated_date
mean_cases = deaths / mortality_rate_mean
max_cases  = deaths / mortality_rate_lower
min_cases  = deaths / mortality_rate_upper

previous_date = estimated_date + datetime.timedelta(days=-6.2)
estim = pd.DataFrame(columns=['Date', 'Estim_Cases', 'Max_Estim_Cases', 'Min_Estim_Cases'])
estim.loc[ 0 ] = [ previous_date, mean_cases/2, max_cases/2, min_cases/2 ]
while( calculated_date <= last_date ):
    estim.loc[ estim.shape[0] ] = [ calculated_date, mean_cases, max_cases, min_cases ]
    calculated_date = calculated_date + datetime.timedelta(days=+6.2)
    mean_cases = mean_cases * 2
    max_cases = max_cases * 2
    min_cases = min_cases * 2
estim.loc[ estim.shape[0] ] = [ calculated_date, mean_cases, max_cases, min_cases ]
f = plt.figure()
plt.plot('DateRep', 'cumsum', data=cz[['DateRep', 'cumsum']].dropna(), label='Confirmed Cases')
#plt.plot('Date', 'Estim_Cases', data=estim[['Date', 'Estim_Cases']])
plt.fill_between( 'Date', 'Min_Estim_Cases', 'Max_Estim_Cases', alpha=0.2, data=estim, label='Estimated Cases')
plt.suptitle(f"COVID-19 cases, Czech Republic, data from ecdc.europa.eu as of {today}\nEstimation of Real Cases, Based on Mortality Data,\ncode at https://github.com/PavelDusek/COVID-19")
plt.xticks(rotation=25)
plt.legend()
plt.show()
