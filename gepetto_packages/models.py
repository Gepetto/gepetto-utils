from django.db import models

from ndh.models import TimeStampedModel, NamedModel


class Project(NamedModel):
    pass


class License(NamedModel):
    pass


class Package(NamedModel, TimeStampedModel):
    project = models.ForeignKey(Project)
    url = models.URLField(max_length=200, blank=True, null=True)
    license = models.ForeignKey(License, blank=True, null=True)


class Repo(TimeStampedModel):
    url = models.URLField(max_length=200, unique=True)
    package = models.ForeignKey(Package)
    default_branch = models.CharField(max_length=50)
    open_issues = models.PositiveSmallIntegerField(blank=True, null=True)
    open_pr = models.PositiveSmallIntegerField(blank=True, null=True)

    def __str__(self):
        return self.url
