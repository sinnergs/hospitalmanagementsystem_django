# Generated by Django 3.0.5 on 2020-06-28 07:49

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Userstore',
            fields=[
                ('ws_ssn', models.IntegerField()),
                ('ws_pat_id', models.AutoField(primary_key=True, serialize=False)),
                ('ws_pat_name', models.CharField(max_length=255)),
                ('ws_pat_age', models.IntegerField()),
                ('ws_city', models.CharField(max_length=100)),
                ('ws_state', models.CharField(max_length=100)),
                ('ws_adrs', models.CharField(max_length=300)),
                ('ws_status', models.CharField(default='Active', max_length=60)),
                ('ws_doj', models.DateTimeField(default=django.utils.timezone.now)),
                ('ws_rtype', models.CharField(choices=[('General', 'General Ward'), ('Semi', 'Semi Sharing'), ('Single', 'Single Room')], default='General', max_length=30)),
            ],
        ),
    ]
