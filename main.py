import requests, json, sqlite3, time, yaml

#top donations

def getHeaders():
    with open("headers.yml") as headers:
        browser_headers = yaml.safe_load(headers)
    return browser_headers["Firefox"]

headers = getHeaders()

urltop = "https://www.gofundme.com/f/z86fy-soutien-pour-la-famille-du-policier-de-nanterre/topdonations"

def del_avant(texte : str, chaine_a_trouver : str) -> str:
    index_chaine = texte.find(chaine_a_trouver)
    if index_chaine != -1:  # Vérifier si la chaîne spécifiée est présente dans le texte
        texte_apres_chaine = texte[index_chaine + len(chaine_a_trouver):]
        return chaine_a_trouver + texte_apres_chaine
    else:
        return texte
    

def del_apres(texte : str, chaine_a_trouver :str) -> str:
    index_chaine_precise = texte.find(chaine_a_trouver)
    if index_chaine_precise != -1:
        return texte[:index_chaine_precise + len(chaine_a_trouver)]
    else:
        return texte

debut ='\\"topDonations\\":[{\\"donation_id\\"'
del_debut = '\\"topDonations\\":'
fin = ',\\"updates\\":[],\\"velocity\\"'


#recent donations
limit = 100
offset = 1
url = f"https://gateway.gofundme.com/web-gateway/v1/feed/z86fy-soutien-pour-la-famille-du-policier-de-nanterre/donations?limit={limit}&offset="

i = 0

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
conn.commit()
conn.close()

def start(i, conn, cursor):
    try :
        if i == -1:
            i = 0
            r = requests.get(urltop, headers=headers)
            edited = del_avant(r.text, debut)
            edited = del_apres(edited, fin)
            edited = edited.replace(fin, "")
            edited = edited.replace(del_debut, "")
            edited = edited.replace("\\", "")
            edited = '{"donations":' + edited + '}'
            extract = json.loads(edited)

            print("top donations " )
            for donation in extract["donations"]:
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
                            
    except:
        pass
        print("Erreur " + str(i))
        start(i)

while True :

    # make a json file
    conn = sqlite3.connect('donations.db')
    cursor = conn.cursor()
    start(-1, conn, cursor)

    conn.close()

    time.sleep(120)

    