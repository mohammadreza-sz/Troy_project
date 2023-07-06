# Generated by Django 4.2.1 on 2023-07-06 08:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Profile', '0008_trip_common_people_id_alter_trip_common_people_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='Request',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('P', 'Pending'), ('A', 'Accepted'), ('R', 'Rejected')], default='P', max_length=1)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('orga_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='requests', to='Profile.organization')),
                ('tl_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='requests', to='Profile.tourleader')),
            ],
            options={
                'unique_together': {('orga_id', 'tl_id')},
            },
        ),
    ]