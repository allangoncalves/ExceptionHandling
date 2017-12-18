import requests
import json
import urllib
import zipfile
import os
import csv
from ExceptionPython import *


loadExceptions()
mc = metricCalculator()

with open('repositorios.csv') as csvfile:
	reader = csv.DictReader(csvfile)
	for row in reader:
		user, repository = row['full_name'].split('/')
		num_of_releases = 6		
		request = requests.get('https://api.github.com/repos/'+user+'/'+repository+'/releases')
		
		##LOADING
		if request.ok:
			content = json.loads(request.content)
			if not os.path.exists(repository):
				os.makedirs(repository)
			os.chdir(repository)
			for release in content:
				urllib.urlretrieve(release['zipball_url'], repository+'-'+release['name'])
				zipdata = zipfile.ZipFile(repository+'-'+release['name'])
				zipdata.extractall()
				zipdata.close()
				print release['name'].split(' ')[0]
				os.rename(zipdata.namelist()[0], release['name'].split(' ')[0])
				os.remove(repository+'-'+release['name'])
				#loadHead()
				#mc.run(release['name'].split(' ')[0])
				num_of_releases -= 1
				if num_of_releases == 0:
					break
			print 'done'
		else:
			print 'error requesting: '+ repository