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
fig, axrray = plt.subplots(3, 4)
for project in lista:
	projects[project] = sorted(os.listdir(project))

for project, versions in projects.iteritems():
	df_principal = pd.DataFrame(index=projects[project], columns=['raise', 're-raise', 'statements', 'try',
																	'handlers', 'exceptions per handler',
																	'EH Code', 'handler per try', 'PLOC', 'raise sys exception',
																	'raise usr exception', 'reraise sys exception',
																	'reraise usr exception'])
	date = pd.to_datetime(df_principal.index)
	for version in projects[project]:
		df_function = pd.read_csv(os.path.join(project, version, 'Function.csv'), sep=';')
		df_handler = pd.read_csv(os.path.join(project, version, 'Handler.csv'), sep=';')
		df_try = pd.read_csv(os.path.join(project, version, 'Try.csv'), sep=';')
		df_raise = pd.read_csv(os.path.join(project, version, 'Raise.csv'), sep=';')
		df_reraise = pd.read_csv(os.path.join(project, version, 'Reraise.csv'), sep=';')
		df_principal.loc[version] = [df_function['raise'].sum(), df_function['re-raise'].sum(),
										df_function['size'].sum(), df_function['try'].sum(), 
										df_function['handlers'].sum(), df_handler['exceptions'].mean(),
										df_handler['size'].sum(), df_try['handlers'].mean(), df_try['size'].sum(),
										df_raise[df_raise['user/sys'] == 'sys']['user/sys'].count(),
										df_raise[df_raise['user/sys'] == 'usr']['user/sys'].count(),
										df_reraise[df_reraise['user/sys'] == 'sys']['user/sys'].count(),
										df_reraise[df_reraise['user/sys'] == 'usr']['user/sys'].count()]

	df_principal['percentage EH'] = df_principal['EH Code']/df_principal['statements']





	axrray[0][1].plot(date, df_principal['raise'], marker='o', markersize=2, label=project)
	axrray[0][1].set_title('Raising Sites')
	axrray[1][1].plot(date, df_principal['raise sys exception'], marker='o', markersize=2, label=project)
	axrray[1][1].set_title('Number of Raising Sites w/ sys exception')
	axrray[2][1].plot(date, df_principal['raise usr exception'], marker='o', markersize=2, label=project)
	axrray[2][1].set_title('Number of Raising Sites w/ usr exception')
	
	axrray[0][3].plot(date, df_principal['statements'], marker='o', markersize=5, label=project)
	axrray[0][3].set_title('Number of Statements')
	axrray[1][3].plot(date, df_principal['EH Code'], marker='o', markersize=2, label=project)
	axrray[1][3].set_title('Exception Handling Code')
	axrray[2][3].plot(date, df_principal['percentage EH'], marker='o', markersize=2, label=project)
	axrray[2][3].set_title('Percentage of EH Code')
	
	'''
	axrray[2][1].plot(date, df_principal['PLOC'], marker='o', markersize=2, label=project)
	axrray[2][1].set_title('Protected lines of code')
	'''
	axrray[0][0].plot(date, df_principal['handlers'], marker='o', markersize=2, label=project)
	axrray[0][0].set_title('Handling Sites')
	axrray[1][0].plot(date, df_principal['handler per try'], marker='o', markersize=2, label=project)
	axrray[1][0].set_title('Handling Site per try (MEAN)')
	axrray[2][0].plot(date, df_principal['exceptions per handler'], marker='o', markersize=2, label=project)
	axrray[2][0].set_title('Exceptions per handler (MEAN)')
	
	axrray[0][2].plot(date, df_principal['re-raise'], marker='o', markersize=2, label=project)
	axrray[0][2].set_title('Raising Sites inside Handling Site')
	axrray[1][2].plot(date, df_principal['reraise sys exception'], marker='o', markersize=2, label=project)
	axrray[1][2].set_title('Re-raise w/ sys exception')
	axrray[2][2].plot(date, df_principal['reraise usr exception'], marker='o', markersize=2, label=project)
	axrray[2][2].set_title('Re-raise w/ usr exception')
'''
	
	axrray
	axrray[2][1].plot(date, df_principal['raise per line'], marker='o', markersize=5, label=project)
	axrray[2][1].set_title('Number of lines per Raising Sites')
'''

for row in axrray:
	for ax in row:
		# format the ticks
		ax.xaxis.set_major_locator(years)
		ax.xaxis.set_major_formatter(yearsFmt)
		ax.xaxis.set_minor_locator(months)
		#ax.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0., shadow=True)

		datemin = datetime.date(2016, 1, 1)
		datemax = datetime.date(2018, 1, 1)
		ax.set_xlim(datemin, datemax)

		# format the coords message box
		ax.format_xdata = mdates.DateFormatter('%Y-%m-%d')
# rotates and right aligns the x labels, and moves the bottom of the
# axes up to make room for them
fig.autofmt_xdate()
	
#plt.tight_layout()
plt.show()