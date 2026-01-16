from django.db import models

# Create your models here.
from django.db import models
from django.core.validators import MaxLengthValidator,MinLengthValidator

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


class AddEmployee(models.Model):
    name = models.CharField(max_length=100,validators=[MaxLengthValidator(10),MinLengthValidator(3)],error_messages={
            'min_length': 'Name must contain at least 3 characters.',
            'max_length': 'Name cannot exceed 10 characters.'
        }
 )
    email = models.EmailField(unique=True)
    contact = models.CharField(max_length=15)
    image = models.ImageField(upload_to='employee_images/', blank=True, null=True)
    password = models.CharField(max_length=128)
    department=models.CharField(max_length=50,null=True)
    d_code = models.CharField(max_length=20,null=True)
    d_des = models.CharField(max_length=50,null=True)


    def __str__(self):
        return self.name

class Department(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.name} ({self.code})"

class Query(models.Model):
    name = models.CharField(max_length=20)
    email = models.EmailField()
    query =  models.CharField(max_length=200)
    subject = models.CharField(max_length=50) 
    status =  models.CharField(max_length=10,default='panding')
    solution = models.CharField(max_length=100,null=True)
    created_at = models.DateTimeField(auto_now_add=True,null=True)

    
