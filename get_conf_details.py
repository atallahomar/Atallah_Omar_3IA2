import os
import django
import asyncio
from asgiref.sync import sync_to_async

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "GestionConferrence3IA2.settings")
django.setup()

from ConferenceApp.models import Conference

@sync_to_async
def _query(name):
    try:
        return Conference.objects.get(name__icontains=name)
    except Conference.DoesNotExist:
        return None
    except Conference.MultipleObjectsReturned:
        return "MULTIPLE"

async def get_conference_details(name: str):
    """Obtenir les détails complets d'une conférence spécifique."""
    conference = await _query(name)

    if conference == "MULTIPLE":
        return f"Plusieurs conférences correspondent à '{name}'. Veuillez préciser."

    if conference is None:
        return f"Aucune conférence trouvée avec le nom '{name}'."

    return (
        f"Nom: {conference.name}\n"
        f"Thème: {conference.get_theme_display()}\n"
        f"Lieu: {conference.location}\n"
        f"Dates: {conference.start_date} -> {conference.end_date}\n"
        f"Description: {conference.description}"
    )

# Run the function
result = asyncio.run(get_conference_details("cours"))
print(result)
