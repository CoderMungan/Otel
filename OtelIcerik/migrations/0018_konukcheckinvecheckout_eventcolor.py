# Generated by Django 4.2.5 on 2023-11-09 01:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('OtelIcerik', '0017_alter_konukbilgileri_birthday'),
    ]

    operations = [
        migrations.AddField(
            model_name='konukcheckinvecheckout',
            name='eventColor',
            field=models.CharField(blank=True, default='#940101', max_length=50, verbose_name='Renk'),
        ),
    ]
