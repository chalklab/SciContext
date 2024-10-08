# Generated by Django 5.0.6 on 2024-07-03 17:11

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('onts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Terms',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=256)),
                ('definition', models.CharField(blank=True, max_length=2048, null=True)),
                ('code', models.CharField(max_length=64)),
                ('notes', models.CharField(blank=True, max_length=64, null=True)),
                ('visible', models.CharField(blank=True, max_length=8, null=True)),
                ('updated', models.DateTimeField()),
                ('nspace', models.ForeignKey(db_column='nspace_id', on_delete=django.db.models.deletion.DO_NOTHING, to='onts.onts')),
            ],
            options={
                'db_table': 'terms',
                'managed': True,
            },
        ),
    ]
