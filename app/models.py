from django.db import models

# Create your models here.
from django.db import models
from datetime import time
from django.core.validators import MaxLengthValidator,MinLengthValidator
from django.core.exceptions import ValidationError

# Create your models here.
class Employee(models.Model):
    name = models.CharField(max_length=20)
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

    def __str__(self):
      return f"{self.name} ({self.email})"

    # def__str__(self):
    # return str(self.contact)
    # return self name 
    # return f"{self.name}" - {self.email}
    # return f"{self.name}"

def Emp_contact(value):
    if not (len(str(value)) == 10 and value.isdigit()):
        raise ValidationError("Contact must be 10 digits only")

class AddEmployee(models.Model):

    name = models.CharField(
        max_length=100,
        validators=[MaxLengthValidator(10), MinLengthValidator(3)],
        error_messages={
            'min_length': 'Name must contain at least 3 characters.',
            'max_length': 'Name cannot exceed 20 characters.'
        }
    )

    email = models.EmailField(unique=True)

    contact = models.CharField(
        max_length=15,
        validators=[Emp_contact]
    )

    image = models.ImageField(
        upload_to='employee_images/',
        blank=True,
        null=True
    )

    password = models.CharField(max_length=128)

    department = models.CharField(max_length=50, null=True)

    d_code = models.CharField(max_length=20, null=True)

    d_des = models.CharField(max_length=50, null=True)
    joining_date = models.DateField(null=True, blank=True)

    salary = models.IntegerField(null=True, blank=True)

    


    def clean(self):

        if len(str(self.password)) < 4:
            raise ValidationError(
                "Password must be at least 4 characters long"
            )


    def save(self, *args, **kwargs):

        self.full_clean()

        super().save(*args, **kwargs)


    def __str__(self):

        return f"{self.name} ({self.email})"

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
    status =  models.CharField(max_length=10,default='pending')
    solution = models.CharField(max_length=100,null=True)
    created_at = models.DateTimeField(auto_now_add=True,null=True)


from django.db import models
from datetime import date

class Attendance(models.Model):

    STATUS_CHOICES = (
        ('Present', 'Present'),
        ('Absent', 'Absent'),
        ('Half Day', 'Half Day'),
    )

    employee = models.ForeignKey(AddEmployee, on_delete=models.CASCADE)
    date = models.DateField(default=date.today)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)

    check_in_time = models.TimeField(
    null=True,
    blank=True
)
    late_fine = models.IntegerField(default=0)
    final_salary = models.FloatField(default=0)

    class Meta:
        unique_together = ('employee', 'date')

    def __str__(self):
        return f"{self.employee.name} - {self.date}"
    

@property
def late_fine(self):

    if self.status == "Present":

        if self.check_in_time and self.check_in_time > time(9, 30) and self.check_in_time <= time(10, 0):

            return 50

        elif self.check_in_time and self.check_in_time > time(10, 0):

            monthly_salary = self.employee.salary
            per_day_salary = monthly_salary / 30

            return per_day_salary / 2

    return 0


@property
def final_salary(self):

    monthly_salary = self.employee.salary

    per_day_salary = monthly_salary / 30

    # PRESENT
    if self.status == "Present":

        # 9:30 to 10
        if self.check_in_time and self.check_in_time > time(9, 30) and self.check_in_time <= time(10, 0):

            return per_day_salary - 50

        # after 10
        elif self.check_in_time and self.check_in_time > time(10, 0):

            return per_day_salary / 2

        else:
            return per_day_salary

    # HALF DAY
    elif self.status == "Half Day":

        return per_day_salary / 2

    # ABSENT
    return 0

# models.py ke sabse niche ye code paste karo:

class Task(models.Model):
    STATUS_CHOICES = [
        ('TODO', 'To Do'),
        ('IN_PROGRESS', 'In Progress'),
        ('DONE', 'Done'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    # Kis employee ko task mila (Tumhare AddEmployee model se connect kiya)
    assigned_to = models.ForeignKey(AddEmployee, on_delete=models.CASCADE, related_name='tasks')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='TODO')
    created_at = models.DateTimeField(auto_now_add=True)
    due_date = models.DateField()
    progress_note = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.title} - {self.status}"