# Generated by Django 4.2.1 on 2023-05-18 04:13

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Place', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city_name', models.CharField(max_length=30, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('country_name', models.CharField(max_length=30, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Favorite',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('favorite', models.TextField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_org', models.CharField(max_length=200, null=True, unique=True)),
                ('description', models.TextField(null=True)),
                ('logo', models.TextField(blank=True, null=True)),
                ('Address', models.CharField(max_length=255, null=True)),
                ('Phone', models.CharField(max_length=20, null=True)),
                ('rates', models.IntegerField(blank=True, default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('birth_date', models.DateField(null=True)),
                ('country', models.CharField(max_length=50, null=True)),
                ('city', models.CharField(max_length=50, null=True)),
                ('gender', models.BooleanField(null=True)),
                ('bio', models.TextField(null=True)),
                ('registration_date', models.DateField(auto_now=True)),
                ('profile_image', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('caption', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Post_image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('post_image', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Rate_Org',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rate', models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(5)])),
            ],
        ),
        migrations.CreateModel(
            name='TourLeader',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rates', models.IntegerField(blank=True, default=0)),
                ('rate_no', models.IntegerField(blank=True, default=0)),
                ('joindDate', models.DateTimeField(auto_now=True)),
                ('phonetl', models.CharField(max_length=20, null=True)),
                ('Id', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='Profile.person')),
                ('orga_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='tourleader', to='Profile.organization')),
            ],
        ),
        migrations.CreateModel(
            name='CommenPeople',
            fields=[
                ('Id', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='Profile.person')),
            ],
        ),
        migrations.CreateModel(
            name='Trip',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('departure_transport', models.CharField(choices=[('A', 'airplane'), ('S', 'ship'), ('B', 'bus'), ('T', 'train')], max_length=1, null=True)),
                ('return_transport', models.CharField(choices=[('A', 'airplane'), ('S', 'ship'), ('B', 'bus'), ('T', 'train')], max_length=1, null=True)),
                ('departure_date', models.DateTimeField(null=True)),
                ('return_date', models.DateTimeField(null=True)),
                ('Description', models.TextField(null=True)),
                ('capacity', models.IntegerField(null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(50)])),
                ('Price', models.IntegerField(null=True, validators=[django.core.validators.MinValueValidator(5), django.core.validators.MaxValueValidator(5000)])),
                ('TourLeader_ids', models.ManyToManyField(blank=True, to='Profile.tourleader')),
                ('destination_city', models.ManyToManyField(related_name='cities', to='Profile.city')),
                ('destination_country', models.ManyToManyField(related_name='countries', to='Profile.country')),
                ('organization_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='Profile.organization')),
                ('origin_city_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='Profile.city')),
                ('place_ids', models.ManyToManyField(blank=True, to='Place.place')),
            ],
        ),
        migrations.CreateModel(
            name='Rate_Tour',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rate', models.IntegerField(default=5, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(5)])),
                ('tour_leader', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rate_tour', to='Profile.tourleader')),
            ],
        ),
    ]
