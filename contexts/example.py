"""example functions for development"""
import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from config.git_functions import *
# from contexts.views import *
from config.functions import *
from scipy.io import loadmat
import pandas as pd


# test GitHub access
gh = False
if gh:
    test = '{"@context": {"@vocab": "https://www.w3.org/2001/XMLSchema#",' \
           '"sdo2": "https://stuchalk.github.io/scidata/ontology/scidata.owl#",' \
           '"condition": {"@id": "sdo:condition"}}}'
    print(test)
    out = addctxfile('contexts/test4.jsonld', 'test commit via API', test)
    print(out)
    exit()

# test matlab file import
mlab = True
if mlab:
    file = loadmat(
        '/Users/n00002621/Dropbox/Grants/Funded/NIST KnowLedger 2021 - 2022/Data/AmBench 2018/sam_0_output.mat')
    data = [[row.flat[0] for row in line] for line in file['ans'][0]]
    width = 320
    pd.set_option('display.width', width)
    pd.set_option('display.max_columns', 12)
    table = pd.DataFrame(data)
    print(table.head())
    exit()

# test ChEMBL API
chembl = False
if chembl:
    out = ctxonts()
    print(out)
    exit()

# add a new substance to the database
nslist = False
if nslist:
    nslist = getnsps()
    print(nslist)
    exit()

term = False
if term:
    data = getont(13)
    print(data.sdsection)
    exit()
