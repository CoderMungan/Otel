# Generated by Django 4.2.5 on 2023-11-06 00:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('OtelIcerik', '0015_konukbilgileri_kur'),
    ]

    operations = [
        migrations.AddField(
            model_name='konukbilgileri',
            name='birthday',
            field=models.CharField(blank=True, max_length=50, verbose_name='Müşteri Doğum Tarihi'),
        ),
    ]
