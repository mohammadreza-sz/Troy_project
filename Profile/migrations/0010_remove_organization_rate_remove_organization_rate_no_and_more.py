# Generated by Django 4.2.1 on 2023-05-15 08:47

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Profile', '0009_remove_organization_id_remove_tourleader_first_name_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='organization',
            name='rate',
        ),
        migrations.RemoveField(
            model_name='organization',
            name='rate_no',
        ),
        migrations.AddField(
            model_name='tourleader',
            name='rate_no',
            field=models.IntegerField(blank=True, default=0),
        ),
        migrations.AlterField(
            model_name='organization',
            name='logo',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='tourleader',
            name='orga_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Profile.organization'),
        ),
        migrations.AlterField(
            model_name='tourleader',
            name='rate',
            field=models.DecimalField(blank=True, decimal_places=1, default=0, max_digits=2),
        ),
        migrations.CreateModel(
            name='Rate_Tour',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rate', models.DecimalField(decimal_places=1, default=5, max_digits=2, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(5)])),
                ('tour_leader', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rates_Tour', to='Profile.tourleader')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rates_Tour', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
