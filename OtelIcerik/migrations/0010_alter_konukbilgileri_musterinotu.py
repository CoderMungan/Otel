# Generated by Django 4.2.6 on 2023-10-29 00:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('OtelIcerik', '0009_remove_oteloda_odafiyat'),
    ]

    operations = [
        migrations.AlterField(
            model_name='konukbilgileri',
            name='musteriNotu',
            field=models.CharField(blank=True, default='', max_length=50, verbose_name='Müşteri Notu'),
        ),
    ]
