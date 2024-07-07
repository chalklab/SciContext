from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.forms.models import model_to_dict
from config.functions import *
from config.git_functions import *
from datetime import datetime


def home(request):
    ctxcnt = Contexts.objects.all().count()
    return render(request, "home.html", {'ctxcnt': ctxcnt})


def index(request):
    ctxs = lstctxs(None)
    return render(request, "contexts/index.html", {'ctxlist': ctxs})


def view(request, ctxid):
    ctx = getctx(ctxid)
    if ctx.subcontexts is not None:
        subids = ctx.subcontexts.split(',')
        ctxs = lstctxs(subids)
    else:
        subids = None
        ctxs = None
    cws = ctx.contextsfields_set.all().order_by('context', 'field')
    onts = gettrms()

    return render(request, "contexts/view.html",
                  {'context': ctx, 'fields': cws, 'onts': onts, 'ctxs': ctxs, 'subids': subids})


def add(request):
    """view to add data about a context"""
    if request.method == "POST":
        # save new namespace
        data = request.POST
        ctx = Contexts()
        ctx.name = data['name']
        ctx.description = data['description']
        ctx.filename = data['filename']
        if data['prjid']:
            ctx.project_id = data['prjid']
        else:
            ctx.project_id = None
        temp = list(request.POST.getlist('subctxs'))
        ctx.subcontexts = ','.join(temp)  # bizarre syntax, but it works!
        ctx.updated = datetime.now()
        ctx.save()
        # TODO: save field entries that have not been saved?
        return redirect('/contexts/view/' + str(ctx.id))

    ctxs = getctxs()
    prjs = getprjs()
    return render(request, "contexts/add.html", {'ctxs': ctxs, 'prjs': prjs})


# ajax functions (wrappers)


@csrf_exempt
def terms(request, ontid):
    termz = getont(ontid)
    return JsonResponse({"terms": termz}, status=200)


@csrf_exempt
def jsfldadd(request):
    fld = None
    if request.method == "POST":
        data = request.POST
        fldid = data['fldid']
        ctxid = data['ctxid']
        # check if field exists (assume context does)
        fld = Fields.objects.get(id=fldid)
        if not fld.exists():
            fld = Fields()
            fld.name = data['name']
            fld.datatype = data['datatype']
            fld.cardinality = data['card']
        fld.save()
        # create join table entry
        cf = ContextsFields()
        cf.field_id = fldid
        cf.context_id = ctxid
    return JsonResponse(model_to_dict(fld), status=200)


@csrf_exempt
def jsdelcwk(request):
    response = {}
    if request.method == "POST":
        data = request.POST
        cwkid = data['cwkid']
        Fields.objects.get(id=cwkid).delete()
        try:
            Fields.objects.get(id=cwkid)
            response.update({"response": "failure"})
        except Fields.DoesNotExist:
            response.update({"response": "success"})
    return JsonResponse(response, status=200)


@csrf_exempt
def jscwkread(request, cwkid=""):
    cwk = Fields.objects.get(id=cwkid)
    return JsonResponse(model_to_dict(cwk), status=200)


@csrf_exempt
def jswrtctx(request, ctxid: int):
    ctx = Contexts.objects.get(id=ctxid)
    tpl = '{"@vocab": "https://www.w3.org/2001/XMLSchema#",' \
          '"sdo": "https://stuchalk.github.io/scidata/ontology/scidata.owl#"}'
    cdict = json.loads(tpl)
    nss = {}
    # add namespaces
    for cwk in ctx.contextsfields_set.all():
        nss.update({cwk.term.nspace.ns: cwk.term.nspace.path})
    for key in nss:
        cdict.update({key: nss[key]})
    # add entries
    for cwk in ctx.contextsfields_set.all():
        tmp = {}
        if cwk.datatype == '@list':
            tmp.update({"@id": cwk.term.url, "@type": "string", "@container": "@list"})
        else:
            tmp.update({"@id": cwk.term.url, "@type": cwk.datatype})
        if cwk.newname:
            cdict.update({cwk.newname: tmp})
        else:
            cdict.update({cwk.field: tmp})
    jld = {"@context": cdict}
    text = json.dumps(jld, separators=(',', ':'))
    resp = addctxfile('contexts/' + ctx.filename + '.jsonld', 'commit via API ' + str(datetime.now()), text)
    return JsonResponse({"response": resp}, status=200)
