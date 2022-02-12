import json
import re
import sqlite3

con = sqlite3.connect('xref.db')
cur = con.cursor()

jf = open('jaff.geojson', mode = 'r', encoding='utf8')
js = json.load(jf)
js['name'] = 'JAFFPOTA'
for elem in js['features']:
    m = re.match(r'(JAFF\-\d+).*',elem['properties']['JAF'])
    jaffcode = m.group(1)
    res = cur.execute(f"select * from xref where JAFF = '{jaffcode}'")
    res = cur.fetchall()
    for i in res:
        (pota, _, _, _, _, _, _, _, _) = i
        print(f'{pota} = {jaffcode}')
    elem['properties'] = { 'JAFF': jaffcode , 'POTA': pota}

out = open('jaffpota.geojson', mode = 'w', encoding='utf8')
out.write(json.dumps(js))

