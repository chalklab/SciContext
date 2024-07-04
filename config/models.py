""" models for the contexts DB """

# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Contexts(models.Model):
    name = models.CharField(max_length=64)
    description = models.CharField(max_length=128)
    version = models.CharField(max_length=8)
    vocab = models.CharField(max_length=64)
    base = models.CharField(max_length=128)
    filename = models.CharField(max_length=128)
    subcontexts = models.CharField(max_length=256, blank=True, null=True)
    updated = models.DateTimeField()

    class Meta:
        managed = True
        db_table = 'contexts'
        app_label = 'contexts'


class Nspaces(models.Model):
    """ contexts nspaces table """
    name = models.CharField(max_length=64)
    ns = models.CharField(max_length=8)
    path = models.CharField(unique=True, max_length=64)
    homepage = models.CharField(max_length=128)
    updated = models.DateTimeField()

    class Meta:
        managed = True
        db_table = 'nspaces'
        app_label = 'nspaces'


class Terms(models.Model):
    """ contexts terms table """
    title = models.CharField(max_length=256)
    definition = models.CharField(max_length=2048, blank=True, null=True)
    code = models.CharField(max_length=64)
    nspace = models.ForeignKey(Nspaces, on_delete=models.DO_NOTHING, db_column='nspace_id')
    notes = models.CharField(max_length=64, blank=True, null=True)
    visible = models.CharField(max_length=8, blank=True, null=True)
    updated = models.DateTimeField()

    class Meta:
        managed = True
        db_table = 'terms'
        app_label = 'terms'


class ContextsFields(models.Model):
    context = models.ForeignKey(Contexts, on_delete=models.DO_NOTHING, db_column='context_id')
    term = models.ForeignKey(Terms, on_delete=models.DO_NOTHING, db_column='term_id')
    updated = models.DateTimeField()

    class Meta:
        managed = True
        db_table = 'contexts_fields'
        app_label = 'contexts_fields'


class Fields(models.Model):
    name = models.CharField(max_length=256)
    term = models.ForeignKey(Terms, on_delete=models.DO_NOTHING, db_column='term_id')
    datatype = models.CharField(max_length=8)
    container = models.CharField(max_length=64, blank=True, null=True)
    cardinality = models.PositiveIntegerField(blank=True, null=True)
    category = models.CharField(max_length=64, blank=True, null=True)
    unit = models.CharField(max_length=32, blank=True, null=True)
    comments = models.CharField(max_length=128, blank=True, null=True)
    updated = models.DateTimeField()

    class Meta:
        managed = True
        db_table = 'fields'
        app_label = 'fields'