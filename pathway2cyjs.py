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

WP_API_BASE = 'https://webservice.wikipathways.org/'

def wp2cyelements(identifier):
    gpml = requests.get(WP_API_BASE + 'getPathway?pwId=' + identifier + '&format=json').content
    soup = BeautifulSoup(json.loads(gpml)['pathway']['gpml'], "xml")
    
    wpnodes = soup.find_all('DataNode')
    wpedges = soup.find_all('Interaction')

    cyelements = {}
    cynodes = []
    cyedges = []
    nodeids = []

    for wpn in wpnodes:
        if wpn['Type'] == "Metabolite":
            g = wpn.find('Graphics')
            
            data = {}
            data['id'] = wpn['GraphId']
            nodeids.append(wpn['GraphId'])
            data['label'] = wpn['TextLabel']
            data['x'] = float(g['CenterX'])
            data['y'] = float(g['CenterY'])
            data['width'] = g['Width']
            data['height'] = g['Height']

            xref = wpn.find('Xref')
            if xref is not None:
                data['database'] = xref['Database']
                data['xrefID'] = xref['ID']
                print(data['id'], data['label'], data['database'], data['xrefID'])
                data['KEGG'] = bridgedbpy.gpml2kegg(xref['Database'], xref['ID'])

        cynode = {"data":data, "position":{"x":float(g["CenterX"]), "y":float(g["CenterY"])}, "selected":"false"}
        cynodes.append(cynode)

    for wpe in wpedges:
        data = {}
        for point in wpe.find_all('Point'):
            if point.has_attr('GraphRef') and point.has_attr('ArrowHead'):
                if point['GraphRef'] in nodeids:
                    data['target'] = point['GraphRef']
            elif point.has_attr('GraphRef'):
                if point['GraphRef'] in nodeids:
                    data['source'] = point['GraphRef']
        if 'source' in data.keys() and 'target' in data.keys():
            cyedge = {"data":data}
            cyedges.append(cyedge)

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
