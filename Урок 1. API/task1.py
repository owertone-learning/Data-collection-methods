import requests
import json
from pprint import pprint

url = 'https://api.github.com/user'
repo_url = 'https://api.github.com/user/repos'
username = ''
token = ''

#response = requests.get(url=url, auth=(username, token))
#pprint(response.json())

repos = requests.get(url=repo_url, auth=(username, token))
print(repos.status_code)
repo_dict = {}
repo_dict['repositories'] = []
for repo in repos.json():
    if not repo['private']:
        print(repo['full_name'], repo['html_url'])
        repo_dict['repositories'].append({
            'name': repo['full_name'],
            'url': repo['html_url']
        })
with open('repositories.json', 'w', encoding='utf-8') as f:
    json.dump(repo_dict, f, ensure_ascii=False, indent=2)
print('Данные загружены!')
