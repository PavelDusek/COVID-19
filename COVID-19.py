# coding: utf-8
import datetime
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import urllib

try:
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    url = f"https://www.ecdc.europa.eu/sites/default/files/documents/COVID-19-geographic-disbtribution-worldwide-{today}.xls"
    df = pd.read_excel(url)
except urllib.error.HTTPError:
    today = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime("%Y-%m-%d")
    url = f"https://www.ecdc.europa.eu/sites/default/files/documents/COVID-19-geographic-disbtribution-worldwide-{today}.xls"
    df = pd.read_excel(url)

df.loc[ df['CountryExp'] == 'Czech republic', 'CountryExp'] = 'Czech Republic'
df.loc[ df['CountryExp'] == 'switzerland', 'CountryExp'] = 'Switzerland'
df.loc[ df['CountryExp'] == 'United kingdom', 'CountryExp'] = 'United Kingdom'

selected_countries = [
        #'Afghanistan',
	#'Albania',
	#'Algeria',
	#'Andorra',
	#'Antigua and Barbuda',
	#'Argentina',
	#'Armenia',
	#'Australia',
	'Austria',
	#'Azerbaijan',
	#'Bahrain',
	#'Bangladesh',
	#'Belarus',
	#'Belgium',
	#'Bhutan',
	#'Bolivia',
	#'Bosnia and Herzegovina',
	#'Brazil',
	#'Brunei Darussalam',
	#'Bulgaria',
	#'Burkina Faso',
	#'Cambodia',
	#'Cameroon',
	#'Cases on an international conveyance Japan',
	#'Chile',
	'China',
	#'Colombia',
	#'Costa Rica',
	#'Cote dIvoire',
	#'Croatia',
	#'Cuba',
	#'Cyprus',
	'Czech Republic',
	#'Democratic Republic of the Congo',
	#'Denmark',
	#'Dominican Republic',
	#'Ecuador',
	#'Egypt',
	#'Equatorial Guinea',
	#'Estonia',
	#'Ethiopia',
	#'Finland',
	'France',
	#'Gabon',
	#'Georgia',
	'Germany',
	#'Ghana',
	#'Greece',
	#'Guatemala',
	#'Guinea',
	#'Guyana',
	#'Holy See',
	#'Honduras',
	#'Hungary',
	#'Iceland',
	#'India',
	#'Indonesia',
	#'Iraq',
	#'Ireland',
	#'Israel',
	'Italy',
	#'Jamaica',
	#'Japan',
	#'Jordan',
	#'Kazakhstan',
	#'Kenya',
	#'Kuwait',
	#'Latvia',
	#'Lebanon',
	#'Liechtenstein',
	#'Lithuania',
	#'Luxembourg',
	#'Malaysia',
	#'Maldives',
	#'Malta',
	#'Mauritania',
	#'Mexico',
	#'Moldova',
	#'Monaco',
	#'Mongolia',
	#'Morocco',
	#'Namibia',
	#'Nepal',
	#'Netherlands',
	#'New Zealand',
	#'Nigeria',
	#'North Macedonia',
	#'Norway',
	#'Oman',
	#'Pakistan',
	#'Palestine',
	#'Panama',
	#'Paraguay',
	#'Peru',
	#'Philippines',
	#'Poland',
	#'Portugal',
	#'Qatar',
	#'Romania',
	#'Russia',
	#'Rwanda',
	#'Saint Lucia',
	#'Saint Vincent and the Grenadines',
	#'San Marino',
	#'Saudi Arabia',
	#'Senegal',
	#'Serbia',
	#'Seychelles',
	#'Singapore',
	'Slovakia',
	#'Slovenia',
	#'South Africa',
	#'South Korea',
	#'Spain',
	#'Sri Lanka',
	#'Sudan',
	#'Suriname',
	#'Swaziland',
	#'Sweden',
	'Switzerland',
	#'Thailand',
	#'Togo',
	#'Trinidad and Tobago',
	#'Tunisia',
	#'Turkey',
	#'Ukraine',
	#'United Arab Emirates',
	#'United Kingdom',
	#'United States of America',
	#'Uruguay',
	#'Venezuela',
	#'Vietnam',
	'Canada',
	'Iran',
	'Taiwan',
]

f, ax = plt.subplots( nrows=2, ncols=1 )
for country in selected_countries:
    country_data = df.sort_values(by='DateRep', ascending=True).loc[ df['CountryExp'] == country, 'NewConfCases'].cumsum()
    country_data = country_data[ country_data > 0 ]
    ax[0].plot( range( len( country_data ) ), country_data, label=country )
    ax[1].plot( range( len( country_data ) ), country_data, label=country )
ax[0].set_title(f"COVID-19 cases, selected countries, data from ecdc.europa.eu as of {today}")
plt.suptitle("https://github.com/PavelDusek/COVID-19")
ax[1].set_yscale("log")
ax[1].set_title("Log scale")
ax[0].legend()
ax[1].legend()
ax[0].set_ylabel("No. cases")
ax[1].set_ylabel("No. cases")
ax[1].set_xlabel("days")
plt.show()
