# Generated by Django 4.2 on 2023-07-09 10:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Profile', '0010_passenger_trip_passenger'),
    ]

    operations = [
        migrations.AlterField(
            model_name='request',
            name='created_at',
            field=models.DateField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='request',
            name='updated_at',
            field=models.DateField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='tourleader',
            name='joindDate',
            field=models.DateField(auto_now=True, null=True),
        ),
        migrations.AlterField(
            model_name='tourleader',
            name='orga_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='tourleader', to='Profile.organization'),
        ),
        migrations.AlterField(
            model_name='trip',
            name='departure_date',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='trip',
            name='return_date',
            field=models.DateField(null=True),
        ),
    ]
