const endpoint = {
    'revgeocode':'https://mreversegeocoder.gsi.go.jp/reverse-geocoder/LonLatToAddress',
    'elevation':'https://cyberjapandata2.gsi.go.jp/general/dem/scripts/getelevation.php',
    'muni' : 'https://www.sotalive.net/api/reverse-geocoder/LonLatMuniToAddress',
};

async function local_reverse_geocoder(lat, lng, elev) {
    let pos = '?lat=' + String(lat) + '&lon=' + String(lng)
    let rev_uri = endpoint['revgeocode'] + pos
    let elev_uri = endpoint['elevation'] + pos + '&outtype=JSON'

    if (elev) 
	res_elev = fetch(elev_uri);
    res = await fetch(rev_uri);
    res = await res.json();
    let muni_uri =
	endpoint['muni'] + pos + '&muni=' + res['results']['muniCd'];
    res2 = await fetch(muni_uri);
    res2 = await res2.json()
    res2['addr1'] = res['results']['lv01Nm']
    res2['errors'] = 'OK'
    if (elev) {
	return res_elev
	    .then(res3 => res3.json())
	    .then(res3 => {
		res2['elevation'] = res3['elevation']
		res2['hsrc'] = res3['hsrc']
		if (res3['elevation'] == '-----')
		    res2['errors'] = 'OUTSIDE_JA';
		return res2;})
    } else
	return new Promise((resolve, reject) => { resolve(res2);});
}
