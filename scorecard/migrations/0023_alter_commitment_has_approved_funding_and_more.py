# Generated by Django 4.0.3 on 2022-03-30 22:53

from django.db import migrations, models
import model_utils.fields


class Migration(migrations.Migration):

    dependencies = [
        ('scorecard', '0022_merge_20200618_1608'),
    ]

    operations = [
        migrations.AlterField(
            model_name='commitment',
            name='has_approved_funding',
            field=models.BooleanField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='commitment',
            name='has_begun_implementation',
            field=models.BooleanField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='commitment',
            name='has_detailed_plan',
            field=models.BooleanField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='commitment',
            name='is_complete',
            field=models.BooleanField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='status',
            name='status',
            field=model_utils.fields.StatusField(choices=[('completed', 'Completed'), ('in_progress', 'In Progress'), ('delayed', 'Delayed'), ('not_started', 'Not Started'), ('na', 'N/A')], default='completed', max_length=100, no_check_for_status=True, verbose_name='status'),
        ),
    ]
