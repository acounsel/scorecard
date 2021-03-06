# Generated by Django 3.0.6 on 2020-05-22 02:31

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import django_scorecard.storage_backends
import model_utils.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Commitment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True)),
                ('original_timeline', models.CharField(blank=True, max_length=255)),
                ('order_num', models.PositiveSmallIntegerField(default=0)),
                ('order_letter', models.CharField(blank=True, max_length=3)),
            ],
        ),
        migrations.CreateModel(
            name='CommitmentCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('order_num', models.PositiveSmallIntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('name', models.CharField(max_length=255)),
                ('document', models.FileField(blank=True, null=True, storage=django_scorecard.storage_backends.PrivateMediaStorage(), upload_to='cases/')),
                ('description', models.TextField(blank=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Overview',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('name', models.CharField(max_length=255)),
                ('hero_video', models.CharField(blank=True, max_length=255)),
                ('hero_image', models.CharField(blank=True, max_length=255)),
                ('story_part1', models.TextField(blank=True)),
                ('story_part2', models.TextField(blank=True)),
                ('story_part3', models.TextField(blank=True)),
                ('achievements_text', models.TextField(blank=True)),
                ('challenges_text', models.TextField(blank=True)),
                ('report', models.URLField(blank=True, max_length=255)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Status',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('status', model_utils.fields.StatusField(choices=[('completed', 'Completed'), ('in_progress', 'In Progress'), ('delayed', 'Delayed'), ('not_started', 'Not Started')], default='completed', max_length=100, no_check_for_status=True, verbose_name='status')),
                ('status_changed', model_utils.fields.MonitorField(default=django.utils.timezone.now, monitor='status', verbose_name='status changed')),
                ('description', models.TextField(blank=True)),
                ('commitment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='scorecard.Commitment')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Recommendation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True)),
                ('image', models.ImageField(blank=True, null=True, storage=django_scorecard.storage_backends.PublicMediaStorage(), upload_to='images/')),
                ('commitments', models.ManyToManyField(blank=True, to='scorecard.Commitment')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='commitment',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='scorecard.CommitmentCategory'),
        ),
        migrations.CreateModel(
            name='Challenge',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True)),
                ('image', models.ImageField(blank=True, null=True, storage=django_scorecard.storage_backends.PublicMediaStorage(), upload_to='images/')),
                ('commitments', models.ManyToManyField(blank=True, to='scorecard.Commitment')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Achievement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True)),
                ('image', models.ImageField(blank=True, null=True, storage=django_scorecard.storage_backends.PublicMediaStorage(), upload_to='images/')),
                ('commitments', models.ManyToManyField(blank=True, to='scorecard.Commitment')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
