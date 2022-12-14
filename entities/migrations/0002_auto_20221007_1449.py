# Generated by Django 3.2.7 on 2022-10-07 09:19

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('entities', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='school',
            name='board',
            field=models.CharField(choices=[('CBSE', 'CBSE'), ('State', 'State'), ('ICSE', 'ICSE'), ('IB', 'IB'), ('CIE', 'CIE'), ('NIOS', 'NIOS'), ('CISCE', 'CISCE')], default='State', max_length=50),
        ),
        migrations.AddField(
            model_name='school',
            name='highest_standard',
            field=models.IntegerField(default=1, validators=[django.core.validators.MinValueValidator(1, "Can't have standard lower than 1."), django.core.validators.MaxValueValidator(12, "Can't have standard higher than 12.")]),
        ),
    ]
