# Generated by Django 3.0.6 on 2020-05-29 03:12

from django.db import migrations, models
import django_scorecard.storage_backends


class Migration(migrations.Migration):

    dependencies = [
        ('scorecard', '0003_auto_20200528_1435'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='commitmentcategory',
            options={'verbose_name_plural': 'commitment categories'},
        ),
        migrations.AlterModelOptions(
            name='status',
            options={'verbose_name_plural': 'statuses'},
        ),
        migrations.AlterField(
            model_name='achievement',
            name='image',
            field=models.ImageField(blank=True, null=True, storage=django_scorecard.storage_backends.PrivateMediaStorage(), upload_to='images/'),
        ),
        migrations.AlterField(
            model_name='challenge',
            name='image',
            field=models.ImageField(blank=True, null=True, storage=django_scorecard.storage_backends.PrivateMediaStorage(), upload_to='images/'),
        ),
        migrations.AlterField(
            model_name='overview',
            name='commitments_image',
            field=models.ImageField(blank=True, null=True, storage=django_scorecard.storage_backends.PrivateMediaStorage(), upload_to='images/'),
        ),
        migrations.AlterField(
            model_name='overview',
            name='story_image',
            field=models.ImageField(blank=True, null=True, storage=django_scorecard.storage_backends.PrivateMediaStorage(), upload_to='images/'),
        ),
        migrations.AlterField(
            model_name='recommendation',
            name='image',
            field=models.ImageField(blank=True, null=True, storage=django_scorecard.storage_backends.PrivateMediaStorage(), upload_to='images/'),
        ),
    ]
