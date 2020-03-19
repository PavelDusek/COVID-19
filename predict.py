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


params = {}
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
model = smf.ols( 'log ~ index', data=model_data )
result = model.fit()
params[today] = {
        'index': result.params['index'],
        'Intercept': result.params['Intercept'],
        'R2': result.rsquared_adj,
        'p_index': result.pvalues['index'],
        'p_Intercept': result.pvalues['Intercept'],
        }

f, ax = plt.subplots( nrows=1, ncols=2 )
ax[0].plot( model_data['index'], model_data['log'], label='Real Data')
ax[0].plot( model_data['index'], result.predict(model_data['index']), label='Model' )
ax[0].text( model_data['index'][0], model_data['log'].max() - 0.5, 'R^2 = {:.2f}'.format( result.rsquared_adj ) )
ax[0].text( model_data['index'][0], model_data['log'].max() - 1, 'Cases = e^( {:.3f} * day + {:.3f} )'.format( result.params['index'], result.params['Intercept'] ) )
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
cz[f'model'] = np.exp( result.params['index'] * cz['index'] + result.params['Intercept'] )
ax[1].plot( cz['DateRep'], cz[f'model'], label=f'Model')
#for day in params.keys():
#    cz[f'model_{day}'] = np.exp( result.params['index'] * cz['index'] + result.params['Intercept'] )
#    ax[1].plot( cz['DateRep'], cz[f'model_{day}'], label=f'Model based on {day} data')

ax[1].set_ylabel("No. cases")
plt.setp( ax[1].xaxis.get_majorticklabels(), rotation=25 )
ax[1].legend()
plt.suptitle(f"COVID-19 cases, Czech Republic, data from ecdc.europa.eu as of {today}\nmodel prediction, code at https://github.com/PavelDusek/COVID-19")
plt.show()

with open("params.json", "w") as f: f.write( json.dumps( params, indent=4, sort_keys=True ) )
