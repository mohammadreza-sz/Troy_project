# Generated by Django 4.2 on 2023-07-09 15:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Profile', '0011_make_all_datetime_to_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='request',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='request',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='tourleader',
            name='joindDate',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AlterField(
            model_name='trip',
            name='departure_date',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='trip',
            name='return_date',
            field=models.DateTimeField(null=True),
        ),
    ]