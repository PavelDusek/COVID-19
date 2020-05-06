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

width, height, my_dpi = 1296, 670, 100

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
#today = "2020-04-08"
try:
    #try for xlsx
    #url = f"https://www.ecdc.europa.eu/sites/default/files/documents/COVID-19-geographic-disbtribution-worldwide-{today}.xlsx"
    url = "https://www.ecdc.europa.eu/sites/default/files/documents/COVID-19-geographic-disbtribution-worldwide-{}.xlsx".format(today)
    df = pd.read_excel(url)
except urllib.error.HTTPError:
    #the file is not xlsx, but xls?
    try:
        #url = f"https://www.ecdc.europa.eu/sites/default/files/documents/COVID-19-geographic-disbtribution-worldwide-{today}.xls"
        url = "https://www.ecdc.europa.eu/sites/default/files/documents/COVID-19-geographic-disbtribution-worldwide-{}.xls".format(today)
        df = pd.read_excel(url)
    except urllib.error.HTTPError:
        try:
            day = datetime.datetime.now()
            day = day + datetime.timedelta(days=-1)
            today = day.strftime("%Y-%m-%d")
            #try for yesterdays date xlsx
            #url = f"https://www.ecdc.europa.eu/sites/default/files/documents/COVID-19-geographic-disbtribution-worldwide-{today}.xlsx"
            url = "https://www.ecdc.europa.eu/sites/default/files/documents/COVID-19-geographic-disbtribution-worldwide-{}.xlsx".format(today)
            df = pd.read_excel(url)
        except urllib.error.HTTPError:
            #the file is not xlsx, but xls?
            try:
                #url = f"https://www.ecdc.europa.eu/sites/default/files/documents/COVID-19-geographic-disbtribution-worldwide-{today}.xls"
                url = "https://www.ecdc.europa.eu/sites/default/files/documents/COVID-19-geographic-disbtribution-worldwide-{}.xls".format(today)
                df = pd.read_excel(url)
            except urllib.error.HTTPError:
                url = "https://www.ecdc.europa.eu/sites/default/files/documents/COVID-19-geographic-disbtribution-worldwide.xlsx"
                df = pd.read_excel(url)
print(url)
df.rename(
       columns={
            'dateRep': 'DateRep',
            'countriesAndTerritories': 'Countries and territories',
            'cases': 'Cases',
            'deaths': 'Deaths',
       }, inplace=True)
df.loc[ df['Countries and territories'] == 'Czechia', 'Countries and territories'] = 'Czech_Republic'

cz = df.loc[ df['Countries and territories'] == 'Czech_Republic' ]
cz = cz.loc[ cz['Cases'] > 0 ]
cz = cz.sort_values(by='DateRep', ascending=True).reset_index()
cz['index'] = cz.index
cz.loc[:, 'cumsum'] = cz.sort_values(by='DateRep', ascending=True)['Cases'].cumsum()
cz.loc[:, 'log'] = np.log( cz['cumsum'] )

model_data = cz.loc[ cz['log'] > 0]
result, params[today] = exponential_model( data=model_data )
model_data_last_week = model_data.loc[ model_data['DateRep'] >= ( datetime.datetime.strptime(today, "%Y-%m-%d") + datetime.timedelta(days=-8) ) ]
result_last_week, params["{}_for_last_week".format(today)] = exponential_model( data=model_data_last_week )


f, ax = plt.subplots( nrows=1, ncols=2, figsize=(width/100, height/100), dpi=my_dpi )
ax[0].plot( model_data['index'], model_data['log'], label='Real Data')
ax[0].plot( model_data['index'], result.predict(model_data['index']), label='Model' )
ax[0].plot( model_data_last_week['index'], result_last_week.predict(model_data_last_week['index']), label='Model for the last week' )
ax[0].text( model_data['index'][0], model_data['log'].max() - 0.5, 'R^2 = {:.2f}'.format( result.rsquared_adj ), color=plt_colors[1] )
ax[0].text( model_data['index'][0], model_data['log'].max() - 0.75, 'Cases = e^( {:.3f} * day + {:.3f} )'.format( result.params['index'], result.params['Intercept'] ), color=plt_colors[1])
ax[0].text( model_data['index'][0], model_data['log'].max() - 1, 'R^2 = {:.2f}'.format( result_last_week.rsquared_adj ), color=plt_colors[2] )
ax[0].text( model_data['index'][0], model_data['log'].max() - 1.25, 'Cases = e^( {:.3f} * day + {:.3f} )'.format( result_last_week.params['index'], result_last_week.params['Intercept'] ), color=plt_colors[2])
ax[0].set_ylabel("Log No. cases")
ax[0].legend()

