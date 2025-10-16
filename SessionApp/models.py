from django.db import models
from ConferenceApp.models import Conference
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
# Create your models here.
room_validator = RegexValidator(
    regex=r'^[a-zA-Z0-9]+$',
    message="Le nom de la salle ne doit contenir que des lettres et des chiffres."
)


class Session(models.Model):
    session_id=models.AutoField(primary_key=True)
    title=models.CharField(max_length=255)
    topic=models.CharField(max_length=255)
    session_day=models.DateField()
    start_time=models.TimeField()
    end_time=models.TimeField()
    room=models.CharField(max_length=255,validators=[room_validator])
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    #conference=models.ForeignKey("ConferenceApp.Conference",on_delete=models.CASCADE,related_name="sessions")
    conference=models.ForeignKey(Conference, on_delete=models.CASCADE,related_name="sessions")
    def clean(self):
        self.validate_session_day()
        self.validate_time()
        
    def validate_session_day(self):
        if self.conference:
            if not (self.conference.start_date <= self.session_day <= self.conference.end_date):
                raise ValidationError(
                    {"session_day": (
                        f"La date de la session doit être comprise entre "
                        f"{self.conference.start_date} et {self.conference.end_date}."
                    )}
                )

    def validate_time(self):
        if self.start_time and self.end_time:
            if self.start_time >= self.end_time:
                raise ValidationError(
                    {"start_time": "L'heure de début doit être inférieure à l'heure de fin."}
                )

