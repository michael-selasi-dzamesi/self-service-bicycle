import requests
import json

def getLilleData():
    url = "https://opendata.lillemetropole.fr/api/records/1.0/search/?dataset=vlille-realtime&q=&rows=3000&facet=libelle&facet=nom&facet=commune&facet=etat&facet=type&facet=etatconnexion"
    response = requests.request("GET", url)
    json_response = json.loads(response.text.encode('utf8'))
    return json_response.get("records",[])
