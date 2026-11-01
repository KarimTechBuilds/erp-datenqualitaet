import random
from datetime import date, timedelta
data_list = []
random.seed(42)

typen_liste = ["Schraube", "Mutter", "Bolzen", "Ventil", "Sensor", "Halterung"]
groessen_liste = ["M4", "M6", "M8", "klein", "gross", "10mm", "20mm"]
material_liste = ["Stahl", "Edelstahl", "Aluminium", "Kupfer", "Messing", "Kunststoff", "Titan"]
lieferant_liste = ["Karlsruhe Metallwerke", "Berlin Metallwerke", "Konstanz Metallwerke", "Aachen Metallwerke", "Stuttgart Metallwerke"]


for i in range(200):

    start_datum = date(2023, 1, 1)
    zufallstage = random.randint(0, 365)
    datum = start_datum + timedelta(days= zufallstage)

    single_data_dict = {"artikelnummer":"","bezeichnung":"", "material": "", "gewicht":"", "preis": "", "lieferant": "", "letzte_aenderung": "" }

    single_data_dict["artikelnummer"] = f"A-{1001 + i}"
    single_data_dict["bezeichnung"] = f"{random.choice(typen_liste)} {random.choice(groessen_liste)}"
    single_data_dict["material"] = random.choice(material_liste)
    single_data_dict["gewicht"] = round(random.uniform(0.1, 50.0), 2)
    single_data_dict["preis"] = round(random.uniform(1.0, 500.0), 2)
    single_data_dict["lieferant"] = f"{random.choice(lieferant_liste)}"
    single_data_dict["letzte_aenderung"] = str(datum)

    
    data_list.append(single_data_dict)
    
