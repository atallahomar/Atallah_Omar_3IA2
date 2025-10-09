from django.contrib import admin
from .models import Conference , Submission
# Register your models here.
admin.site.site_title="Gestion Conférence 25/26"
admin.site.site_header="Gestion Conférences"
admin.site.index_title="django app conférence"
admin.site.register(Conference)
admin.site.register(Submission)