initdate = datetime.datetime(2020, 3, 1)
texts = {
        datetime.datetime(2020, 3, 7): u"Karanténa cestovatelů z Itálie",
        datetime.datetime(2020, 3, 9): u"Zákaz návštěv v nemocnicích",
        datetime.datetime(2020, 3, 10): u"Zákaz společenských akcí, uzávěr škol",
        datetime.datetime(2020, 3, 12): u"Stav nouze",
        datetime.datetime(2020, 3, 13): u"Karanténa cestovatelů z rizikových zemí",
        datetime.datetime(2020, 3, 14): u"Uzavření obchodů",
        datetime.datetime(2020, 3, 15): u"Zákaz volného pohybu osob",
        datetime.datetime(2020, 3, 18): u"Povinnost ochranných prostředků",
        datetime.datetime(2020, 3, 25): u"Pouze dva lidé spolu",
        datetime.datetime(2020, 3, 30): u"Spuštění chytré karantény",
        datetime.datetime(2020, 4, 6): u"Individuální sportování bez roušek",
        datetime.datetime(2020, 4, 8): u"Otevření obchodů",
        datetime.datetime(2020, 4, 9): u"Upraven režim nošení roušek",
        datetime.datetime(2020, 4, 11): u"Sportování v malých skupinách",
        datetime.datetime(2020, 4, 14): u"Nouzové cestování do zahraničí",
        datetime.datetime(2020, 4, 20): u"Uvolnění řemesla, prodej aut, trhy, sportovci, malé svatby, zkoušky VŠ",
        datetime.datetime(2020, 4, 27): u"Uvolnění malé provozy, autoškoly, fitness, malé bohoslužby, knihovny, ZOO venku",
        datetime.datetime(2020, 5, 11): u"Uvolnění velké provozy, gastronomie venku, kultura, velké bohoslužby, velké svatby",
        datetime.datetime(2020, 5, 25): u"Uvolnění gastronomie uvnitř, hotely, taxi, tábory, cestování",
        datetime.datetime(2020, 6, 1): u"Uvolnění maturity",
}
for date, text in texts.items():
    time_difference = date - initdate
    days = time_difference.days
    ax[0].text( days, 4, text, rotation=90, alpha=0.3 )

ax[0].set_ylim([ 0, ax[0].get_ylim()[1] ])
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
cz['model'] = np.exp( result.params['index'] * cz['index'] + result.params['Intercept'] )
cz['model_last_week'] = np.exp( result_last_week.params['index'] * cz['index'] + result_last_week.params['Intercept'] )
ax[1].plot( cz['DateRep'], cz['model'], label='Model')
ax[1].plot( cz['DateRep'], cz['model_last_week'], label='Model for last week data')

ax[1].set_ylabel("No. cases")
plt.setp( ax[1].xaxis.get_majorticklabels(), rotation=25 )
ax[1].legend()
plt.suptitle("COVID-19 cases, Czech Republic, data from ecdc.europa.eu as of {}\nmodel prediction, code at https://github.com/PavelDusek/COVID-19".format(today))
plt.savefig( 'predict.png', dpi=my_dpi )
plt.savefig( 'predict.svg', dpi=my_dpi )

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
#mortality_rate_mean = 0.034
#mortality_rate_upper = 0.05
#mortality_rate_lower = 0.005

# Data from https://pubmed.ncbi.nlm.nih.gov/32168463/?dopt=Abstract
mortality_rate_mean = 0.008
mortality_rate_upper = 0.03
mortality_rate_lower = 0.0025

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


f = plt.figure( figsize=(width/100, height/100), dpi=my_dpi )
plt.plot('DateRep', 'cumsum', data=cz[['DateRep', 'cumsum']].dropna(), label='Confirmed Cases')
#plt.plot('Date', 'Estim_Cases', data=estim[['Date', 'Estim_Cases']])
plt.fill_between( 'Date', 'Min_Estim_Cases', 'Max_Estim_Cases', alpha=0.2, data=estim, label='Estimated Cases Range')

testy = pd.read_csv("https://onemocneni-aktualne.mzcr.cz/api/v1/covid-19/testy.csv")
testy['datum'] = pd.to_datetime(testy['datum'])
plt.plot('datum', 'testy_celkem', data=testy, label='No. of test performed' )

#plt.suptitle(f"COVID-19 cases, Czech Republic, data from ecdc.europa.eu as of {today}\nEstimation of Real Cases, Based on Mortality Data,\ncode at https://github.com/PavelDusek/COVID-19")
plt.suptitle("COVID-19 cases, Czech Republic, data from ecdc.europa.eu as of {}\nEstimation of Real Cases, Based on Mortality Data,\ncode at https://github.com/PavelDusek/COVID-19".format(today))
plt.xticks(rotation=25)
plt.legend()
#plt.show()
plt.savefig( "estimated_cases.png", dpi=my_dpi )
plt.savefig( "estimated_cases.svg", dpi=my_dpi )

