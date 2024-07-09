""" models for the contexts DB """

# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Projects(models.Model):
    name = models.CharField(max_length=64)
    description = models.CharField(max_length=128)
    prefix = models.CharField(max_length=64, blank=True, null=True)
    prjurl = models.CharField(max_length=256, blank=True, null=True)
    updated = models.DateTimeField()

    class Meta:
        managed = True
        db_table = 'projects'
        app_label = 'projects'


class Contexts(models.Model):
    name = models.CharField(max_length=64)
    project = models.ForeignKey(Projects, on_delete=models.DO_NOTHING, db_column='project_id', blank=True, null=True)
    description = models.CharField(max_length=128, blank=True, null=True)
    version = models.CharField(max_length=8, blank=True, null=True)
    vocab = models.CharField(max_length=64, blank=True, null=True)
    base = models.CharField(max_length=128, blank=True, null=True)
    filename = models.CharField(max_length=128, blank=True, null=True)
    subcontexts = models.CharField(max_length=256, blank=True, null=True)
    updated = models.DateTimeField()

    class Meta:
        managed = True
        db_table = 'contexts'
        app_label = 'contexts'


class ContextJoins(models.Model):
    parent = models.ForeignKey(Contexts, on_delete=models.DO_NOTHING, db_column='parent_id', blank=True, null=True)
    child = models.ForeignKey(Contexts, on_delete=models.DO_NOTHING, db_column='child_id', blank=True, null=True)
    updated = models.DateTimeField()

    class Meta:
        managed = True
        db_table = 'contextjoins'
        app_label = 'contextjoins'


class Servers(models.Model):
    name = models.CharField(max_length=64)
    abbrev = models.CharField(max_length=64, blank=True, null=True)
    description = models.CharField(max_length=128)
    type = models.CharField(max_length=8, blank=True, null=True)
    homepage = models.CharField(max_length=128)
    apiurl = models.CharField(max_length=256)
    apikey = models.CharField(max_length=256, blank=True, null=True)
    headers = models.CharField(max_length=256, blank=True, null=True)
    updated = models.DateTimeField()

    class Meta:
        managed = True
        db_table = 'servers'
        app_label = 'servers'


class Onts(models.Model):
    """ contexts onts table """
    name = models.CharField(max_length=64)
    ns = models.CharField(max_length=8)
    path = models.CharField(unique=True, max_length=64)
    description = models.CharField(max_length=512, blank=True, null=True)
    homepage = models.CharField(max_length=128)
    server = models.ForeignKey(Servers, on_delete=models.DO_NOTHING, db_column='server_id')
    trmcnt = models.IntegerField(blank=True, null=True)
    version = models.CharField(max_length=16, blank=True, null=True)
    updated = models.DateTimeField()

    class Meta:
        managed = True
        ordering = 'name',
        db_table = 'onts'
        app_label = 'onts'


class Terms(models.Model):
    """ contexts terms table """
    title = models.CharField(max_length=256)
    definition = models.CharField(max_length=2048, blank=True, null=True)
    code = models.CharField(max_length=64)
    iri = models.CharField(max_length=256, blank=True, null=True)
    ont = models.ForeignKey(Onts, on_delete=models.DO_NOTHING, db_column='ont_id', default=None)
    notes = models.CharField(max_length=64, blank=True, null=True)
    visible = models.CharField(max_length=8, blank=True, null=True)
    updated = models.DateTimeField()

    class Meta:
        managed = True
        db_table = 'terms'
        app_label = 'terms'


class Fields(models.Model):
    name = models.CharField(max_length=256)
    term = models.ForeignKey(Terms, on_delete=models.DO_NOTHING, db_column='term_id')
    datatype = models.CharField(max_length=8)
    container = models.CharField(max_length=64, blank=True, null=True)
    category = models.CharField(max_length=64, blank=True, null=True)
    comments = models.CharField(max_length=128, blank=True, null=True)
    updated = models.DateTimeField()

    class Meta:
        managed = True
        db_table = 'fields'
        app_label = 'fields'


class ContextsFields(models.Model):
    context = models.ForeignKey(Contexts, on_delete=models.DO_NOTHING, db_column='context_id', blank=True, null=True)
    field = models.ForeignKey(Fields, on_delete=models.DO_NOTHING, db_column='field_id', blank=True, null=True)
    updated = models.DateTimeField()

    class Meta:
        managed = True
        db_table = 'contexts_fields'
        app_label = 'contexts_fields'
