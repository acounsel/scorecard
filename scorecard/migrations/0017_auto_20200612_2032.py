# Generated by Django 3.0.6 on 2020-06-13 03:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scorecard', '0016_auto_20200612_1950'),
    ]

    operations = [
        migrations.AddField(
            model_name='overview',
            name='subtitle_en',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='overview',
            name='subtitle_mn',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
