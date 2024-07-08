""" functions file for the contexts app"""
from config.svr_functions import *
from datetime import datetime


def getprjs():
    """get a list of projects"""
    prjs = Projects.objects.all()
    return prjs


def getprj(prjid):
    """get a project"""
    prj = Projects.objects.get(id=prjid)
    return prj


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


def getflds():
    """get a list of fields for a context file"""
    flds = Fields.objects.all()
    return flds


def getsvrs():
    """get a list of fields for a context file"""
    svrs = Servers.objects.all().order_by('name')
    return svrs


def getsvr(svrid):
    """get a list of fields for a context file"""
    svr = Servers.objects.get(id=svrid)
    return svr


def svrontsdb(svrid):
    """get a list of ontologies from a server"""
    onts = list(Onts.objects.filter(server_id=svrid))
    return onts


def ctxflds(cxtid):
    """get a list of fields for a context file"""
    fldids = ContextsFields.objects.get(context_id=cxtid).values_list('field_id', flat=True)
    flds = Fields.objects.filter(fld_id__in=fldids)
    return flds


def getfld(fldid):
    """get a field"""
    fld = Fields.objects.get(id=fldid)
    return fld


def getonts():
    """get a list of namespaces"""
    onts = Onts.objects.filter(name__isnull=False).order_by('name')
    return onts


def getont(ontid):
    """get the data about a namespace"""
    ont = Onts.objects.get(id=ontid)
    return ont


def ontaliases():
    aliases = Onts.objects.all().values_list('ns', flat=True).order_by('ns').distinct()
    return aliases


def gettrms(ontid=None):
    """get the list of all terms (or only those for one ontology)"""
    if ontid:
        trms = Terms.objects.filter(ont_id=ontid).order_by('title')
    else:
        trms = Terms.objects.all().order_by('title')
    return trms


def gettrm(ontid):
    """get the data for an ont term"""
    term = Terms.objects.get(id=ontid)
    return term


def termsbyont(ontid):
    """get the terms from a specific ontology"""
    terms = Terms.objects.all().filter(ont_id=ontid)
    return terms


def ctxonts(svrid):
    """
    gets the ontologies and then filters for only those already in contexts
    namespaces are already aligned otherwise this will not work
    """
    kept = []
    aliases = list(ontaliases())
    print(aliases)
    sonts = svronts(svrid)
    sonts.sort(key=lambda tup: tup[0])
    for i, ont in enumerate(sonts):
        if ont[0] in aliases:
            kept.append(ont)
    return sonts


def allonts():
    pass


def svrload(svrid):
    # get onts from server
    onts = svronts(svrid)
    # populate the onts table with namesplaces from OLS
    for ont in onts:
        if not ont['ns']:
            ont['ns'] = "NA"
        if not ont['title']:
            ont['name'] = "NA"
        if not ont['description']:
            ont['description'] = "NA"
        if not ont['path']:
            ont['path'] = "NA"
        if not ont['homepage']:
            ont['homepage'] = "NA"
        o, created = Onts.objects.get_or_create(
            name=ont['title'],
            description=ont['description'],
            ns=ont['ns'],
            path=ont['path'],
            homepage=ont['homepage'],
            server_id=svrid
        )
        if created:
            o.updated = datetime.now()
            o.save()

    return True


def ontload(svrid, ontid):
    # get an ontologies' set of terms in a server
    trms = svronttrms(svrid, ontid)
    for trm in trms:
        if not trm['title']:
            trm['title'] = "NA"
        if not trm['code']:
            trm['code'] = "NA"
        if not trm['description']:
            trm['description'] = "NA"
        if not trm['visible']:
            trm['visible'] = "NA"
        if not trm['ontid']:
            trm['ontid'] = "NA"
        t, created = Terms.objects.get_or_create(
            title=trm['label'],
            code=trm['code'],
            description=trm['description'],
            visible='yes',
            ont_id=trm['ontid']
        )
        if created:
            t.updated = datetime.now()
            t.save()

    return True
