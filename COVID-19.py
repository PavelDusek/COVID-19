# coding: utf-8
import datetime
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import urllib

width, height = 1296, 670
#today = "2020-03-29"
today = datetime.datetime.now().strftime("%Y-%m-%d")
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
df.rename(
       columns={
            'dateRep': 'DateRep',
            'countriesAndTerritories': 'Countries and territories',
            'cases': 'Cases',
            'deaths': 'Deaths',
       }, inplace=True)

selected_countries = [
       #'Afghanistan', 'Albania', 'Algeria', 'Andorra',
       #'Antigua_and_Barbuda', 'Argentina', 'Armenia', 'Australia',
       #'Austria', 'Azerbaijan', 'Bahamas', 'Bahrain', 'Bangladesh',
       #'Belarus', 'Belgium', 'Benin', 'Bhutan', 'Bolivia',
       #'Bosnia_and_Herzegovina', 'Brazil', 'Brunei_Darussalam',
       #'Bulgaria', 'Burkina_Faso', 'Cambodia', 'Cameroon',
       'Canada',
       #'Cases_on_an_international_conveyance_Japan',
       #'Central_African_Republic', 'Chile',
       'China',
       #'Colombia', 'Congo',
       #'Costa_Rica', 'Cote_dIvoire', 'Croatia', 'Cuba', 'Cyprus',
       'Czech_Republic',
       #'Democratic_Republic_of_the_Congo',
       'Denmark',
       #'Dominican_Republic', 'Ecuador', 'Egypt', 'Equatorial_Guinea',
       #'Estonia', 'Eswatini', 'Ethiopia', 'Finland',
       'France',
       #'Gabon',
       #'Georgia',
       'Germany',
       #'Ghana', 'Greece', 'Guatemala', 'Guinea',
       #'Guyana', 'Holy_See', 'Honduras', 'Hungary', 'Iceland', 'India',
       #'Indonesia',
       'Iran',
       #'Iraq', 'Ireland', 'Israel',
       'Italy',
       #'Jamaica', 'Japan', 'Jordan', 'Kazakhstan', 'Kenya', 'Kosovo',
       #'Kuwait', 'Latvia', 'Lebanon', 'Liberia', 'Liechtenstein',
       #'Lithuania', 'Luxembourg', 'Malaysia', 'Maldives', 'Malta',
       #'Mauritania', 'Mexico', 'Moldova', 'Monaco', 'Mongolia', 'Morocco',
       #'Myanmar', 'Namibia', 'Nepal', 'Netherlands', 'New_Zealand',
       #'Nigeria', 'North_Macedonia', 'Norway', 'Oman', 'Pakistan',
       #'Palestine', 'Panama', 'Paraguay', 'Peru', 'Philippines', 'Poland',
       #'Portugal', 'Qatar', 'Romania', 'Russia', 'Rwanda', 'Saint_Lucia',
       #'Saint_Vincent_and_the_Grenadines', 'San_Marino', 'Saudi_Arabia',
       #'Senegal', 'Serbia', 'Seychelles', 'Singapore',
       'Slovakia',
       #'Slovenia', 'Somalia', 'South_Africa', 'South_Korea', 'Spain',
       #'Sri_Lanka', 'Sudan', 'Suriname', 'Sweden', 'Switzerland',
       'Taiwan',
       #'Thailand', 'Togo', 'Trinidad_and_Tobago', 'Tunisia',
       #'Turkey', 'Ukraine', 'United_Arab_Emirates', 'United_Kingdom',
       #'United_Republic_of_Tanzania',
       'United_States_of_America',
       #'Uruguay', 'Uzbekistan', 'Venezuela', 'Vietnam'
   ]

f, ax = plt.subplots( nrows=2, ncols=1, figsize=(width/100, height/100), dpi=100 )
for country in selected_countries:
    country_data = df.sort_values(by='DateRep', ascending=True).loc[ df['Countries and territories'] == country, 'Cases'].cumsum()
    country_data = country_data[ country_data > 0 ]
    ax[0].plot( range( len( country_data ) ), country_data, label=country.replace("_", " ") )
    ax[1].plot( range( len( country_data ) ), country_data, label=country.replace("_", " ") )
#ax[0].set_title(f"COVID-19 cases, selected countries, data from ecdc.europa.eu as of {today}\nTotal Cases vs. Time\nhttps://github.com/PavelDusek/COVID-19")
ax[0].set_title("COVID-19 cases, selected countries, data from ecdc.europa.eu as of {}\nTotal Cases vs. Time\nhttps://github.com/PavelDusek/COVID-19".format(today))
ax[1].set_yscale("log")
ax[1].set_title("Log scale")
ax[0].legend()
ax[1].legend()
ax[0].set_ylabel("No. cases")
ax[1].set_ylabel("No. cases")
ax[1].set_xlabel("days")
#plt.show()
plt.savefig( 'plot.png', dpi=100 )
plt.savefig( 'plot.svg', dpi=100 )

f, ax = plt.subplots( nrows=2, ncols=1, figsize=(width/100, height/100), dpi=100 )
for country in selected_countries:
    country_data = df.sort_values(by='DateRep', ascending=True).loc[ df['Countries and territories'] == country]
    country_data['cumsum'] = country_data['Cases'].cumsum()
    country_data = country_data.loc[ country_data['cumsum'] > 0 ]
    country_data['cumsum_per_100k_inh'] = country_data['cumsum'] / np.max(country_data['popData2018'])
    ax[0].plot( range( len(country_data) ), country_data['cumsum_per_100k_inh'], label=country.replace("_", " ") )
    ax[1].plot( range( len( country_data ) ), country_data['cumsum_per_100k_inh'], label=country.replace("_", " ") )
