# Generated by Django 2.1.11 on 2019-11-23 05:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recommender', '0003_auto_20190919_0131'),
    ]

    operations = [
        migrations.RenameField(
            model_name='similarity',
            old_name='similarity_score',
            new_name='score',
        ),
    ]
