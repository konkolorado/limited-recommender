# Generated by Django 2.1.2 on 2019-05-27 16:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('bookcrossing', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Recommendation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('similarity_score', models.DecimalField(decimal_places=14, max_digits=15)),
                ('purchased', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='predictive_item', to='bookcrossing.Book')),
                ('recommended', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='recommended_item', to='bookcrossing.Book')),
            ],
        ),
    ]
