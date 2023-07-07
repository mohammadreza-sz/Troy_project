# Generated by Django 4.2 on 2023-06-27 13:45

from decimal import Decimal
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Profile', '0005_alter_organization_rates_premiumrequest'),
    ]

    operations = [
        migrations.AddField(
            model_name='organization',
            name='wallet',
            field=models.DecimalField(decimal_places=2, default=Decimal('1000.00'), max_digits=10),
        ),
        migrations.AddField(
            model_name='person',
            name='wallet',
            field=models.DecimalField(decimal_places=2, default=Decimal('1000.00'), max_digits=10),
        ),
    ]