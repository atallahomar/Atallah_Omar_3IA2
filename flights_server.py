from mcp.server.fastmcp import FastMCP
import os
import json
from datetime import datetime



app = FastMCP(name="Aéroport Info")
FLIGHTS_PATH = os.path.join(os.path.dirname(__file__), "flights.json")



def _load_flights():
    with open(FLIGHTS_PATH, "r", encoding="utf-8") as f:
        return json.load(f).get("flights", [])
    
@app.resource("flights://today")
def flights_resource():
    """
    Resource qui expose la liste des vols du jour.
    L'URL 'flights://today' sera visible par Copilot/Claude.
    """
    with open(FLIGHTS_PATH, "r", encoding="utf-8") as f:
        return f.read()

@app.tool()
def find_flight(flight_number: str) -> str:
    """Trouve un vol par son numéro (ex: AF1234)"""
    flights = _load_flights()
    for flight in flights:
        if flight.get("flight_number", "").upper() == flight_number.upper():
            return f"""✈️ Vol {flight["flight_number"]} ({flight["airline"]})
                        {flight["departure_city"]} → {flight["arrival_city"]}
                        Départ : {flight["departure_time"]} | Arrivée :
                            {flight["arrival_time"]}
                        Statut : {flight["status"]}"""
    return f"Vol {flight_number} non trouvé aujourd'hui."

@app.tool()
def flights_to(destination: str) -> str:
    """Liste tous les vols à destination d'une ville aujourd'hui."""
    flights = _load_flights()
    matches = [f for f in flights if destination.lower() in f["arrival_city"].lower()]
    if not matches:
        return f"Aucun vol trouvé vers {destination.title()} aujourd'hui."
    result = f"Vols vers {destination.title()} ({len(matches)} trouvé(s)) :\n\n"
    for f in matches:
        result += f"• {f['flight_number']} ({f['airline']}) → {f['arrival_city']} à {f['arrival_time']} – {f['status']}\n"
    return result.strip()
    
@app.tool()
def flights_by_status(status: str) -> str:
    """
    Renvoie les vols ayant un statut particulier (ex : 'retardé', 'annulé', 'à l'heure').
    """
    flights = _load_flights()
    matches = [f for f in flights if  status.lower() == f["status"].lower()]

    if not matches:
        return f"Aucun vol trouvé avec le statut '{status}'."

    result = f"Vols ayant le statut '{status}' ({len(matches)} trouvé(s)) :\n\n"
    for f in matches:
        result += (
            f"• {f['flight_number']} ({f['airline']}) – "
            f"{f['departure_city']} → {f['arrival_city']} | "
            f"Départ {f['departure_time']} – {f['status']}\n"
        )
    return result.strip()
@app.tool()
def flights_by_airline(airline: str) -> str:
    """
    Renvoie tous les vols opérés par une compagnie aérienne donnée.
    Exemple : 'Air France', 'easyJet', 'British Airways'
    """
    flights = _load_flights()

    matches = [
        f for f in flights
        if airline.lower() in f.get("airline", "").lower()
    ]

    if not matches:
        return f"Aucun vol trouvé pour la compagnie '{airline}'."

    result = f"Vols opérés par {airline.title()} ({len(matches)} trouvé(s)) :\n\n"

    for f in matches:
        result += (
            f"• {f['flight_number']} – {f['departure_city']} → {f['arrival_city']} "
            f"({f['departure_time']} → {f['arrival_time']}) – Statut : {f['status']}\n"
        )

    return result.strip()


if __name__ == "__main__":
    app.run(transport="stdio")