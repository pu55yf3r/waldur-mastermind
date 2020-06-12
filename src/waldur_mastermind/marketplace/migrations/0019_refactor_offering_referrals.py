# Generated by Django 2.2.10 on 2020-05-11 14:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('marketplace', '0018_change_default_referrals_value'),
    ]

    operations = [
        migrations.RemoveField(model_name='offering', name='referrals',),
        migrations.AlterField(
            model_name='offering',
            name='datacite_doi',
            field=models.CharField(
                blank=True, max_length=255, verbose_name='Datacite DOI'
            ),
        ),
    ]