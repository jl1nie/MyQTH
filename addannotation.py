import json
import os
import re
import sqlite3

fname = 'jaffpota.json'
con = sqlite3.connect('jaffpota.db')
cur = con.cursor()

def setotable(jaffid, uid):
    pattern = ['JAFF-0024','JAFF-0114','JAFF-0115','JAFF-0024,0115','JAFF-0114,0115','JAFF-0024,0114,0115']
    setodict = {55:2, 56:1, 57:1, 58:2, 59:1, 60:1, 61:1, 62:2, 63:1, 64:2,
    65:2, 66:1, 67:2, 68:3, 69:1, 70:3, 71:3, 72:3, 73:3, 74:3, 
    75:1, 76:2, 77:3, 78:1, 79:1, 80:1, 81:3, 82:4, 83:2, 84:3,
    85:4, 86:1, 87:3, 88:3, 89:1, 90:2, 91:2, 92:3, 93:3, 95:1,
    96:1, 97:1, 98:1, 99:3, 100:3, 101:3, 102:3, 103:3, 104:3, 105:3,
    106:3, 107:3, 108:3, 109:3, 111:3, 112:3, 113:3,
    1812:5,1813:3,1814:6}
    try:
        return pattern[setodict[int(uid)] - 1]
    except KeyError:
        return jaffid

with open(fname) as f:
    src = json.load(f)

for elem in src['objects']['jaffpota']['geometries']:
    jaff = elem['properties']['JAFF']
    uid = elem['properties']['UID']
    res = cur.execute(f"select * from jaffpota where jaff = '{jaff}'")
    res = cur.fetchone()
    if res:
       (pota, jaff, name, location, locid, type, level, namek, lat, lng) = res
       namek = re.sub(r'\(.*\)','',namek)
       namek = re.sub(r'（.*）','',namek)
       elem['properties'] = { 'JAFF': setotable(jaff, uid) , 'POTA': pota ,'UID':uid ,'NAME': namek}
    else:
        print(f'Fatal error: {jaff}')

base = os.path.splitext(os.path.basename(fname))[0]
out = open(base + '-annotated.json', mode = 'w', encoding='utf8')
out.write(json.dumps(src))
