# Generated by Django 4.2.6 on 2023-10-27 04:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('OtelIcerik', '0007_konukbilgileri'),
    ]

    operations = [
        migrations.CreateModel(
            name='KonukCheckInveCheckOut',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('checkIn', models.DateTimeField(verbose_name='Check-In Zamanı')),
                ('checkOut', models.DateTimeField(verbose_name='Check-Out Zamanı')),
                ('fiyat', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Fiyat')),
                ('konuk', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='OtelIcerik.konukbilgileri', verbose_name='Konuk Bilgileri')),
                ('oda', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='OtelIcerik.oteloda', verbose_name='Otel Oda')),
                ('otel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='OtelIcerik.otelyonetim', verbose_name='Otel Adı')),
            ],
        ),
    ]
