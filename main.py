import os, json, requests

def load_cfg():
    if os.getenv("SHOP_URL") and os.getenv("ACCESS_TOKEN"):
        return {
            "shop_url": os.environ["SHOP_URL"],
            "access_token": os.environ["ACCESS_TOKEN"],
            "company": os.getenv("COMPANY","Salayaa B.V."),
            "kvk": os.getenv("KVK","74293815"),
            "address": os.getenv("ADDRESS","Winkelcentrum Alexandrium, Watermanweg 231, 3067 GA Rotterdam, Nederland"),
            "email": os.getenv("EMAIL","info@salayaa.com")
        }
    with open("config.json") as f:
        return json.load(f)

CFG = load_cfg()
HEAD = {"X-Shopify-Access-Token": CFG["access_token"], "Content-Type": "application/json"}
BASE = CFG["shop_url"]

def upsert_policy(slug, title, body_html):
    r = requests.put(f"{BASE}/policies/{slug}.json", headers=HEAD, json={"shop_policy":{"title":title,"body":body_html}})
    r.raise_for_status(); return r.json()

def create_page(title, body_html, published=True):
    r = requests.post(f"{BASE}/pages.json", headers=HEAD, json={"page":{"title":title,"body_html":body_html,"published":published}})
    r.raise_for_status(); return r.json()

def seed_policies():
    upsert_policy("shipping_policy","Verzendbeleid",
        "<h1>Verzendbeleid</h1><p><strong>Gratis verzending</strong> op alle bestellingen.</p><p>Nederland: 2–4 werkdagen na verzending (totaal 3–6 incl. verwerking). EU: 3–7 werkdagen. Cut-off 17:00 (CET).</p>")
    upsert_policy("refund_policy","Retour- en terugbetalingsbeleid",
        "<h1>Retour- en terugbetalingsbeleid</h1><p>Retour binnen 14 dagen, ongedragen in originele verpakking. Uitzonderingen: cadeaubonnen, sale, geopende verzorging. Retourkosten voor klant tenzij onze fout.</p>")
    upsert_policy("privacy_policy","Privacybeleid",
        f"<h1>Privacybeleid</h1><p>Wij verwerken gegevens volgens de AVG. Rechten: inzage, rectificatie, wissing, bezwaar. Contact: <a href='mailto:{CFG['email']}'>{CFG['email']}</a>.</p>")
    upsert_policy("terms_of_service","Algemene voorwaarden",
        "<h1>Algemene voorwaarden</h1><p>Voorwaarden over bestellen, betalen, levering, retouren en aansprakelijkheid. Nederlands recht van toepassing.</p>")

def seed_pages():
    create_page("Over ons",
        "<h1>Over ons</h1><p>Salayaa maakt kleding voor vrouwen die het eenvoudig willen houden. Geen loze beloftes maar stukken die je echt draagt.</p><p><strong>Salayaa maakt kleding easy.</strong></p>")
    create_page("FAQ",
        "<h1>Veelgestelde vragen</h1><h2>Levertijd</h2><p>NL 2–4 werkdagen na verzending (3–6 incl. verwerking).</p><h2>Retour</h2><p>14 dagen, voorwaarden in retourbeleid.</p>")
    create_page("Contact",
        f"<h1>Contact</h1><p><strong>{CFG['company']}</strong><br>KvK: {CFG['kvk']}<br>{CFG['address']}<br>E-mail: <a href='mailto:{CFG['email']}'>{CFG['email']}</a></p>")
    create_page("Betaalmethoden",
        "<h1>Betaalmethoden</h1><ul><li>iDEAL</li><li>Visa</li><li>Mastercard</li><li>Maestro</li><li>American Express</li><li>PayPal</li><li>Klarna (Achteraf Betalen)</li><li>Shop Pay</li><li>Apple Pay</li><li>Google Pay</li></ul>")
    create_page("Verzendbeleid","<h1>Verzendbeleid</h1><p>Zie beleid in checkout. NL 2–4 dagen, gratis verzending.</p>")
    create_page("Retour- en terugbetalingsbeleid","<h1>Retour- en terugbetalingsbeleid</h1><p>14 dagen. Uitzonderingen en kosten zie beleid.</p>")
    create_page("Privacybeleid","<h1>Privacybeleid</h1><p>AVG, doeleinden, rechten, contact via e-mail.</p>")
    create_page("Algemene voorwaarden","<h1>Algemene voorwaarden</h1><p>Bestellen, betalen, levering, retouren, aansprakelijkheid.</p>")

if __name__ == "__main__":
    seed_policies()
    seed_pages()
    print("Klaar.")
