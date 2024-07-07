# Generated by Django 5.0.6 on 2024-07-07 18:44

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Projects',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('description', models.CharField(max_length=128)),
                ('prefix', models.CharField(blank=True, max_length=64, null=True)),
                ('prjurl', models.CharField(blank=True, max_length=256, null=True)),
                ('updated', models.DateTimeField()),
            ],
            options={
                'db_table': 'projects',
                'managed': True,
            },
        ),
    ]