#ax[0].set_title(f"COVID-19 cases, selected countries, data from ecdc.europa.eu as of {today}\nTotal Cases per 100k Inhabitants vs. Time\nhttps://github.com/PavelDusek/COVID-19")
ax[0].set_title("COVID-19 cases, selected countries, data from ecdc.europa.eu as of {}\nTotal Cases per 100k Inhabitants vs. Time\nhttps://github.com/PavelDusek/COVID-19".format(today))
ax[1].set_yscale("log")
ax[1].set_title("Log scale")
ax[0].legend()
ax[1].legend()
ax[0].set_ylabel("No. cases per 100k inhabitants")
ax[1].set_ylabel("No. cases per 100k inhabitants")
ax[1].set_xlabel("days")
#plt.show()
plt.savefig( 'plot_by_100k_inhabitants.png', dpi=100 )
plt.savefig( 'plot_by_100k_inhabitants.svg', dpi=100 )

#######################
# New vs. Total Cases #
#######################

selected_countries = [
       #'Afghanistan', 'Albania', 'Algeria', 'Andorra',
       #'Antigua_and_Barbuda', 'Argentina', 'Armenia', 'Australia',
       #'Austria', 'Azerbaijan', 'Bahamas', 'Bahrain', 'Bangladesh',
       #'Belarus', 'Belgium', 'Benin', 'Bhutan', 'Bolivia',
       #'Bosnia_and_Herzegovina', 'Brazil', 'Brunei_Darussalam',
       #'Bulgaria', 'Burkina_Faso', 'Cambodia', 'Cameroon',
       #'Canada',
       #'Cases_on_an_international_conveyance_Japan',
       #'Central_African_Republic', 'Chile',
       'China',
       #'Colombia', 'Congo',
       #'Costa_Rica', 'Cote_dIvoire', 'Croatia', 'Cuba', 'Cyprus',
       'Czech_Republic',
       #'Democratic_Republic_of_the_Congo',
       #'Denmark',
       #'Dominican_Republic', 'Ecuador', 'Egypt', 'Equatorial_Guinea',
       #'Estonia', 'Eswatini', 'Ethiopia', 'Finland',
       #'France',
       #'Gabon',
       #'Georgia',
       #'Germany',
       #'Ghana', 'Greece', 'Guatemala', 'Guinea',
       #'Guyana', 'Holy_See', 'Honduras', 'Hungary', 'Iceland', 'India',
       #'Indonesia',
       #'Iran',
       #'Iraq', 'Ireland', 'Israel',
       'Italy',
       #'Jamaica', 'Japan', 'Jordan', 'Kazakhstan', 'Kenya', 'Kosovo',
       #'Kuwait', 'Latvia', 'Lebanon', 'Liberia', 'Liechtenstein',
       #'Lithuania', 'Luxembourg', 'Malaysia', 'Maldives', 'Malta',
       #'Mauritania', 'Mexico', 'Moldova', 'Monaco', 'Mongolia', 'Morocco',
       #'Myanmar', 'Namibia', 'Nepal', 'Netherlands', 'New_Zealand',
       #'Nigeria', 'North_Macedonia', 'Norway', 'Oman', 'Pakistan',
       #'Palestine', 'Panama', 'Paraguay', 'Peru', 'Philippines', 'Poland',
       #'Portugal', 'Qatar', 'Romania', 'Russia', 'Rwanda', 'Saint_Lucia',
       #'Saint_Vincent_and_the_Grenadines', 'San_Marino', 'Saudi_Arabia',
       #'Senegal', 'Serbia', 'Seychelles', 'Singapore',
       'Slovakia',
       #'Slovenia', 'Somalia', 'South_Africa', 'South_Korea', 'Spain',
       #'Sri_Lanka', 'Sudan', 'Suriname', 'Sweden', 'Switzerland',
       'Taiwan',
       #'Thailand', 'Togo', 'Trinidad_and_Tobago', 'Tunisia',
       #'Turkey', 'Ukraine', 'United_Arab_Emirates', 'United_Kingdom',
       #'United_Republic_of_Tanzania',
       'United_States_of_America',
       #'Uruguay', 'Uzbekistan', 'Venezuela', 'Vietnam'
   ]
f = plt.figure( figsize=(width/100, height/100), dpi=100 )
for country in selected_countries:
    country_data = df.sort_values(by='DateRep', ascending=True).loc[ df['Countries and territories'] == country]
    country_data['cumsum'] = country_data['Cases'].cumsum()
    country_data = country_data.loc[ country_data['cumsum'] > 0 ]
    country_data['week_cases'] = country_data.rolling(7)['Cases'].sum()
    plt.plot(
            'Total Number of Cases',
            'New Cases',
            data=country_data.dropna().rename(columns={'cumsum': 'Total Number of Cases', 'week_cases': 'New Cases'}),
            label=country.replace("_", " ") )
plt.yscale("log")
plt.xscale("log")
plt.ylabel("New Cases For Last 7 Days")
plt.xlabel("Total Cases")
#plt.title(f"COVID-19 cases, selected countries, data from ecdc.europa.eu as of {today}\nLogarithmic Scale New vs. Total Cases\nhttps://github.com/PavelDusek/COVID-19")
plt.title("COVID-19 cases, selected countries, data from ecdc.europa.eu as of {}\nLogarithmic Scale New vs. Total Cases\nhttps://github.com/PavelDusek/COVID-19".format(today))
plt.suptitle("")
plt.legend()
plt.savefig( 'plot_new_vs_total.png', dpi=100 )
plt.savefig( 'plot_new_vs_total.svg', dpi=100 )
#plt.show()
