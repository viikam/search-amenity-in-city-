### imports

import requests
import argparse
import time 
from geopy.geocoders import Nominatim
from tohtml import tohtml

### definition des fonctiions 

def infos_pays_pour_overpass(nom_ville):
    """recherche gràcae l'api geopy le pays correspondant à la ville demandé"""
    geolocator = Nominatim(user_agent="search_country", timeout=10)
    
    location = geolocator.geocode(nom_ville, addressdetails=True)
    if location and 'address' in location.raw:
        return location.raw['address'].get('country_code', '').upper()
   
def count_things(nom_ville: str, code_pays: str, things: str):
    overpass_url = "https://overpass-api.de/api/interpreter"
    
    query = f"""
    [out:json][timeout:360];
    area["ISO3166-1"="{code_pays}"]["admin_level"="2"]->.p;

    (
        area["name"="{nom_ville}"]["admin_level"="8"](area.p);
        area["name"="{nom_ville}"]["admin_level"="7"](area.p);
        area["name"="{nom_ville}"]["admin_level"="6"](area.p);
        area["name"="{nom_ville}"]["admin_level"="5"](area.p);
    )->.v;


    
    nwr[amenity="{things}"](area.v);
    out count;
    
    nwr[amenity="{things}"](area.p);
    out count;
    """
    
    reponse = requests.get(overpass_url, params={'data': query})
    while reponse.status_code == 504:
        time.sleep(3)
        reponse = requests.get(overpass_url, params={'data': query})

    if reponse.status_code == 200:
        data = reponse.json()
        elements = data.get('elements', [])
        if len(elements) >= 2:
            c_pays = elements[1].get('tags', {}).get('total', 0)
            c_ville = elements[0].get('tags', {}).get('total', 0)
            return int(c_ville), int(c_pays)

def compute_statist(tot_v, tot_p):
    """calcul le pourcentage de amenity par rapport aux amninity dans le pays"""
    if tot_p == 0:
        return 0
    return (tot_v / tot_p) * 100

def tomd(tot_v, tot_p, ville, pays, truc):
    """Ouvre où crée  un fichier md et ecrit dedans les infos """
    with open("markdown.md", "w+", encoding="utf-8") as f:
        f.write(f"# Résultats pour {truc}\n\n")
        f.write(f"* À **{ville}**, il y a **{tot_v}** {truc}(s).\n")
        f.write(f"* Dans toute la **{pays}**, il y en a **{tot_p}**.\n")
        f.write (f"* Statistiquement, À {ville} il y a  environ  **{round(compute_statist(tot_v,tot_p), 3)} % **des {truc} de {pays}.\n")


### main

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("c", help="ville (veillez bien mettre les accents)")
    parser.add_argument("a", help="amenity")
    pars = parser.parse_args()

    ville = str(pars.c)
    ville = str(ville.title())

    print(f"Recherche du pays pour {ville}...")
    pays = infos_pays_pour_overpass(ville)
    
    if pays:
        print(f"Pays identifié : {pays}. Comptage en cours...")
        tot_v, tot_p = count_things(ville, pays, pars.a)
        
        if tot_v is not None:
            tomd(tot_v, tot_p, ville, pays, pars.a)
            tohtml("markdown")
            print(f"Ville: {tot_v} | Pays: {tot_p}")
        else:
            print("Erreur lors de la récupération des données Overpass.")
    else:
        print("Impossible de localiser la ville.")