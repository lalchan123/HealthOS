# Generated by Django 4.1.2 on 2022-10-22 21:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('practicaltestapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='company_operator',
            field=models.CharField(choices=[('GP', 'GP'), ('Robi', 'Robi'), ('Banglalink', 'Banglalink'), ('Airtel', 'Airtel')], default='GP', max_length=50),
        ),
    ]
