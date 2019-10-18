# Generated by Django 2.2.6 on 2019-10-17 12:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('brassin', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='recette',
            options={'ordering': ['id'], 'verbose_name': 'Recette'},
        ),
        migrations.AddField(
            model_name='brassin',
            name='recette',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='brassin.recette'),
        ),
        migrations.AddField(
            model_name='brassin',
            name='volume_starter',
            field=models.DecimalField(blank=True, decimal_places=1, default=0, max_digits=5, null=True),
        ),
        migrations.AlterField(
            model_name='brassin',
            name='temps_ebullition',
            field=models.TimeField(blank=True, default='01:30:00', null=True),
        ),
        migrations.AlterField(
            model_name='brassin',
            name='temps_empatage',
            field=models.TimeField(blank=True, default='01:15:00', null=True),
        ),
        migrations.AlterField(
            model_name='brassin_ingredient',
            name='quantite',
            field=models.DecimalField(decimal_places=4, max_digits=8, null=True),
        ),
        migrations.AlterField(
            model_name='ingredient',
            name='type_ingredient',
            field=models.CharField(choices=[('Malt', 'Malt'), ('Houblon', 'Houblon'), ('Levure', 'Levure'), ('Autre', 'Autre')], default='Autre', max_length=30, null=True),
        ),
    ]
