import requests
import json
import urllib
import zipfile
import os
import csv
from ExceptionPython import *

token = ''

loadExceptions()
mc = metricCalculator()
CONST_MAX = 20

with open('repositorios.csv') as csvfile:
	reader = csv.DictReader(csvfile)
	for row in reader:
		user, repository = row['full_name'].split('/')
		if not os.path.exists(repository):
			request = requests.get('https://api.github.com/repos/'+user+'/'+repository+'/releases', headers={'Authorization': 'token '+token})
			num_of_releases = CONST_MAX
			if request.ok:
				content = json.loads(request.content)
				if len(content) < 2:
					continue
					print 'too few releases' 
				else:
					os.makedirs(repository)
					os.chdir(repository)
					for release in content:
						file_name = release['tag_name']
						print file_name
						urllib.urlretrieve(release['zipball_url'], file_name+'.zip')
						zipdata = zipfile.ZipFile(file_name+'.zip')
						zipdata.extractall()
						print zipdata.namelist()[0]
						os.rename(zipdata.namelist()[0], file_name)
						zipdata.close()
						print file_name
						#os.rename(zipdata.namelist()[0], file_name)
						os.remove(file_name+'.zip')
						#loadHead()
						#mc.run(release['name'].split(' ')[0])
						num_of_releases -= 1
						if num_of_releases == 0:
							break
					os.chdir('../')
					print 'done'
			else:
				print 'error: '+str(request.status_code)
		else:
			print 'already exists'