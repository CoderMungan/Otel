# Generated by Django 4.2.6 on 2023-10-25 21:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('OtelIcerik', '0003_alter_oteloda_odaproblemi'),
    ]

    operations = [
        migrations.AddField(
            model_name='oteloda',
            name='odaRezerveMi',
            field=models.BooleanField(blank=True, default=False, verbose_name='Oda Rezerve Mi?'),
        ),
    ]
