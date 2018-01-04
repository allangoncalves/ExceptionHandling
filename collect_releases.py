import requests
import json
import urllib
import zipfile
import os
import csv
from calculate_metrics import *

token = '050dda8096403012903be8313d4f6e5638993f83'
#loadExceptions()
#mc = metricCalculator()


def download_releases(user, repository, CONST_MAX=-1):
	if not os.path.exists(repository):
		request = requests.get('https://api.github.com/repos/'+user+'/'+repository+'/releases', headers={'Authorization': 'token '+token})
		num_of_releases = CONST_MAX
		if request.ok:
			content = json.loads(request.content)
			if len(content) < 2:
				print 'too few releases' 
				return
			else:
				os.makedirs(repository)
				os.chdir(repository)
				for release in content:
					file_name = release['published_at'].split('T')[0]
					if os.path.exists(file_name):
						continue
					print file_name
					urllib.urlretrieve(release['zipball_url'], file_name+'.zip')
					zipdata = zipfile.ZipFile(file_name+'.zip')
					zipdata.extractall()
					print zipdata.namelist()[0]
					os.rename(zipdata.namelist()[0], file_name)
					zipdata.close()
					os.remove(file_name+'.zip')
					num_of_releases -= 1
					if num_of_releases == 0:
						break
				os.chdir('../')
				print 'done'
		else:
			print 'error: '+str(request.status_code)
	else:
		print 'already exists'

if __name__ == '__main__':

	import sys

	if not os.path.exists('resultados'):
		os.makedirs('resultados')
	os.chdir('resultados')	
	
	if len(sys.argv) < 2:
		with open('../big_repos.csv') as csvfile:
			reader = csv.DictReader(csvfile)
			for row in reader:
				user, repository = row['full_name'].split('/')
				download_releases(user, repository)
	elif len(sys.argv) == 3:
		download_releases(sys.argv[1], sys.argv[2])
	elif len(sys.argv) == 4:
		download_releases(sys.argv[1], sys.argv[2], int(sys.argv[3]))
