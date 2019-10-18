# Generated by Django 2.2.6 on 2019-10-17 13:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('brassin', '0002_auto_20191017_1456'),
    ]

    operations = [
        migrations.CreateModel(
            name='recette_ingredient',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantite', models.DecimalField(decimal_places=4, max_digits=8, null=True)),
                ('temps_infusion', models.TimeField(blank=True, null=True)),
                ('ingredient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='brassin.ingredient')),
                ('recette', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='brassin.recette')),
            ],
        ),
    ]
