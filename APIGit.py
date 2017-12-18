import requests
import json
import urllib
import zipfile
import os
import csv
from ExceptionPython import *

token = 'cc49dcd22f1a1ff477de75e5b7b4fcf6be67d737'

loadExceptions()
mc = metricCalculator()

with open('repositorios.csv') as csvfile:
	reader = csv.DictReader(csvfile)
	for row in reader:
		user, repository = row['full_name'].split('/')
		num_of_releases = 6		
		request = requests.get('https://api.github.com/repos/'+user+'/'+repository+'/releases', headers={'Authorization': 'token '+token})
		
		if request.ok:
			content = json.loads(request.content)
			if not os.path.exists(repository):
				os.makedirs(repository)
			os.chdir(repository)
			for release in content:
				urllib.urlretrieve(release['zipball_url'], release['tag_name']+'.zip')
				zipdata = zipfile.ZipFile(release['tag_name']+'.zip')
				zipdata.extractall()
				print zipdata.namelist()[0]
				os.rename(zipdata.namelist()[0], release['tag_name'])
				zipdata.close()
				print release['tag_name']
				#os.rename(zipdata.namelist()[0], release['tag_name'])
				os.remove(release['tag_name']+'.zip')
				#loadHead()
				#mc.run(release['name'].split(' ')[0])
				num_of_releases -= 1
				if num_of_releases == 0:
					break
			os.chdir('../')
			print 'done'
		else:
			print request.status_code
		break