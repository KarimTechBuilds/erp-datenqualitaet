import random
from datetime import date, timedelta
import copy
import csv

random.seed(42)

typen_liste = ["Schraube", "Mutter", "Bolzen", "Ventil", "Sensor", "Halterung"]
groessen_liste = ["M4", "M6", "M8", "klein", "gross", "10mm", "20mm"]
material_liste = ["Stahl", "Edelstahl", "Aluminium", "Kupfer", "Messing", "Kunststoff", "Titan"]
lieferant_liste = ["Karlsruhe Metallwerke", "Berlin Metallwerke", "Konstanz Metallwerke", "Aachen Metallwerke", "Stuttgart Metallwerke"]
daten_typen = ["artikelnummer", "bezeichnung", "material", "gewicht", "preis", "lieferant", "letzte_aenderung"]

def data_generation(typen, groessen, material, lieferant):

    data_list = []
    for i in range(200):

        start_datum = date(2023, 1, 1)
        zufallstage = random.randint(0, 365)
        datum = start_datum + timedelta(days= zufallstage)

        single_data_dict = {"artikelnummer":"","bezeichnung":"", "material": "", "gewicht":"", "preis": "", "lieferant": "", "letzte_aenderung": "" }

        single_data_dict["artikelnummer"] = f"A-{1001 + i}"
        single_data_dict["bezeichnung"] = f"{random.choice(typen)} {random.choice(groessen)}"
        single_data_dict["material"] = random.choice(material)
        single_data_dict["gewicht"] = round(random.uniform(0.1, 50.0), 2)
        single_data_dict["preis"] = round(random.uniform(1.0, 500.0), 2)
        single_data_dict["lieferant"] = f"{random.choice(lieferant)}"
        single_data_dict["letzte_aenderung"] = str(datum)

        
        data_list.append(single_data_dict)

    return data_list

saubere_liste = data_generation(typen_liste, groessen_liste, material_liste, lieferant_liste)

def fehler_injektion(list_of_data, daten_typen):

    zaeler = {"exaktes_duplikat": 0, "id_kollision": 0, "logisches_duplikat": 0, "fehlende_wert": 0, "material": 0, "komma": 0, "datum": 0, "leerzeichen": 0}
    data_list_copy = copy.deepcopy(list_of_data)
    material_varianten = {"Aluminium": ["Alu", "ALUMINIUM", "aluminium ", "ALU"], "Stahl": ["St", "STAHL", "stahl "], "Edelstahl": ["Edelst.", "EDELSTAHL", "edelstahl "], "Messing": ["Ms", "MESSING", "messing "], "Kunststoff": ["Kunstst.", "KUNSTSTOFF", "kunststoff "], "Kupfer": ["kupfer ", "Cu", "KUPFER"], "Titan": ["TITAN", "titan ", "Ti"]}
    anzahl_pro_typ = 5

    # Formatfehler

    
    for datensatz in random.sample(data_list_copy, anzahl_pro_typ):
        datensatz["material"] = random.choice(material_varianten[datensatz["material"]])
        zaeler["material"] += 1

    # Dezimalkomma

    for datensatz in random.sample(data_list_copy, anzahl_pro_typ ):
        datensatz["preis"] = f"{datensatz['preis']:.2f}".replace(".", ",")
        zaeler["komma"] += 1

    # Datumsformat

    for datensatz in random.sample(data_list_copy, anzahl_pro_typ):
        datum = date.fromisoformat(datensatz["letzte_aenderung"])
        datensatz["letzte_aenderung"] = datum.strftime(random.choice(["%d.%m.%Y", "%d/%m/%Y" ]))
        zaeler["datum"] += 1

    # Leerzeichen
    
    for datensatz in random.sample(data_list_copy, anzahl_pro_typ):
        datensatz["bezeichnung"] = " " + datensatz["bezeichnung"]+ " "
        zaeler["leerzeichen"] += 1

    # Exaktes Zeilenduplikat
    for _ in range(anzahl_pro_typ):
        datensatz_zum_kopieren = copy.deepcopy(data_list_copy[random.randint(0, 199)])
        data_list_copy.insert(random.randint(0, len(data_list_copy)-1), datensatz_zum_kopieren)
        zaeler["exaktes_duplikat"] += 1

    # Logisches Duplikat
    for n in range(anzahl_pro_typ):
        datensatz_falsch_ID = copy.deepcopy(data_list_copy[random.randint(0, len(data_list_copy)-1)])
        datensatz_falsch_ID["artikelnummer"] = f"A-{9001+n}"
        data_list_copy.insert(random.randint(0, len(data_list_copy)-1), datensatz_falsch_ID)
        zaeler["logisches_duplikat"] += 1

    # ID-Kollision
    for _ in range(anzahl_pro_typ):
        datensatz_ID_kollision = data_list_copy[random.randint(0, len(data_list_copy)-1)]
        datensatz_ID_kollision["artikelnummer"] = data_list_copy[random.randint(0, 199)]["artikelnummer"]
        zaeler["id_kollision"] += 1

    # Fehlende Werte
    pflichtfelder = ["bezeichnung", "material", "gewicht", "preis", "lieferant"]
    for _ in range(anzahl_pro_typ):
        datensatz_fehlenden_Wert =data_list_copy[random.randint(0, len(data_list_copy)-1)]
        datensatz_fehlenden_Wert[random.choice(pflichtfelder)] = None
        zaeler["fehlende_wert"] += 1

    

    



    return data_list_copy, zaeler
    
korrumpierte_list, zaeler = fehler_injektion(saubere_liste, daten_typen)

# CSV schreiben

with open("artikel_roh.csv", "w", newline = "", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=daten_typen)
    writer.writeheader()
    writer.writerows(korrumpierte_list)

# Baseline schreiben
with open("fehler_baseline.md", "w", encoding="utf-8") as f:
    f.write("# Fehler-Baseline\n\n| Fehlerart | Anzahl |\n|---|---|\n")
    for fehlerart, anzahl in zaeler.items():
        f.write(f"| {fehlerart} | {anzahl} |\n")