from django.urls import path
from .views import *
urlpatterns =[
    path("liste/",ConferenceList.as_view(),name="liste_sessions"),
    path("<int:pk>/",ConferenceDetails.as_view(),name="sessions_details"),
    path("add/",ConferenceCreate.as_view(),name="sessions_add"),
    path("edit/<int:pk>/",ConferenceUpdate.as_view(),name="sessions_update"),
    path("delete/<int:pk>/",ConferenceDelete.as_view(),name="sessions_delete"),

]