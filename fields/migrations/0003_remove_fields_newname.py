# Generated by Django 5.0.6 on 2024-07-09 10:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fields', '0002_remove_fields_cardinality_remove_fields_unit_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='fields',
            name='newname',
        ),
    ]
