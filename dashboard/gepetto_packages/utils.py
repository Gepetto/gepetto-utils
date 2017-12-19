from enum import IntEnum

import requests

SOURCES = IntEnum('Source', 'github gitlab redmine robotpkg')


def api_url(repo):
    if repo.source_type == SOURCES.github:
        return f'{repo.api_url}/repos/{repo.package.project.slug}/{repo.package.slug}'
    if repo.source_type == SOURCES.redmine:
        return f'{repo.api_url}/projects/{repo.repo_id}.json'


def api_headers(repo=None, source=None, token=None):
    if repo is not None:
        source = repo.source_type
        token = repo.token
    if source == SOURCES.github:
        return {
            'Authorization': f'token {token}',
            'Accept': 'application/vnd.github.drax-preview+json',
        }
    if source == SOURCES.redmine:
        return {'X-Redmine-API-Key': token}


def api_data(repo, url=''):
    return requests.get(api_url(repo) + url, headers=api_headers(repo)).json()
