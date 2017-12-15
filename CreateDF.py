#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import csv
import matplotlib.pyplot as plt

projects = {}

##DEFINIR PROJETOS E VERSOES
projects['Pandas/'] = ['pandas-0.19.2', 'pandas-0.20.0', 'pandas-0.20.1',
						'pandas-0.20.2', 'pandas-0.20.3', 'pandas-0.21.0',
						'pandas-0.21.1',]
##

for project, versions in projects.iteritems():
	
	df_1 = pd.DataFrame(columns=versions, index=['methods w/ raise', 'methods w/o raise',
								'methods w/o handler', 'methods w/ handler',
								'methods'])
	print project
	for version in versions:

		df_functions = pd.read_csv(project+version+'/Function.csv', sep=';')

		df_1[version] = ([df_functions[df_functions['raise'] > 0]['id'].count(),
		df_functions[df_functions['raise'] == 0]['id'].count(),
		df_functions[df_functions['handlers'] == 0]['id'].count(),
		df_functions[df_functions['handlers'] > 0]['id'].count(),
		df_functions['id'].count()])
	print df_1
	df_1.plot(kind='line', marker='o')
	plt.show()
