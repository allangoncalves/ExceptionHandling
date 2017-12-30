import requests
import json
import urllib
import zipfile
import os
import csv
from calculate_metrics import *

token = '050dda8096403012903be8313d4f6e5638993f83'
CONST_MAX = 100
#loadExceptions()
#mc = metricCalculator()


def download_releases(user, repository):
	if not os.path.exists(repository):
		##SEND A GET REQUEST FOR THE GITHUB API
		request = requests.get('https://api.github.com/repos/'+user+'/'+repository+'/tags', headers={'Authorization': 'token '+token})
		num_of_tags = CONST_MAX
		if request.ok:
			content = json.loads(request.content)
			if len(content) < 2:
				return
				print 'too few tags' 
			else:
				os.makedirs(repository)
				os.chdir(repository)
				for tag in content:
					
					##GET INFO FROM THE COMMIT
					request2 = requests.get(tag['commit']['url'])
					if request2.ok:
						content2 = json.loads(request2.content) 
						file_name = content2['commit']['committer']['date'].split('T')[0]
					else:
						return
					###

					##GET ONLY THE LAST COMMIT FROM THE DAY
					if os.path.exists(file_name):
						continue
					###

					##DOWNLOAD AND EXTRACT THE FILES
					print file_name
					urllib.urlretrieve(tag['zipball_url'], file_name+'.zip')
					zipdata = zipfile.ZipFile(file_name+'.zip')
					zipdata.extractall()
					print zipdata.namelist()[0]
					os.rename(zipdata.namelist()[0], file_name)
					zipdata.close()
					os.remove(file_name+'.zip')
					###

					##LIMITS THE NUMBER OF TAGS
					num_of_tags -= 1
					if num_of_tags == 0:
						break
					###
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
