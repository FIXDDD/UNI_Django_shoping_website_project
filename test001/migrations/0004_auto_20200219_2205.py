# Generated by Django 3.0.3 on 2020-02-19 14:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('test001', '0003_auto_20200219_2155'),
    ]

    operations = [
        migrations.AlterField(
            model_name='products',
            name='Release_date',
            field=models.DateField(),
        ),
    ]