#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import csv
import matplotlib.pyplot as plt

projects = {}

##DEFINIR PROJETOS E VERSOES
projects['pandas'] = ['0.19.2', '0.20.0', '0.20.1',
						'0.20.2', '0.20.3', '0.21.0',
						'0.21.1',]
##

for project, versions in projects.iteritems():
	
	df_1 = pd.DataFrame(columns=['methods w/ raise', 'methods w/o raise',
								'methods w/o handler', 'methods w/ handler',
								'methods', 'statements'])
	df_2 = pd.DataFrame(columns=['handlers w/ exception', 'handlers w/o exception', 'handlers w/ one',
									'handlers w/ onemore', 'handlers'])
	df_3 = pd.DataFrame(columns=['handler w/ sys', 'handler w/ user', 'unique exceptions', 'unique sys', 'unique users'])
	df_4 = pd.DataFrame(columns=['raising sites', 'raise w/ sys', 'raise w/ user', 'unique raised', 'unique sys', 'unique users'])
	df_5 = pd.DataFrame(columns=['re-raises', 're-raise w/ sys', 're-raise w/ user', 'unique re-raised', 'unique sys', 'unique users'])
	for version in versions:

		df_functions = pd.read_csv(project+'/'+project+'-'+version+'/Function.csv', sep=';')
		df_handler = pd.read_csv(project+'/'+project+'-'+version+'/Handler.csv', sep=';')
		df_exception = pd.read_csv(project+'/'+project+'-'+version+'/Exception.csv', sep=';')
		df_raise = pd.read_csv(project+'/'+project+'-'+version+'/Raise.csv', sep=';')
		df_reraise = pd.read_csv(project+'/'+project+'-'+version+'/Reraise.csv', sep=';')

		##DF FUNCTION.CSV
		df_1.loc[version] = [df_functions[df_functions['raise'] > 0]['id'].count(),
								df_functions[df_functions['raise'] == 0]['id'].count(),
								df_functions[df_functions['handlers'] == 0]['id'].count(),
								df_functions[df_functions['handlers'] > 0]['id'].count(),
								df_functions['id'].count(),
								df_functions['size'].sum()]
								
		##DF FUNCTION.CSV

		##DF HANDLER.CSV
		df_2.loc[version] = [df_handler[df_handler['exceptions'] > 0]['id'].count(),
								df_handler[df_handler['exceptions'] == 0]['id'].count(),
								df_handler[df_handler['exceptions'] == 1]['id'].count(),
								df_handler[df_handler['exceptions'] > 1]['id'].count(),
								df_handler['id'].nunique(),]
		##DF HANDLER.CSV

		##DF EXCEPTION.CSV
		df_3.loc[version] = [df_exception[df_exception['user/sys'] == 'sys']['id_handler'].nunique(),
								df_exception[df_exception['user/sys'] == 'usr']['id_handler'].nunique(),
								df_exception['name'].nunique(),
								df_exception[df_exception['user/sys'] == 'sys']['name'].nunique(),
								df_exception[df_exception['user/sys'] == 'usr']['name'].nunique()]
		##DF EXCEPTION.CSV

		##DF RAISE.CSV
		df_4.loc[version] = [df_raise['name_func'].count(),
								df_raise[df_raise['user/sys'] == 'sys']['name_func'].count(),
								df_raise[df_raise['user/sys'] == 'usr']['name_func'].count(),
								df_raise['name_exception'].nunique(),
								df_raise[df_raise['user/sys'] == 'sys']['name_exception'].nunique(),
								df_raise[df_raise['user/sys'] == 'usr']['name_exception'].nunique(),]
		##DF RAISE.CSV

		##DF RERAISE.CSV
		df_5.loc[version] = [df_reraise['name_func'].count(),
							df_reraise[df_reraise['user/sys'] == 'sys']['name_func'].count(),
							df_reraise[df_reraise['user/sys'] == 'usr']['name_func'].count(),
							df_reraise['exception_name'].nunique(),
							df_reraise[df_reraise['user/sys'] == 'sys']['exception_name'].nunique(),
							df_reraise[df_reraise['user/sys'] == 'usr']['exception_name'].nunique(),]

	
	fig1 = df_1.plot(kind='line', marker='o').get_figure()
	fig2 = df_2.plot(kind='line', marker='o').get_figure()
	fig3 = df_3.plot(kind='line', marker='o').get_figure()
	fig4 = df_4.plot(kind='line', marker='o').get_figure()
	fig5 = df_5.plot(kind='line', marker='o').get_figure()
	fig1.savefig(project+'-methods')
	fig2.savefig(project+'-handler')
	fig3.savefig(project+'-exception')
	fig4.savefig(project+'-raise')
	fig5.savefig(project+'-reraise')
