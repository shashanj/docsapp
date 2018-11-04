# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('driver', '0001_initial'),
        ('customer', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ride',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('lat', models.CharField(max_length=10)),
                ('long', models.CharField(max_length=10)),
                ('createts', models.DateTimeField(auto_now_add=True)),
                ('customer', models.ForeignKey(to='customer.Customer')),
            ],
            options={
                'db_table': 'ride_request',
            },
        ),
        migrations.CreateModel(
            name='RideDriver',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('status', models.IntegerField(default=0)),
                ('createts', models.DateTimeField(auto_now_add=True)),
                ('last_updatets', models.DateTimeField(auto_now_add=True)),
                ('driver_id', models.ForeignKey(to='driver.Driver')),
                ('ride_id', models.OneToOneField(to='dashboard.Ride')),
            ],
            options={
                'db_table': 'ride_driver',
            },
        ),
        migrations.CreateModel(
            name='RideDriverEvent',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('status', models.IntegerField(default=0)),
                ('createts', models.DateTimeField(auto_now_add=True)),
                ('driver_id', models.ForeignKey(to='driver.Driver')),
                ('ride_id', models.ForeignKey(to='dashboard.Ride')),
            ],
            options={
                'db_table': 'ride_driver_event',
            },
        ),
    ]
