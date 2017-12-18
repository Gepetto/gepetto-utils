from django.db import models

from ndh.models import TimeStampedModel, NamedModel
from ndh.utils import query_sum


class Project(NamedModel):
    pass


class License(NamedModel):
    github_key = models.CharField(max_length=50)
    spdx_id = models.CharField(max_length=50)
    url = models.URLField(max_length=200)

    def __str__(self):
        return self.spdx_id or self.name


class Package(NamedModel, TimeStampedModel):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    homepage = models.URLField(max_length=200, blank=True, null=True)
    license = models.ForeignKey(License, on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        ordering = ('name',)

    def open_pr(self):
        return query_sum(self.repo_set, 'open_pr')

    def open_issues(self):
        return query_sum(self.repo_set, 'open_issues')


class Repo(TimeStampedModel):
    package = models.ForeignKey(Package, on_delete=models.CASCADE)
    url = models.URLField(max_length=200, unique=True)
    homepage = models.URLField(max_length=200, blank=True, null=True)
    license = models.ForeignKey(License, on_delete=models.CASCADE, blank=True, null=True)
    default_branch = models.CharField(max_length=50)
    open_issues = models.PositiveSmallIntegerField(blank=True, null=True)
    open_pr = models.PositiveSmallIntegerField(blank=True, null=True)
    repo_id = models.PositiveIntegerField()

    class Meta:
        ordering = ('package', 'url')

    def __str__(self):
        return self.url
