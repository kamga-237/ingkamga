# Generated by Django 3.2.7 on 2022-07-19 05:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('camhouse', '0002_chambreuniv_etat'),
    ]

    operations = [
        migrations.RenameField(
            model_name='composition',
            old_name='montant',
            new_name='montants',
        ),
    ]
