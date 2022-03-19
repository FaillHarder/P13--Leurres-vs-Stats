# Generated by Django 4.0.2 on 2022-03-19 17:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('adddata', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='color',
            name='name',
            field=models.CharField(max_length=30, unique=True, verbose_name='Couleur du leurre'),
        ),
        migrations.AlterField(
            model_name='lure',
            name='name',
            field=models.CharField(max_length=30, unique=True, verbose_name='Leurre'),
        ),
        migrations.CreateModel(
            name='CatchFish',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sky_state', models.CharField(choices=[('Ensoleillé', 'Ensoleillé'), ('Blanc', 'Blanc'), ('Gris', 'Gris'), ('Noir', 'Noir')], default='Clair', max_length=30, verbose_name='Etat du ciel')),
                ('water_state', models.CharField(choices=[('Clair', 'Clair'), ('Trouble', 'Trouble')], default='Clair', max_length=30, verbose_name="Etat de l'eau")),
                ('color_lure', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='adddata.color', verbose_name='Couleur du leurre')),
                ('fisherman', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Pécheur')),
                ('lure', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='adddata.lure', verbose_name='Leurre')),
            ],
        ),
    ]
