# Generated by Django 3.0.6 on 2020-06-06 01:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scorecard', '0010_auto_20200605_1828'),
    ]

    operations = [
        migrations.AddField(
            model_name='document',
            name='date',
            field=models.DateField(blank=True, null=True),
        ),
    ]