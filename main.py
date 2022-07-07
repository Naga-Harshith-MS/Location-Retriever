import urllib.request, urllib.parse, urllib.error
import sqlite3
import json
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE


# Enter the API key within the quotes
apikey = ''
googleurl = "https://maps.googleapis.com/maps/api/geocode/json?"

# Here we create a sqlite3 database in order to store the data
con = sqlite3.connect('database.sqlite')
cur = con.cursor()

cur.execute('DROP TABLE IF EXISTS Places')
cur.execute('CREATE TABLE IF NOT EXISTS Places (address TEXT, retrieveddata TEXT)')

a = 0
handle = open("locations.data")

for b in handle:
#    if count > : break
#If the API you are using, has a rate limit, then set the rate here
    c = b.strip()
    cur.execute('SELECT retrieveddata FROM Places WHERE address= ?', (memoryview(c.encode()), ))

    dictionary = dict()
    dictionary["address"] = c
    dictionary['key'] = apikey
    url = googleurl + urllib.parse.urlencode(dictionary)

    print('Retrieving data from', url)
    urldata = urllib.request.urlopen(url, context=ctx)
    reqdata = urldata.read().decode()
    print('Retrieved data:', len(reqdata), 'characters')

    a += 1

    try:
        js = json.loads(reqdata)
    except: continue

    if (js['status'] != 'OK' and js['status'] != 'ZERO_RESULTS') or 'status' not in js:
        print('ERROR2')
        break

    cur.execute('''INSERT INTO Places (address, retrieveddata)
            VALUES ( ?, ? )''', (memoryview(c.encode()), memoryview(reqdata.encode()) ) )
    con.commit()


cur.execute('SELECT * FROM Locations')
for a in cur :
    data = str(a[1].decode())
    try: z = json.loads(str(data))
    except: continue
    lat = z["results"][0]["geometry"]["location"]["lat"]
    lng = z["results"][0]["geometry"]["location"]["lng"]
    if lat == 0 or lng == 0:continue
    where = z['results'][0]['formatted_address']
    print(where.replace("'", ""), lat, lng)
