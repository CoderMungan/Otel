# Generated by Django 4.2.6 on 2023-10-30 08:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('OtelIcerik', '0012_alter_konukcheckinvecheckout_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='konukbilgileri',
            options={'verbose_name': 'Konuk Bilgileri', 'verbose_name_plural': 'Konuk Bilgileri'},
        ),
        migrations.AlterModelOptions(
            name='oteloda',
            options={'verbose_name': 'Otel Oda Bilgileri', 'verbose_name_plural': 'Otel Oda Bilgileri'},
        ),
        migrations.AlterModelOptions(
            name='otelyonetim',
            options={'verbose_name': 'Otel Yönetim Bilgileri', 'verbose_name_plural': 'Otel Yönetim Bilgileri '},
        ),
    ]