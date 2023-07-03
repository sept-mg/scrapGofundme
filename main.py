import requests, json, sqlite3, time
limit = 100
offset = 1
url = f"https://gateway.gofundme.com/web-gateway/v1/feed/z86fy-soutien-pour-la-famille-du-policier-de-nanterre/donations?limit={limit}&offset="

i = 0
data = []

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
conn.close()

def start(i, conn, cursor):
    # try :
        for i in range(i, 1000, offset):
            time.sleep(0.1)
            r = requests.get(url + str(i))
            print("offset " + str(i))
            extract = json.loads(r.text)
            for donation in extract["references"]["donations"]:
                    if donation['name'] != "Anonymous":
                        
                        cursor.execute('SELECT donation_id FROM donations WHERE donation_id=?', (donation['donation_id'],))
                        existing_donation = cursor.fetchone()

                        if existing_donation:
                            print(f"Donation_id {donation['donation_id']} existe déjà dans la base de données. Ignorer l'insertion.")
                        else:
                            cursor.execute('''
                                INSERT INTO donations (name, amount, donation_id, created_at)
                                VALUES (?, ?, ?, ?)
                            ''', (donation['name'], donation['amount'], donation['donation_id'], donation['created_at']))
                            conn.commit()
                            print(f"Donation_id {donation['donation_id']} a été ajouté dans la base de données.")
                            
    # except:
    #     pass
    #     print("Erreur " + str(i))
    #     start(i)

while True :

    # make a json file
    conn = sqlite3.connect('donations.db')
    cursor = conn.cursor()
    start(0, conn, cursor)

    conn.close()

    time.sleep(120)

    