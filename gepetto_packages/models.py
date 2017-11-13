from django.db import models

from ndh.models import TimeStampedModel, NamedModel
from ndh.utils import enum_to_choices

from .choices import REPO_ORIGINS


class Project(NamedModel):
    pass


class License(NamedModel):
    pass


class Package(NamedModel, TimeStampedModel):
    project = models.ForeignKey(Project)
    homepage = models.URLField(max_length=200, blank=True, null=True)
    license = models.ForeignKey(License, blank=True, null=True)

    class Meta:
        ordering = ('name',)

    def domain(self):
        return '.'.join(self.homepage.split('/')[2].split('.')[-2:])


class Repo(TimeStampedModel):
    package = models.ForeignKey(Package)
    url = models.URLField(max_length=200, unique=True)
    homepage = models.URLField(max_length=200, blank=True, null=True)
    license = models.ForeignKey(License, blank=True, null=True)
    default_branch = models.CharField(max_length=50)
    open_issues = models.PositiveSmallIntegerField(blank=True, null=True)
    open_pr = models.PositiveSmallIntegerField(blank=True, null=True)
    origin = models.PositiveSmallIntegerField(choices=enum_to_choices(REPO_ORIGINS))

    class Meta:
        ordering = ('package', 'origin')

    def __str__(self):
        return self.url
