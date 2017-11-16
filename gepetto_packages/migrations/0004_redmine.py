# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-14 09:29
from __future__ import unicode_literals

from os.path import expanduser

from django.db import migrations

import requests

REDMINE_APIS = [
    'https://redmine.laas.fr',
    # 'https://git.openrobots.org',
]
with open(expanduser('~/.redminetoken')) as f:
    TOKEN = f.read().strip()
HEADERS = {
    'X-Redmine-API-Key': TOKEN,
}
PACKAGES = [
    'openhrp3-hrp2',
    'Pyrene Talos',
]

def redmine(apps, schema_editor):
    Project, License, Package, Repo = (apps.get_model('gepetto_packages', model)
                                       for model in ['Project', 'License', 'Package', 'Repo'])
    dummy_project, _ = Project.objects.get_or_create(name='dummy')
    for api in REDMINE_APIS:
        for data in requests.get(f'{api}/projects.json?limit=100', headers=HEADERS).json()['projects']:
            if data['name'] in PACKAGES:
                Package.objects.get_or_create(name=data['name'], project=dummy_project)
            package_qs = Package.objects.filter(name=data['name'])
            if package_qs.exists():
                r = Repo(package=package_qs.first(), repo_id=data['id'], open_pr=0)
                repo_data = requests.get(f'{api}/projects/{r.repo_id}.json', headers=HEADERS).json()['project']
                r.homepage = repo_data['homepage']
                r.url = f'{api}/projects/{repo_data["identifier"]}'
                issues_data = requests.get(f'{api}/issues.json?project_id={r.repo_id}&status_id=open', headers=HEADERS)
                r.open_issues = issues_data.json()['total_count']
                r.save()
                if r.homepage and not r.package.homepage:
                    r.package.homepage = r.homepage
                    r.package.save()


class Migration(migrations.Migration):

    dependencies = [
        ('gepetto_packages', '0003_gitlab'),
    ]

    operations = [
        migrations.RunPython(redmine),
    ]
