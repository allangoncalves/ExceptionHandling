import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime
import sys
import os

years = mdates.YearLocator()   # every year
months = mdates.MonthLocator()  # every month
yearsFmt = mdates.DateFormatter('%Y')
##LISTANDO E MUDANDO DIRETORIO
lista = os.listdir('resultados')
os.chdir('resultados')
##

##
projects= {}
fig, axrray = plt.subplots(3)
for project in lista:
	projects[project] = sorted(os.listdir(project))

for project, versions in projects.iteritems():
	df_principal = pd.DataFrame(index=projects[project])
	date = pd.to_datetime(df_principal.index)
	for version in projects[project]:
		df_function = pd.read_csv(os.path.join(project, version, 'Function.csv'), sep=';')
		df_principal.loc[version, 'raise'] = df_function['raise'].sum()
		df_principal.loc[version, 're-raise'] = df_function['re-raise'].sum()
		df_principal.loc[version, 'try'] = df_function['try'].sum()
		df_principal.loc[version, 'handlers'] = df_function['handlers'].sum()
		df_principal.loc[version, 'statements'] = df_function['size'].sum()
	df_principal['raise per line'] = df_principal['statements']/df_principal['raise']
	axrray[0].plot(date, df_principal['raise'], marker='o', markersize=5, label=project)
	axrray[0].set_title('Raising Sites')
	axrray[1].plot(date, df_principal['statements'], marker='o', markersize=5, label=project)
	axrray[1].set_title('Number of Statements')
	axrray[2].plot(date, df_principal['raise per line'], marker='o', markersize=5, label=project)
	axrray[2].set_title('Number of lines per Raising Sites')

for ax in axrray:
	# format the ticks
	ax.xaxis.set_major_locator(years)
	ax.xaxis.set_major_formatter(yearsFmt)
	ax.xaxis.set_minor_locator(months)

	datemin = datetime.date(2017, 1, 1)
	datemax = datetime.date(2018, 1, 1)
	ax.set_xlim(datemin, datemax)

	# format the coords message box
	ax.format_xdata = mdates.DateFormatter('%Y-%m-%d')
	ax.grid(True)
	# rotates and right aligns the x labels, and moves the bottom of the
	# axes up to make room for them
	fig.autofmt_xdate()
	ax.legend(loc='upper left', shadow=True)
plt.tight_layout()
plt.show()