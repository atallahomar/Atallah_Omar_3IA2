from django import forms
from .models import Session

class sessionForm(forms.ModelForm):
    class Meta:
        model=Session
        fields=['title','topic','session_day','start_time','end_time','room']
        widgets ={
            'session_day' : forms.DateInput(
                attrs ={
                    'type':"date"
                }
            ),
            'start_time' : forms.TimeInput(
                attrs ={
                    'type':"date"
                }
            ),
            'end_time' : forms.TimeInput(
                attrs ={
                    'type':"date"
                }
            )
        }

