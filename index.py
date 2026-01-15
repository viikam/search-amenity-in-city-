import requests
import argparse


###Défninitions des fonctions###

def count_things(nom_ville, things)-> int:
    overpass_url = "https://overpass-api.de/api/interpreter"
    """compte le nombres de choses demandés dans une ville  """
    query = f"""
    [out:json][timeout:90];
    area["name"="{nom_ville}"]["admin_level"="8"]->.a;

    nwr[amenity="{things}"](area.a);
    out count;
    """

    reponse = requests.get(overpass_url, data={'data': query})
    
    while reponse.status_code == 504:
        reponse = requests.get(overpass_url, data={'data': query})

    if reponse.status_code != 200:
        return f"Erreur {reponse.status_code} lors de la requête Overpass API"
        
    try:
        data = reponse.json()
        elements = data.get('elements', [])
        if elements:
            total = elements[0].get('tags', {}).get('total', 0)
            return f"À {nom_ville}, il y a {int(total)} {things}."
        return 0
        
    except (ValueError, KeyError, IndexError):
        return "Erreur lors de la lecture des données JSON"



print (count_things("Caen", "hospital"))  
    



