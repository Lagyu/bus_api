# Generated by Django 2.2.6 on 2019-11-06 01:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Beacon',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mac_address', models.CharField(max_length=17)),
            ],
        ),
        migrations.CreateModel(
            name='OfficeBrunch',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='RaspberryPi',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('office_brunch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bus_api.OfficeBrunch')),
            ],
        ),
        migrations.CreateModel(
            name='BeaconRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('detection_time', models.DateTimeField(auto_now=True)),
                ('strength', models.IntegerField()),
                ('beacon', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bus_api.Beacon')),
                ('raspberry_pi', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bus_api.RaspberryPi')),
            ],
        ),
    ]
