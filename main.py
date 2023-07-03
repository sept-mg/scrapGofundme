import requests, json, sqlite3, time
limit = 20
offset = 1
url = f"https://gateway.gofundme.com/web-gateway/v1/feed/z86fy-soutien-pour-la-famille-du-policier-de-nanterre/donations?limit={limit}&offset="

i = 0
data = []
def start(i):
    try :
        for i in range(i, 1000, offset):
            time.sleep(0.1)
            r = requests.get(url + str(i))
            print("offset" + str(i))
            extract = json.loads(r.text)
            for j in extract["references"]["donations"]:
                data.append({"name": j["name"], "amount": j["amount"], "donation_id": j["donation_id"], "created_at": j["created_at"]})
            # get only "name", "amount", "donation_id" and "created_at"
    except:
        pass
        start(i)
# make a json file

start(0)

conn = sqlite3.connect('donations.db')
cursor = conn.cursor()

cursor.execute(
    '''
    CREATE TABLE IF NOT EXISTS donations (
        name TEXT,
        amount REAL,
        donation_id INTEGER PRIMARY KEY,
        created_at TEXT
    )
    '''
)

for donation in data:
    # Vérifier si le donation_id existe déjà dans la table
    cursor.execute('SELECT donation_id FROM donations WHERE donation_id=?', (donation['donation_id'],))
    existing_donation = cursor.fetchone()

    if donation['name'] == "Anonymous" or existing_donation:
        print(f"Donation_id {donation['donation_id']} existe déjà dans la base de données. Ignorer l'insertion.")
    else:
        cursor.execute('''
            INSERT INTO donations (name, amount, donation_id, created_at)
            VALUES (?, ?, ?, ?)
        ''', (donation['name'], donation['amount'], donation['donation_id'], donation['created_at']))

conn.commit()

conn.close()