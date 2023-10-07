const endpoint = {
    'revgeocode':'https://mreversegeocoder.gsi.go.jp/reverse-geocoder/LonLatToAddress',
    'elevation':'https://cyberjapandata2.gsi.go.jp/general/dem/scripts/getelevation.php',
    'muni' : 'https://www.sotalive.net/api/reverse-geocoder/LonLatMuniToAddress',
};

var cache_result = null;
var prev_pos = null;

async function local_reverse_geocoder(lat, lng, elev) {
    let pos = '?lat=' + String(lat) + '&lon=' + String(lng);

    if (prev_pos && prev_pos == pos && cache_result)
	return cache_result;

    prev_pos = pos;
	    
    let rev_uri = endpoint['revgeocode'] + pos
    let elev_uri = endpoint['elevation'] + pos + '&outtype=JSON'
    let res_elev = null;
    if (elev) 
	res_elev = fetch(elev_uri);

    let res = await fetch(rev_uri);
    res = await res.json();
    if (!('results' in res)) {
	cache_result = {'errors': 'OUTSIDE_JA'}; 
	return cache_result; 
    }
    
    let muni_uri =
	endpoint['muni'] + pos + '&muni=' + res['results']['muniCd'];
    let res2 = await fetch(muni_uri);
    let result = await res2.json()
    result['addr1'] = res['results']['lv01Nm']
    result['errors'] = 'OK'
    cache_result = result;
    
    if (elev) {
	return res_elev
	    .then(res => res.json())
	    .then(res => {
		result['elevation'] = res['elevation']
		result['hsrc'] = res['hsrc']
		if (res['elevation'] == '-----')
		    result['errors'] = 'OUTSIDE_JA';
		cache_result = result;
		return result;})
    } else
	return new Promise((resolve, reject) => { resolve(result);});
}
