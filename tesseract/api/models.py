import uuid
import os
from urllib.parse import urlparse

from django.db import models
from django.utils.translation import gettext_lazy as _


class TargetFile(models.Model):
    identifier = models.UUIDField(primary_key=True, default=uuid.uuid4)
    description = models.TextField(default='')
    file_uri = models.URLField(default=None)
    size_bytes = models.IntegerField(default=0)

    @property
    def file_name(self):
        path = self._parse_uri().path
        return os.path.basename(path)

    @property
    def uri_domain(self):
        return self._parse_uri().netloc

    @property
    def file_type(self):
        _, ext = os.path.splitext(self.file_name)
        return ext

    def _parse_uri(self):
        return urlparse(self.file_uri)

    def __str__(self):
        if self.description:
            return f'{self.file_uri} [{self.description}]'
        return f'{self.file_uri}'


class OCRJob(models.Model):
    class JobStatus(models.TextChoices):
        NOT_STARTED = 'NS', _('Not Started')
        IN_PROGRESS = 'IP', _('In Progress')
        COMPLETE = 'CP', _('Complete')
        FAILED = 'FD', _('Failed')

    target_file = models.ForeignKey(TargetFile, on_delete=models.CASCADE)
    identifier = models.UUIDField(primary_key=True)
    description = models.TextField()
    job_status = models.CharField(max_length=2, choices=JobStatus.choices,
                                  default=JobStatus.NOT_STARTED)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(null=True)
    files_processed = models.IntegerField(default=0)
    total_files = models.IntegerField()

    def __str__(self):
        return (
            f'ID: [{self.identifier}] '
            f'TARGET FILE: [{self.target_file.file_name}] '
            f'STATUS: [{self.job_status}]'
        )


class OCRTranscript(models.Model):
    related_job = models.ForeignKey(OCRJob, on_delete=models.CASCADE)
    tesseract_version = models.CharField(max_length=32)
    leptonica_version = models.CharField(max_length=32)
    image_type = models.CharField(max_length=32)
    transcript = models.TextField()
    size_bytes = models.IntegerField()
    page_num = models.IntegerField()
    total_pages = models.IntegerField()

    def __str__(self):
        return (
            f'TRANSCRIPT FOR: [{self.related_job.identifier}] '
            f'PAGE: [{self.page_num} of {self.total_pages}]'
        )
