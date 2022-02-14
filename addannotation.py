import json
import os
import re
import sqlite3
fname = 'jaffpota.json'
con = sqlite3.connect('jaffpota.db')
cur = con.cursor()

with open(fname) as f:
    src = json.load(f)

for elem in src['objects']['jaffpota']['geometries']:
    jaff = elem['properties']['JAFF']
    res = cur.execute(f"select * from jaffpota where jaff = '{jaff}'")
    res = cur.fetchone()
    if res:
       (pota, jaff, name, location, locid, type, level, namek, lat, lng) = res
       namek = re.sub(r'\(.*\)','',namek)
       namek = re.sub(r'（.*）','',namek)
       elem['properties'] = { 'JAFF': jaff , 'POTA': pota ,'NAME': namek}
    else:
        print(f'Fatal error: {jaff}')

base = os.path.splitext(os.path.basename(fname))[0]
out = open(base + '-annotated.json', mode = 'w', encoding='utf8')
out.write(json.dumps(src))
