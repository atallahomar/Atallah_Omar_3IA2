from django.shortcuts import render
from .models import Session
from django.views.generic import ListView,DetailView,CreateView,UpdateView,DeleteView
from django.urls import reverse_lazy
from .forms import sessionForm
# Create your views here.
class ConferenceList(ListView):
    model=Session
    context_object_name="liste"
    template_name="sessions/liste.html"
    ordering = ["start_date"]

class ConferenceDetails(DetailView):
    model=Session
    context_object_name="conference"
    template_name="sessions/details.html"

class ConferenceCreate(CreateView):
    model= Session
    template_name ="sessions/form.html"
    #fields = "__all__"
    form_class =sessionForm
    success_url = reverse_lazy("liste_conferences")

class ConferenceUpdate(UpdateView):
    model =Session
    template_name="sessions/form.html"
    #fields="__all__"
    form_class =sessionForm
    success_url=reverse_lazy("liste_conferences")

class ConferenceDelete(DeleteView):
    model=Session
    template_name ="sessions/conference_confirm_delete.html"
    success_url =reverse_lazy("liste_conferences")