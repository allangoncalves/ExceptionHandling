import requests
import json
import urllib
import zipfile
import os
from ExceptionPython import *

user = 'scikit-learn'
repository = 'scikit-learn'
num = 6
loadExceptions()
request = requests.get('https://api.github.com/repos/'+user+'/'+repository+'/releases')
releases = []

if request.ok:
	content = json.loads(request.content)
	if not os.path.exists(repository):
		os.makedirs(repository)
	os.chdir(repository)
	for release in content:
		urllib.urlretrieve(release['zipball_url'], repository+'-'+release['name'])
		zipdata = zipfile.ZipFile(repository+'-'+release['name'])
		zipdata.extractall()
		print release['name'].split(' ')[0]
		os.rename(zipdata.namelist()[0], release['name'].split(' ')[0])
		#os.remove(repository+'-'+release['name'])
		loadHead()
		mc = metricCalculator()
		mc.run(release['name'].split(' ')[0])
		num -= 1
		if num == 0:
			break
	print 'done'
