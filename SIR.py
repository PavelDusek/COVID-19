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
#import tensorflow as tf
#tf.enable_eager_execution()

def get_czech_data( url ):
    df = pd.read_csv(url)
    df = df.loc[ df['Country/Region'] == "Czechia" ].reset_index().T
    df.drop(['index', 'Province/State', 'Country/Region', 'Lat', 'Long'], inplace=True)
    df.rename(columns={0: 'data' }, inplace=True)
    df = df.reset_index()
    df['date'] = df['index'].apply( lambda i: datetime.datetime.strptime(i, "%m/%d/%y"))
    df.drop(columns=['index'], inplace=True)
    #df.set_index('date', inplace=True)
    return df

def derivative( y, t, population, beta, gamma ):
    S, I, R = y
    dSdt = -beta * S * I / population
    dIdt = beta * S * I / population - gamma * I
    dRdt = gamma * I
    return dSdt, dIdt, dRdt

def model( beta, gamma ):
    I0, R0 = 3, 0
    S0 = population - I0 - R0
    t = np.linspace(0, 159, 160)
    y0 = S0, I0, R0
    #Integrate the SIR equations over the time grid t
    ret = scipy.integrate.odeint( derivative, y0, t, args=(population, beta, gamma) )
    S, I, R = ret.T
    return np.array([S, I, R])

def loss( x ):
    beta = x[0]
    gamma = x[1]
    predicted = model( beta, gamma )
    predicted = predicted[:, : data.shape[1] ]
    weights = np.array([[1], [1], [1]])
    return np.sum( np.sum( (( data - predicted )**2) * weights ) )

def plot_data( predicted_data, filename ):
    initdate = datetime.datetime(2020, 3, 1)
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    time = [ initdate + datetime.timedelta(days=i) for i in range( predicted_data.shape[1]) ]
    width, height, my_dpi = 1296, 670, 100
    f = plt.figure( figsize=(width/100, height/100), dpi=my_dpi )
    #plt.plot( df['date'], df['S'], label='Real Data – Susceptible')
    plt.plot( df['date'], df['I'], label='Real Data – Infected')
    plt.plot( df['date'], df['R'], label='Real Data – Removed (Recovered or Death)')
    #plt.plot( time, S, label='Model – Susceptible' )
    plt.plot( time, I, label='Model – Infected' )
    plt.plot( time, R, label='Model – Removed (Recovered or Death)' )
    plt.title( "https://github.com/PavelDusek/COVID-19\nSIR model for the Czech Republic\nparameters estimated based on data from {}\nbeta = 1/{:.2f}, gamma = 1/{:.2f}, R0 = {:.2f}".format(today, beta_inv, gamma_inv, r0) )
    plt.legend()
    plt.savefig(filename + '.png', dpi=my_dpi)
    plt.savefig(filename + '.svg', dpi=my_dpi)

population = 10649800
confirmed = get_czech_data( "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv" )
recovered = get_czech_data( "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv" )
deaths    = get_czech_data( "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv" )

confirmed.rename(columns={'data': 'confirmed'}, inplace=True)
recovered.rename(columns={'data': 'recovered'}, inplace=True)
deaths.rename(   columns={'data': 'deaths'   }, inplace=True)

df = pd.merge( left=confirmed, right=recovered, on='date' )
df = pd.merge( left=df, right=deaths, on='date' )
df = df[ ['date', 'confirmed', 'recovered', 'deaths' ] ]
df = df.loc[ df['confirmed'] > 0 ].reset_index().drop(columns=['index'])
df['S'] = population - df['confirmed']
df['R'] = df['recovered'] + df['deaths']
df['I'] = df['confirmed'] - df['R']
data = df[['S', 'I', 'R']].values.T

res = scipy.optimize.minimize(loss, x0=[1/5, 1/39], method='BFGS')#, options={'gtol': 1e-12, 'disp': True})

beta, gamma = res.x
beta_inv, gamma_inv = 1/beta, 1/gamma
r0 = beta/gamma
predicted = model(beta, gamma)

S, I, R = predicted
plot_data(predicted, 'SIR')

predicted = predicted[:, :data.shape[1] + 14 ]
S, I, R = predicted
plot_data(predicted, 'SIR2')
