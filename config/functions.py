""" functions file for the contexts app"""
from config.models import *
from config.ols_functions import *
import datetime


def getctxs():
    """get a list of contexts"""
    ctxs = Contexts.objects.all()
    return ctxs


def lstctxs(idlist):
    """get a list of contexts"""
    if idlist:
        clist = Contexts.objects.filter(id__in=idlist).values_list('id', 'name').order_by('name')
    else:
        clist = Contexts.objects.values_list('id', 'name').order_by('name')
    return clist


def getctx(ctxid):
    """get a context"""
    ctx = Contexts.objects.get(id=ctxid)
    return ctx


def getflds(cxtid):
    """get a list of fields for a context file"""
    ctx = Contexts.objects.get(id=cxtid)
    # cfs = ctx.values_list('id', 'field', 'term__title').order_by('field'))
    return ctx


def getfld(fldid):
    """get a field"""
    fld = Fields.objects.get(id=fldid)
    return fld


def getnsps():
    """get a list of namespaces"""
    spaces = Nspaces.objects.all().order_by('name')
    return spaces


def getnsp(nsid):
    """get the data about a namespace"""
    space = Nspaces.objects.get(id=nsid)
    return space


def nsaliases():
    aliases = Nspaces.objects.all().values_list('ns', flat=True).order_by('ns')
    return aliases


def gettrms():
    """get the list of ont terms"""
    return Terms.objects.all().order_by('title')


def gettrm(otid):
    """get the data for an ont term"""
    term = Terms.objects.get(id=otid)
    return term


def termsbyns(nsid):
    """get the terms from a specific namespace"""
    terms = Terms.objects.all().filter(nspace_id=nsid)
    return terms


def ctxonts():
    """
    gets the ontologies in ols and then filters for only those already in contexts
    namespaces are already aligned otherwise this will not work
    """
    kept = []
    aliases = list(nsaliases())
    print(aliases)
    allonts = olsonts()
    allonts.sort(key=lambda tup: tup[0])
    for i, ont in enumerate(allonts):
        if ont[0] in aliases:
            kept.append(ont)
    return allonts


def olsload(nss):
    # populate the nspaces table with namesplaces from OLS
    for ns in nss:
        if not ns['ns']:
            ns['ns'] = "NA"
        if not ns['title']:
            ns['name'] = "NA"
        if not ns['path']:
            ns['path'] = "NA"
        if not ns['homepage']:
            ns['homepage'] = "NA"
        n, created = Nspaces.objects.get_or_create(
            name=ns['title'],
            ns=ns['ns'],
            path=ns['path'],
            homepage=ns['homepage'],
            updated=datetime.datetime.now()
        )
        if not created:
            n.save()
    return True
