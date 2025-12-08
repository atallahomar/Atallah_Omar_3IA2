import os
import django
import asyncio
from asgiref.sync import sync_to_async

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "GestionConferrence3IA2.settings")
django.setup()

from ConferenceApp.models import Conference

# Define the list_conferences function
@sync_to_async
def _query():
    return list(Conference.objects.all())

async def list_conferences():
    """Lister toutes les conférences disponibles."""
    conferences = await _query()
    
    if not conferences:
        return "Aucune conférence trouvée."
    
    return "\n".join(
        [f"- {c.name} ({c.start_date} -> {c.end_date})" for c in conferences]
    )

# Run the function
result = asyncio.run(list_conferences())
print(result)
