# Generated by Django 2.1.2 on 2019-05-27 16:21

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('isbn', models.CharField(max_length=20)),
                ('title', models.CharField(max_length=200)),
                ('author', models.CharField(max_length=100)),
                ('publication_yr', models.CharField(max_length=10)),
                ('publisher', models.CharField(max_length=50)),
                ('image_url_s', models.URLField()),
                ('image_url_m', models.URLField()),
                ('image_url_l', models.URLField()),
            ],
            options={
                'ordering': ['pk'],
            },
        ),
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.IntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(10)])),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('last_modified', models.DateTimeField(auto_now=True)),
                ('isbn', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='bookcrossing.Book')),
            ],
            options={
                'ordering': ['pk'],
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.CharField(max_length=20)),
                ('location', models.CharField(max_length=50)),
                ('age', models.CharField(max_length=3)),
            ],
            options={
                'ordering': ['pk'],
            },
        ),
        migrations.AddField(
            model_name='rating',
            name='user_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='bookcrossing.User'),
        ),
    ]
