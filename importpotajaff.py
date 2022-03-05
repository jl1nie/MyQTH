import json
import numpy as np
import matplotlib.pyplot as plt
import re
import sqlite3
from shapely.geometry import shape
from shapely.geometry.polygon import Polygon
import xml.etree.ElementTree as ET

parkdict = {}
tree = ET.parse('A10-10-property.xml')
root = tree.getroot()
for elem in root[15][0]:
    parkdict[elem.attrib['value']] = elem[0][0][0].text

con = sqlite3.connect('jaffpota.db')
cur = con.cursor()

jf = open('A10-10.geojson', mode = 'r', encoding='utf8')
js = json.load(jf)
js['name'] = 'JAFFPOTA'

for elem in js['features']:
    parkid = elem['properties']['A10_005']
    parkname = parkdict[parkid]
    #parkname = re.sub(r'\(.*\)','',parkname)
    #parkname = re.sub(r'（.*）','',parkname)
    res = cur.execute(f"select * from jaffpota where namek like '{parkname}%'")
    res = cur.fetchone()
    if res:
       (pota, jaff, name, location, locid, type, level, namek, lat, lng) = res
       elem['properties'] = { 'JAFF': jaff , 'POTA': pota}
    else:
        elem['properties'] = { 'JAFF': parkid , 'POTA': parkid}
        print(f'Error: {parkid} {parkname}')

out = open('jaffpota.geojson', mode = 'w', encoding='utf8')
json.dump(js, out, ensure_ascii=False)

areadict = {}
ar = np.array([])

for el in js['features']:
    name = el['properties']['JAFF']
    geo = el['geometry']
    shp = shape(geo)
    if name in areadict:
        if shp.area > areadict[name]:
            areadict[name] = shp.area
    else:
        areadict[name] = shp.area

for j in areadict:
    sq = int(areadict[j]*1000)
    q = f"update jaffpota set level = {sq} where jaff = '{j}';"
    cur.execute(q)
    if sq < 100:
        ar = np.append(ar,sq)

con.commit()
con.close()

fig = plt.figure()
ax = fig.add_subplot(1,1,1)
ax.hist(ar, bins=50)
ax.set_xlabel('x')
ax.set_ylabel('freq')
fig.savefig('parkarea-hist.png')