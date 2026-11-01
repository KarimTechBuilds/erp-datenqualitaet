import random
from datetime import date, timedelta
import copy

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
    daten_typen_int = ["preis","gewicht"]
    daten_typen_str = ["artikelnummer", "bezeichnung", "material", "lieferant", "letzte_aenderung"]
    data_list_copy = copy.deepcopy(list_of_data)

    # Exaktes Zeilenduplikat

    datensatz_zum_kopieren = copy.deepcopy(data_list_copy[random.randint(0, 199)])
    data_list_copy.append(datensatz_zum_kopieren)
    data_list_copy.insert(random.randint(0, len(data_list_copy)-1), datensatz_zum_kopieren)

    # Logisches Duplikat

    datensatz_falsch_ID = copy.deepcopy(data_list_copy[random.randint(0, len(data_list_copy)-1)])
    datensatz_falsch_ID["artikelnummer"] = "A-" + str(random.randint(1000, 9999))
    data_list_copy.insert(random.randint(0, len(data_list_copy)-1), datensatz_falsch_ID)

    # ID-Kollision

    datensatz_ID_kollision = copy.deepcopy(data_list_copy[random.randint(0, len(data_list_copy)-1)])
    datensatz_ID_kollision["artikelnummer"] = data_list_copy[random.randint(0, 199)]["artikelnummer"]
    data_list_copy.insert(random.randint(0, len(data_list_copy)-1), datensatz_ID_kollision)

    # Fehlende Werte

    datensatz_fehlenden_Wert = copy.deepcopy(data_list_copy[random.randint(0, len(data_list_copy)-1)])
    datensatz_fehlenden_Wert[random.choice(daten_typen)] = None
    data_list_copy.insert(random.randint(0, len(data_list_copy)-1), datensatz_fehlenden_Wert)

    # Falsche Datentypen

    datensatz_falsche_datentyp = copy.deepcopy(data_list_copy[random.randint(0, len(data_list_copy)-1)])
    datensatz_falsche_datentyp[random.choice(daten_typen_str)] = data_list_copy[random.randint(0, len(data_list_copy)-1)][random.choice(daten_typen_int)]
    datensatz_falsche_datentyp[random.choice(daten_typen_int)] = data_list_copy[random.randint(0, len(data_list_copy)-1)][random.choice(daten_typen_str)]
    data_list_copy.insert(random.randint(0, len(data_list_copy)-1), datensatz_falsche_datentyp)



    return data_list_copy
    
korrumpierte_liste = fehler_injektion(saubere_liste, daten_typen)