# Generated by Django 4.2.1 on 2023-05-16 13:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Profile', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='rate_tour',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rates_tour', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='post_image',
            name='post',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Profile.post'),
        ),
        migrations.AddField(
            model_name='post',
            name='trip_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Profile.trip'),
        ),
        migrations.AddField(
            model_name='person',
            name='user_id',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='organization',
            name='city_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Profile.city'),
        ),
        migrations.AddField(
            model_name='organization',
            name='user_id',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='orguser', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='city',
            name='country_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Profile.country'),
        ),
        migrations.AddField(
            model_name='favorite',
            name='common_people_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Profile.commenpeople'),
        ),
        migrations.AddField(
            model_name='commenpeople',
            name='friend_id',
            field=models.ManyToManyField(to='Profile.commenpeople'),
        ),
    ]
