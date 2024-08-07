# Generated by Django 5.0.7 on 2024-08-07 08:01

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('core', '0001_initial'),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Treatment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
                ('remarks', models.TextField(max_length=255)),
                ('disease', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='treatment', to='core.disease')),
                ('doctor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='treatment', to='users.doctor')),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='treatment', to='users.patient')),
            ],
            options={
                'db_table': 'ams_treatment',
            },
        ),
        migrations.CreateModel(
            name='Prescription',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('details', models.TextField(max_length=255)),
                ('treatment', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='prescriptions', to='treatments.treatment')),
            ],
            options={
                'db_table': 'ams_prescription',
            },
        ),
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.IntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)])),
                ('comment', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.patient')),
                ('treatment', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='feedback', to='treatments.treatment')),
            ],
            options={
                'db_table': 'ams_feedback',
            },
        ),
    ]
