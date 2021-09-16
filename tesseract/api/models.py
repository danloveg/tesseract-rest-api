from django.db import models
from django.utils.translation import gettext_lazy as _

class OCRJob(models.Model):
    class JobStatus(models.TextChoices):
        NOT_STARTED = 'NS', _('Not Started')
        IN_PROGRESS = 'IP', _('In Progress')
        COMPLETE = 'CP', _('Complete')
        FAILED = 'FD', _('Failed')

    identifier = models.UUIDField(primary_key=True)
    description = models.TextField()
    job_status = models.CharField(max_length=2, choices=JobStatus.choices,
                                  default=JobStatus.NOT_STARTED)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(null=True)
    files_processed = models.IntegerField(default=0)
    total_files = models.IntegerField()
