# Generated by Django 4.2.1 on 2023-05-07 15:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Place', '0004_place_rate_place_rate_no'),
    ]

    operations = [
        migrations.AlterField(
            model_name='place',
            name='rate',
            field=models.DecimalField(blank=True, decimal_places=1, max_digits=2),
        ),
    ]
