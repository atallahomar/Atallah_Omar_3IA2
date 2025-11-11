from django.shortcuts import render
from .models import Conference , Submission
from django.views.generic import ListView , DetailView , CreateView,UpdateView,DeleteView
from django.urls import reverse_lazy
from .forms import ConferenceForm,SubmissionForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseForbidden
# Create your views here.


def list_conferences(request):
    conferences_list=Conference.objects.all()
    """retour : liste + page """
    return render(request,"conferences/liste.html", {"liste":conferences_list})

class ConferenceList(ListView):
    model=Conference
    context_object_name="liste"
    template_name="conferences/liste.html"

class ConferenceDetails(DetailView):
    model=Conference
    context_object_name="conference"
    template_name="conferences/details.html"

class ConferenceCreate(LoginRequiredMixin,CreateView):
    model= Conference
    template_name ="conferences/form.html"
    #fields = "__all__"
    form_class =ConferenceForm
    success_url = reverse_lazy("liste_conferences")

class ConferenceUpdate(LoginRequiredMixin,UpdateView):
    model =Conference
    template_name="conferences/form.html"
    #fields="__all__"
    form_class =ConferenceForm
    success_url=reverse_lazy("liste_conferences")

class ConferenceDelete(LoginRequiredMixin,DeleteView):
    model=Conference
    template_name ="conferences/conference_confirm_delete.html"
    success_url =reverse_lazy("liste_conferences")

class SubmissionList(ListView):
    model = Submission
    context_object_name = "liste"
    template_name = "submissions/liste.html"  
    def get_queryset(self):
        return Submission.objects.filter(user=self.request.user)

class SubmissionDetails(DetailView):
    model = Submission
    context_object_name = "submission"
    template_name = "submissions/details.html"
class SubmissionCreate(LoginRequiredMixin,CreateView):
    model = Submission
    form_class = SubmissionForm
    template_name = "submissions/form.html"
    success_url = reverse_lazy("submission_list")

    def form_valid(self, form):
        form.instance.user = self.request.user 
        return super().form_valid(form)
    
class SubmissionUpdate(LoginRequiredMixin,UpdateView):
    model = Submission
    form_class = SubmissionForm
    template_name = "submissions/form.html"
    success_url = reverse_lazy("submission_list")
    def get_form(self, *args, **kwargs):
        form = super().get_form(*args, **kwargs)
        form.fields['title'].disabled = False
        form.fields['abstract'].disabled = False
        form.fields['keywords'].disabled = False
        form.fields['paper'].disabled = False

        for field in ['conference', 'user', 'submission_id', 'submission_date']:
            if field in form.fields:
                form.fields[field].disabled = True
        return form
    def dispatch(self, request, *args, **kwargs):
        submission = self.get_object()
        if submission.status in ['accepted', 'rejected']:
            return HttpResponseForbidden(f"Cette soumission ne peut pas être modifiée car elle est {submission.status}.")
        return super().dispatch(request, *args, **kwargs)
    