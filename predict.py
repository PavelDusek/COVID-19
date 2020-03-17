# coding: utf-8
import datetime
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.formula.api as smf
import numpy as np

today = datetime.datetime.now().strftime("%Y-%m-%d")
url = f"https://www.ecdc.europa.eu/sites/default/files/documents/COVID-19-geographic-disbtribution-worldwide-{today}.xlsx"
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

f, ax = plt.subplots( nrows=1, ncols=2 )
ax[0].plot( model_data['index'], model_data['log'], label='Real Data')
ax[0].plot( model_data['index'], result.predict(model_data['index']), label='Model' )
ax[0].text( model_data['index'][0], model_data['log'].max() - 0.5, 'R^2 = {:.2f}'.format( result.rsquared_adj ) )
ax[0].text( model_data['index'][0], model_data['log'].max() - 1, 'Cases = e^( {:.3f} * day + {:.3f} )'.format( result.params['index'], result.params['Intercept'] ) )
ax[0].set_ylabel("Log No. cases")
ax[0].legend()

cz['model'] = np.exp( result.params['index'] * cz['index'] + result.params['Intercept'] )

predict = pd.DataFrame(
    {
        'DateRep': [ cz.iloc[cz.index.max()]['DateRep'] + datetime.timedelta(i) for i in range(1,8)],
        'index': range( cz.index.max()+1, cz.index.max() + 8 ),
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
cz['model'] = np.exp( result.params['index'] * cz['index'] + result.params['Intercept'] )


ax[1].plot( cz['DateRep'], cz['Cases'], label='Real Data')
ax[1].plot( cz['DateRep'], cz['model'], label='Model')
ax[1].set_ylabel("No. cases")
plt.setp( ax[1].xaxis.get_majorticklabels(), rotation=25 )
ax[1].legend()

plt.suptitle(f"COVID-19 cases, Czech Republic, data from ecdc.europa.eu as of {today}\nmodel prediction, code at https://github.com/PavelDusek/COVID-19")
plt.show()
