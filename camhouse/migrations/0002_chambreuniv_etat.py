# Generated by Django 3.2.7 on 2022-07-19 04:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('camhouse', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='chambreuniv',
            name='etat',
            field=models.IntegerField(null=True),
        ),
    ]
