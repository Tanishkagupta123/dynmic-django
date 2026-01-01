from django.db import models

# Create your models here.
from django.db import models

# Create your models here.
class Employee(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    contact = models.CharField()
    gender = models.CharField(max_length=10)
    qualification = models.CharField(max_length=200)
    state = models.CharField(max_length=50)
    image = models.ImageField(upload_to='images/')
    audio = models.FileField(upload_to='audios/')
    video = models.FileField(upload_to='videos/')
    resume = models.FileField(upload_to='resumes/')
    password=models.CharField(max_length=20,null=True)         ##table pehle se created  h ab isme naya column add krna h islie 


    # def__str__(self):
    # return str(self.contact)
    # return self name 
    # return f"{self.name}" - {self.email}
    # return f"{self.name}"


