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
import scipy

cz = pd.DataFrame()
initdate = datetime.datetime(2020, 3, 1)
today = datetime.datetime.now()
datediff = today - initdate
for i in range(datediff.days):
    day = initdate + datetime.timedelta(days=i)
    date = day.strftime("%m-%d-%Y")
    url = f"https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/{date}.csv"
    df = pd.read_csv(url)
    df.loc[ df['Country/Region'] == 'Czech Republic', 'Country/Region'] = 'Czechia'
    df = df.loc[ df['Country/Region'] == 'Czechia' ]
    df.loc[ df['Country/Region'] == 'Czechia', 'date' ] = day
    cz = pd.concat( [cz, df] )
    
population = 10649800
cz['Susceptible'] = population - cz['Confirmed'] - cz['Deaths'] - cz['Recovered']
cz['Infected'] = cz['Confirmed'] - cz['Deaths'] - cz['Recovered']
cz['Removed'] = cz['Deaths'] + cz['Recovered']
#Initial number of infected and recovered individuals, I0 and R0.
I0, R0 = 3, 0
S0 = population - I0 - R0

#beta and gamma according to SIR model from https://www.kaggle.com/lisphilar/covid-19-data-with-sir-model
beta, gamma = 1/5, 1/39
#beta, gamma = 1/5, 1/11
t = np.linspace(0, 159, 160)

def derivative( y, t, population, beta, gamma ):
    S, I, R = y
    dSdt = -beta * S * I / population
    dIdt = beta * S * I / population - gamma * I
    dRdt = gamma * I
    return dSdt, dIdt, dRdt

#Initial condition vector:
y0 = S0, I0, R0
#Integrate the SIR equations over the time grid t
ret = scipy.integrate.odeint( derivative, y0, t, args=(population, beta, gamma) )
S, I, R = ret.T
time = [ initdate + datetime.timedelta(days=i) for i in t ]
plt.plot( time, S, label='Model – Susceptible' )
plt.plot( time, I, label='Model – Infected' )
plt.plot( time, R, label='Model – Removed (Recovered or Death)' )
plt.plot( time[:len(cz)], cz['Infected'], label='Real Data – Infected' )
#plt.plot( time[:len(cz)], cz['Deaths'], label='Real Data – Deaths' )
plt.title( "SIR model for the Czech Republic\n parameters from https://www.kaggle.com/lisphilar/covid-19-data-with-sir-model" )
plt.legend()
plt.show()
