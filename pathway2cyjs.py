import json
import requests

__author__ = 'Kozo Nishida'
__email__ = 'knishida@riken.jp'
__version__ = '0.0.1'
__license__ = 'MIT'

def escher2cyelements(escher_json_url):
    r = requests.get(escher_json_url)
    data = json.loads(r.content)
    escher_nodes = data[1]['nodes']
#   escher_edges = 

    cyelements = {}
    cynodes = []
    cyedges = []
    nodeids = []

    for k, v in escher_nodes.items():
        if v['node_type'] == 'metabolite':
            data = {}
            data['id'] = k
            data['bigg_id'] = v['bigg_id']
            data['label'] = v['name']
            data['x'] = float(v['x'])
            data['y'] = float(v['y'])
            cynode = {'data':data, 'position':{'x':float(v['x']), 'y':float(v['y'])}, "selected":"false"}
            cynodes.append(cynode)

    cyelements["nodes"] = cynodes
    cyelements["edges"] = cyedges
    return cyelements

def cynodes2df(cynodes):
    rows = []
    for cynode in cynodes:
        rows.append(pd.Series(cynode['data']))
    return pd.DataFrame(rows)

def cyelements2cyjs(cyelements, filename):
    d = {}
    d["elements"] = cyelements
    print(json.dumps(d, indent=4), file=open(filename,'w'))
    print("save cyelements as " + filename)
