import csv
import io

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
    commitment_chart_text = models.TextField(blank=True)
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
        ordering = ('order_num',)
        verbose_name_plural = 'commitment categories'

    def __str__(self):
        return self.name

class CommitmentManager(models.Manager):

    def import_commitments(self, import_file):
        categories = ('Pasture', 'Water', 'Monitoring',
            'Individual Compensation', 
            'Collective Compensation',
            'Undai River Diversion')
        for cat in categories:
            CommitmentCategory.objects.get_or_create(
                name=cat
            )
        reader = csv.DictReader(import_file)
        for index, c_dict in enumerate(
            reader, start=1):
            print(c_dict)
            commitment, created = self.get_or_create(
                order_num=c_dict['\ufefforder_num'],
                name=c_dict['name'],
                original_timeline=c_dict['original_timeline'],
                description=c_dict['description'],
            )
            category = CommitmentCategory.objects.get(
                name=c_dict['category']
            )
            commitment.category = category
            commitment.save()
            Status.objects.create(
                commitment=commitment,
                status=c_dict['status'],
                description=c_dict.get('status_description')
            )

class Commitment(models.Model):
    objects = CommitmentManager()

    name = models.CharField(max_length=255)
    category = models.ForeignKey(CommitmentCategory, 
        on_delete=models.SET_NULL, blank=True, null=True)
    description = models.TextField(blank=True)
    original_timeline = models.CharField(
        max_length=255,blank=True)
    order_num = models.PositiveSmallIntegerField(default=0)
    order_letter = models.CharField(max_length=3, blank=True)
    has_detailed_plan = models.NullBooleanField()
    has_approved_funding = models.NullBooleanField()
    has_begun_implementation = models.NullBooleanField()
    is_complete = models.NullBooleanField()

    class Meta:
        ordering = ('order_num', 'order_letter')

    def __str__(self):
        return self.name

    def get_status(self):
        return self.status_set.last()

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
    is_current = models.BooleanField(default=True)

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

