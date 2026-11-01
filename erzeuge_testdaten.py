import random

data_list = []
random.seed(42)

for i in range(200):
    single_data_dict = {"artikelnummer":"","bezeichnung":"", "material": "", "gewicht":"", "preis": "", "lieferant": "", "letzte_aenderung": "" }

    single_data_dict["artikelnummer"] = f"A-{1001 + i}"



    data_list.append(single_data_dict)
    
