# Generated by Django 4.0.2 on 2022-03-12 17:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usermanager', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(error_messages={'unique': 'Cette adresse mail existe déjà'}, max_length=255, unique=True, verbose_name='email address'),
        ),
    ]
