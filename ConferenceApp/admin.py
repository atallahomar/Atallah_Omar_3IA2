from django.contrib import admin
from .models import Conference , Submission
from django.utils import timezone

# Register your models here.
admin.site.site_title="Gestion Conférence 25/26"
admin.site.site_header="Gestion Conférences"
admin.site.index_title="django app conférence"
#admin.site.register(Conference)
admin.site.register(Submission)

class SubmissionInlineadmin(admin.StackedInline):
    model= Submission
    extra=1
    readonly_fields=("submission_date",)
    fieldsets = (
        ("Informations sur la soumission", {
            "fields": ("title", "abstract", "keywords", "paper")
        }),
        ("Statut et paiement", {
            "fields": ("status", "payed")
        })
    )

@admin.register(Conference)
class adminConferenceModel(admin.ModelAdmin):
    list_display = ("name", "theme", "location", "start_date", "end_date", "duration" , "is_past")
    list_editable = ("theme",)
    ordering=("start_date",)
    list_filter=("theme",)
    search_fields=("description","name")
    date_hierarchy="start_date"
    fieldsets=(
        ("information general",{
            "fields":("conference_id","name","theme","description")
        }),
        ("logistics info",{
            "fields":("location","start_date","end_date")
        })
    )
    readonly_fields=("conference_id",)
    def duration(self,objet):
        if objet.start_date and objet.end_date :
            return (objet.end_date-objet.start_date ).days
        return"RAS"
    duration.short_description="Duration (days)"
    def is_past(self, objet):
        return objet.end_date < timezone.now().date()
    is_past.boolean = True  
    is_past.short_description ="Déjà passée ?"

    list_per_page = 10
    inlines=[SubmissionInlineadmin]