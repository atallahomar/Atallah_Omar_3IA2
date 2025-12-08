import os
import django
from fastmcp import FastMCP
from asgiref.sync import sync_to_async
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), 'GestionConferrence3IA2'))

# Set Django settings module
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "GestionConferrence3IA2.settings")

import django
django.setup()
from ConferenceApp.models import Conference
from SessionApp.models import Session

# ----------------------------
# Création du serveur MCP
# ----------------------------
mcp = FastMCP("Conference Assistant")

# --------------------------------------------------------------------
# TOOL 1 : Lister toutes les conférences
# --------------------------------------------------------------------
@mcp.tool()
async def list_conferences() -> str:
    """Lister toutes les conférences disponibles."""
    @sync_to_async
    def _query():
        return list(Conference.objects.all())

    conferences = await _query()

    if not conferences:
        return "Aucune conférence trouvée."

    return "\n".join(
        [f"- {c.name} ({c.start_date} → {c.end_date})" for c in conferences]
    )

# --------------------------------------------------------------------
# TOOL 2 : Détails d'une conférence
# --------------------------------------------------------------------
@mcp.tool()
async def get_conference_details(name: str) -> str:
    """Obtenir les détails complets d'une conférence spécifique."""
    @sync_to_async
    def _query():
        try:
            return Conference.objects.get(name__icontains=name)
        except Conference.DoesNotExist:
            return None
        except Conference.MultipleObjectsReturned:
            return "MULTIPLE"

    conference = await _query()

    if conference == "MULTIPLE":
        return f"Plusieurs conférences correspondent à '{name}'. Veuillez préciser."

    if conference is None:
        return f"Aucune conférence trouvée avec le nom '{name}'."

    return (
        f"Nom: {conference.name}\n"
        f"Thème: {conference.get_theme_display()}\n"
        f"Lieu: {conference.location}\n"
        f"Dates: {conference.start_date} → {conference.end_date}\n"
        f"Description: {conference.description}"
    )

# --------------------------------------------------------------------
# TOOL 3 : Lister les sessions d'une conférence
# --------------------------------------------------------------------
@mcp.tool()
async def list_sessions(conference_name: str) -> str:
    """Lister toutes les sessions pour une conférence donnée."""
    @sync_to_async
    def _query():
        try:
            conf = Conference.objects.get(name__icontains=conference_name)
            return list(conf.sessions.all()), conf
        except Conference.DoesNotExist:
            return None, None
        except Conference.MultipleObjectsReturned:
            return "MULTIPLE", None

    result, conference = await _query()

    if result == "MULTIPLE":
        return f"Plusieurs conférences correspondent à '{conference_name}'. Veuillez préciser."

    if conference is None:
        return f"Aucune conférence trouvée avec le nom '{conference_name}'."

    if not result:
        return f"Aucune session trouvée pour la conférence '{conference.name}'."

    session_list = [
        f"- {s.title} ({s.start_time} → {s.end_time}) in {s.room}\n  Sujet: {s.topic}"
        for s in result
    ]

    return "\n".join(session_list)

# --------------------------------------------------------------------
# TOOL 4 : Filtrer les conférences par thème
# --------------------------------------------------------------------
@mcp.tool()
async def filter_conferences_by_theme(theme: str) -> str:
    """Filtrer les conférences par thème."""
    @sync_to_async
    def _query():
        return list(Conference.objects.filter(theme__icontains=theme))

    filtered = await _query()

    if not filtered:
        return f"Aucune conférence trouvée pour le thème '{theme}'."

    return "\n".join(
        [
            f"- {c.name} ({c.start_date} → {c.end_date}) — Thème: {c.get_theme_display()}"
            for c in filtered
        ]
    )

# --------------------------------------------------------------------
# Lancement du serveur MCP
# --------------------------------------------------------------------
if __name__ == "__main__":
    mcp.run(transport="stdio")
