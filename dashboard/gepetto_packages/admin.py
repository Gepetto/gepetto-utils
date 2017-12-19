from django.contrib.admin import site

from .models import License, Package, Project, Repo

for model in [License, Package, Project, Repo]:
    site.register(model)
