from django.contrib import admin
from .models import User,OrganizingComitee
# Regimodelster your models here.

admin.site.register(OrganizingComitee)

class CommiteeInlineAdmin(admin.StackedInline):
    model = OrganizingComitee
    extra = 1
    readonly_fields=("comitee_role","join_date")

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("user_id", "first_name", "last_name", "email", "role")
    list_editable = ("role",)
    ordering = ("first_name", "last_name")
    list_filter = ("role",)
    search_fields = ( "first_name", "last_name", "email")
    readonly_fields = ("user_id",)
    list_per_page = 10


    inlines = [CommiteeInlineAdmin]
