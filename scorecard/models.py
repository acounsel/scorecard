import csv
import datetime
import io

from django.apps import apps
from django.db import models
from django.http import StreamingHttpResponse

from django_scorecard import storage_backends

from model_utils.models import StatusModel, TimeStampedModel
from model_utils import Choices

class Echo:
    """An object that implements just the write method
    of the file-like interface.
    """
    def write(self, value):
        """Write the value by returning it, instead of
        storing in a buffer.
        """
        return value

class Overview(TimeStampedModel):

    name = models.CharField(max_length=255)
    subtitle = models.CharField(max_length=255, blank=True)
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

    def import_data(self):
        with open('data.csv', 'r') as import_file:
            reader = csv.DictReader(import_file)
            for index, cdict in enumerate(
                reader, start=1):
                print(index, cdict)
                Model = apps.get_model(
                    app_label='scorecard', model_name=cdict['type'])
                instance, created = Model.objects.get_or_create(
                    name=cdict['name'],
                    description=cdict['description'],
                    order_id=cdict['order_id'],
                    overview=self,
                )
                # if cdict.get('image_url'):
                #     instance.image = cdict['image_url']
                #     instance.save()
                print(instance)


    def import_commitments(self):
        with open('commitments.csv', 'r') as import_file:
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
                print(c_dict['name'])
                commitment, created = Commitment.objects \
                    .get_or_create(
                    order_num=c_dict['order_num'],
                    order_letter=c_dict['order_letter'],
                    name=c_dict['name'][:255],
                    original_timeline=c_dict['original_timeline'],
                    description=c_dict['description'],
                    overview=self,
                )
                if len(c_dict['name']) > 250:
                    print('TOO LONG!')
                category, created = CommitmentCategory \
                    .objects.get_or_create(
                    name=c_dict['category']
                )
                commitment.category = category
                for field in (
                    'has_detailed_plan', 
                    'has_approved_funding',
                    'has_begun_implementation',
                    'is_complete'):
                    if c_dict[field] == 'N':
                        value = False
                    elif c_dict[field] == 'Y':
                        value = True
                    else:
                        value = None
                    setattr(commitment, field, value)
                commitment.save()
                Status.objects.get_or_create(
                    commitment=commitment,
                    status=c_dict['status'],
                    description=c_dict.get('status_description'),
                    date=datetime.date(2020,6,1),
                )
                Status.objects.get_or_create(
                    commitment=commitment,
                    status=c_dict['status_2019'],
                    date=datetime.date(2019,2,1),
                )

    def export_commitments(self):
        pseudo_buffer = Echo()
        writer = csv.writer(pseudo_buffer)
        rows = self.get_export_rows()
        response = StreamingHttpResponse(
            (writer.writerow(row) for row in rows),
            content_type="text/csv")
        cont_disp = 'attatchment;filename="commitment_export.csv"'
        response['Content-Disposition'] = cont_disp
        return response

    def get_export_rows(self, queryset=None):
        if not queryset:
            queryset = self.commitment_set.all()
        rows = [
            ['category', 'id', 'commitment', 
                'description', 'original_timeline', 
                'has_detailed_plan', 'has_approved_funding', 
                'has_begun_implementation', 'is_complete', 
                'latest_status', 'status_date',
                'status_decription', 'previous status',
                'previous_status_date', 
                'previous_status_description',
            ],
        ]
        for commitment in queryset:
            row = commitment.get_export_row()
            rows.append(row)
        return rows

class CommitmentCategory(models.Model):

    name = models.CharField(max_length=255)
    order_num = models.PositiveSmallIntegerField(default=0)
    overview = models.ForeignKey(Overview, 
        on_delete=models.SET_NULL, blank=True, null=True)

    class Meta:
        ordering = ('order_num',)
        verbose_name_plural = 'commitment categories'

    def __str__(self):
        return self.name

class Commitment(models.Model):

    name = models.CharField(max_length=255)
    category = models.ForeignKey(CommitmentCategory, 
        on_delete=models.SET_NULL, blank=True, null=True)
    description = models.TextField(blank=True)
    overview = models.ForeignKey(Overview, 
        on_delete=models.SET_NULL, blank=True, null=True)
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

    def get_export_row(self):
        row = [self.category.name, 
            str(self.order_num) + self.order_letter, self.name,
            self.description, self.original_timeline,
            self.has_detailed_plan, self.has_approved_funding,
            self.has_begun_implementation, self.is_complete,
        ]
        for status in self.status_set.order_by('-date'):
            row.extend([status.status, status.date, 
                status.description])
        return row

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
    date = models.DateField(blank=True, null=True)

    class Meta:
        verbose_name_plural = 'statuses'
        ordering = ('date',)

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
    overview = models.ForeignKey(Overview, 
        on_delete=models.SET_NULL, blank=True, null=True)
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
    date = models.DateField(blank=True, null=True)
    overview = models.ForeignKey(Overview, 
        on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.name

