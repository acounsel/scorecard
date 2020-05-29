from django.db import models

from django_scorecard import storage_backends

from model_utils.models import StatusModel, TimeStampedModel
from model_utils import Choices

class Overview(TimeStampedModel):

    name = models.CharField(max_length=255)
    hero_video = models.CharField(max_length=255, blank=True)
    hero_image = models.CharField(max_length=255, blank=True)
    story_image = models.ImageField(
        storage=storage_backends.PrivateMediaStorage(), 
        upload_to='images/', blank=True, null=True)
    story_part1 = models.TextField(blank=True)
    story_part2 = models.TextField(blank=True)
    story_part3 = models.TextField(blank=True)
    achievements_text = models.TextField(blank=True)
    challenges_text = models.TextField(blank=True)
    commitments_image = models.ImageField(
        storage=storage_backends.PrivateMediaStorage(), 
        upload_to='images/', blank=True, null=True)
    report = models.URLField(max_length=255, blank=True)

    def __str__(self):
        return self.name

class CommitmentCategory(models.Model):

    name = models.CharField(max_length=255)
    order_num = models.PositiveSmallIntegerField(default=0)

    class Meta:
        verbose_name_plural = 'commitment categories'

    def __str__(self):
        return self.name

class Commitment(models.Model):

    name = models.CharField(max_length=255)
    category = models.ForeignKey(CommitmentCategory, 
        on_delete=models.SET_NULL, blank=True, null=True)
    description = models.TextField(blank=True)
    original_timeline = models.CharField(
        max_length=255,blank=True)
    order_num = models.PositiveSmallIntegerField(default=0)
    order_letter = models.CharField(max_length=3, blank=True)

    def __str__(self):
        return self.name

class Status(StatusModel, TimeStampedModel):

    STATUS = Choices(
        ('completed', 'Completed'),
        ('in_progress', 'In Progress'),
        ('delayed', 'Delayed'),
        ('not_started', 'Not Started'),
    )
    commitment = models.ForeignKey(Commitment, 
        on_delete=models.CASCADE)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = 'statuses'

    def __str__(self):
        return self.get_status_display()

class OverviewModel(models.Model):

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    image = models.ImageField(
        storage=storage_backends.PrivateMediaStorage(), 
        upload_to='images/', blank=True, null=True)
    commitments = models.ManyToManyField(Commitment, 
        blank=True)
    order_id = models.PositiveSmallIntegerField(default=0)
    is_featured = models.BooleanField(default=False)

    class Meta:
        abstract = True
        ordering = ('order_id',)

    def __str__(self):
        return self.name

class Achievement(OverviewModel):

    pass

class Challenge(OverviewModel):

   pass

class Recommendation(OverviewModel):

    pass

class Document(TimeStampedModel):

    name = models.CharField(max_length=255)
    document = models.FileField(
        storage=storage_backends.PrivateMediaStorage(), 
        upload_to='cases/', blank=True, null=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

