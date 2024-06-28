import requests
import json
import untangle
import xml.etree.ElementTree as ET

req_headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
url = 'https://plataforma-pf.sccon.com.br/gama-api/auth/token?password=<senha>&username=<usuario>'
req = requests.get(url, headers=req_headers)

res_json = json.loads(req.text)

access_token = res_json['access_token']

req_headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36', 'Authorization': f'Bearer {access_token}'}
url = 'https://plataforma-pf.sccon.com.br/gama-api/users-planet/users/609c9c0f-5244-4714-b5cf-ac3a9078fe54'
req = requests.get(url, headers=req_headers)

res_json = json.loads(req.text)

gsa_json = res_json['geoserviceAccesses']

wmts_json = gsa_json[0]

req_headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
url = wmts_json['link']
req = requests.get(url, headers=req_headers)

old_tiling = '{TileMatrix}/{TileCol}/{TileRow}'
new_tiling = '{z}/{x}/{y}'

filtered = req.text.replace(old_tiling, new_tiling)

res_xml = untangle.parse(filtered)

data = {}

for layer in res_xml.Capabilities.Contents.Layer:
    inner_data = []
    title = layer.ows_Title.cdata
    identifier = layer.ows_Identifier.cdata
    link = layer.ResourceURL['template']

    if identifier.startswith('global_monthly'):
        ano = identifier[15:19]
        mes = identifier[20:22]

        if ano in data:
            inner_data = data[ano]
        info = {'title' : title, 'identifier' : identifier, 'mes' : mes, 'link' : link}
        inner_data.append(info)
        data[ano] = inner_data
        planet_json = json.dumps(data)
        
filtrado = json.loads(planet_json)
for i in filtrado['2020']:
    print(i['identifier'])
    print(i['link']+'\n')
