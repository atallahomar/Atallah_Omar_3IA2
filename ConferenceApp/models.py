import string
import random
from django.db import models
from UserApp.models import User
from django.core.validators import MinLengthValidator
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.utils import timezone

# Create your models here.
def generate_submission_id():
    while True:
        random_string = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
        submission_id = f"SUB-{random_string}"
        if not Submission.objects.filter(submission_id=submission_id).exists():
            return submission_id
        

class Conference(models.Model):
    conference_id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=255)
    THEME=[
        ("IA","Computer Science & ia"),
        ("SE","Science & eng"),
        ("SC","Social sciences"),
        ("IT","Interdisciplinary Themes"),
    ]
    theme=models.CharField(max_length=255,choices=THEME)
    location=models.CharField(max_length=50)
    description=models.TextField(validators=[MinLengthValidator(30,"vous devez ecrire au moins 30 lettres ")])
    start_date=models.DateField()
    end_date=models.DateField()
    created_at=models.DateTimeField(auto_now_add=True) 
    updated_at=models.DateTimeField(auto_now=True)
    def clean(self):
        if self.start_date >self.end_date :
            raise ValidationError("la date de debut doit etre inferieur à la date fin")

def validate_keywords(keywords):
    mots = [mot.strip() for mot in keywords.split(',') if mot.strip()]
    if len(mots) > 10:
        raise ValidationError("Vous ne pouvez pas avoir plus de 10 mots-clés.")

class Submission(models.Model):
    submission_id=models.CharField(max_length=255,primary_key=True,unique=True,editable=False,default=generate_submission_id)
    title=models.CharField(max_length=50)
    abstract=models.TextField()
    keywords=models.TextField(validators=[validate_keywords])
    paper=models.FileField(upload_to="papers/",validators=[FileExtensionValidator(allowed_extensions=['pdf'], message="Seuls les fichiers PDF sont autorisés.")])
    STATUS=[
        ("submitted","submitted"),
        ("under review","under review"),
        ("accepted","accepted"),
        ("rejected","rejected"),
    ]
    status=models.CharField(max_length=50,choices=STATUS)
    payed=models.BooleanField(default=False)
    submission_date=models.DateField(auto_now_add=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name="submissions")
    conference=models.ForeignKey(Conference,on_delete=models.CASCADE,related_name="submissions")
    def clean(self):
    
        if self.conference and self.conference.start_date < timezone.now().date():
            raise ValidationError({"conference": "Vous ne pouvez pas soumettre pour une conférence déjà commencée ou passée."})

        
        if self.user: 
            submissions_today = Submission.objects.filter(
                user=self.user,
                submission_date=timezone.now().date()
            ).exclude(submission_id=self.submission_id).count()

            if submissions_today >= 3:
                raise ValidationError({"user": "Vous ne pouvez pas soumettre plus de 3 conférences par jour."})



