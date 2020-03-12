from django.db import models
from django.contrib.postgres.fields import ArrayField


class FilesModel(models.Model):
    """
    Model for uploaded files
    """

    id = models.AutoField(auto_created=True, primary_key=True,
                          serialize=False, verbose_name='ID')
    uploaded_file = models.FileField(blank=False, null=False)


class FeedbackModel(models.Model):
    """
    Model for feedback form
    """
    full_name = models.CharField(max_length=255, blank=False)
    email = models.EmailField(blank=False)
    message = models.TextField(blank=True)
    files_to_send = ArrayField(models.CharField(
        max_length=255, blank=True, null=True), blank=True, null=True)
