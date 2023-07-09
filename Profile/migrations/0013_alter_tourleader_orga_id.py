# Generated by Django 4.2 on 2023-07-09 15:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Profile', '0012_alter_request_created_at_alter_request_updated_at_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tourleader',
            name='orga_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='tourleader', to='Profile.organization'),
        ),
    ]
