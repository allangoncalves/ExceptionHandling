import requests
import csv

repos = [['id','full_name','watchers','created_at','updated_at','pushed_at','tags_url','releases_url','collaborators_url','contributors_url','html_url']]

for i in xrange(1, 10):

	response = requests.get('https://api.github.com/search/repositories?q=language:python&sort=watchers&order=desc&page='+str(i)+'&per_page=100')

	if response.ok:
		content = response.json()
		for repo in content['items']:
			repos.append([repo['id'], repo['full_name'], repo['watchers'], repo['created_at'], repo['updated_at'], repo['pushed_at'], repo['tags_url'], repo['releases_url'], repo['collaborators_url'], repo['contributors_url'], repo['html_url']])

with open('big_repos.csv', 'wb') as f:
	writer = csv.writer(f, delimiter=',')
	writer.writerows(repos)
