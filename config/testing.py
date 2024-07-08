from ols_py.client import *

client = Ols4Client()
resp = client.search('name', params={"exact": True})
docs = resp.response.docs
for doc in docs:
    print(doc.iri, doc.label, doc.description)
exit()
for term in terms:
    print(term)
    exit()
exit()
# for term in terms:
#     print(term['title'])
# exit()
#
#
# terms = resp.embedded.terms
ontid = 334  # iao
tlist = []
for term in terms:
    tlist.append({'title': term.label, 'code': term.ontology_name, 'iri': str(term.iri),
                  'description': term.description[0], 'visible': 'yes', 'ontid': ontid})
    print(tlist)
    # t, created = Terms.objects.get_or_create(
    #     title=term.label,
    #     code=term.code,
    #     description=term.description,
    #     visible='yes',
    #     ont_id=ontid
    # )
    # if created:
    #     t.updated = datetime.datetime.now()
    #     t.save()
    # print(t)
    exit()
