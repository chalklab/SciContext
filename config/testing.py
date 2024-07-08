from ols_py.client import *
from operator import itemgetter

client = Ols4Client()
resp = client.get_terms('iao', params={"page": 0, "size": 1000})
terms = resp.embedded.terms
# terms = sorted(temp, key=itemgetter('label'))
print(terms)
exit()
for term in terms:
    print(term['title'])
exit()


ontid = 524  # abcd
terms = resp.embedded.terms
tlist = []
for term in terms:
    tlist.append({'title': term.label, 'code': term.ontology_name,
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
