from django.db import models

from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from rest_framework.authtoken.models import Token
from phonenumber_field.modelfields import PhoneNumberField

#from django.contrib.contenttypes.fields import GenericForeignKey
#from django.contrib.contenttypes.models import ContentType
#from django.contrib.contenttypes.fields import GenericRelation

import django.utils.timezone

class UserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('The Email must be set')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self.create_user(email, password, **extra_fields)

class User(AbstractUser):
    username=None
    email = models.EmailField(("Email Address"),primary_key=True)
    phone = PhoneNumberField(blank = True)
    department = models.CharField(blank = True, null = True, max_length = 63)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS=[]

    objects = UserManager()

    def __str__(self):
        return self.email

    @property
    def token(self):
        token = Token.objects.get(user=User.objects.get(self.id))
        return token

class Profile(models.Model):
    EMPLOYEE = 'Employee'
    TEAM_LEADER = 'Team Leader'
    ADMIN = 'Admin'
    ROLE_CHOICES = ((EMPLOYEE, 'Employee'),(TEAM_LEADER, 'Team Leader'),(ADMIN, 'Admin'),)

    role = models.CharField(choices = ROLE_CHOICES, default = '1', max_length = 15)
    user = models.OneToOneField(User, on_delete = models.CASCADE, primary_key = True)
    joining_date = models.DateField(default = django.utils.timezone.now)
    picture = models.ImageField(upload_to = 'profiles/', blank = True)

    def __str__(self):
        return self.user.email

def upload_path_handler(instance, filename):
    return "fingerprints/{title}/{file}".format(
        title=instance.profile.user.email, file=filename
    )

class FingerPrint(models.Model):
    profile = models.ForeignKey(Profile, on_delete = models.CASCADE)
    finger_type = models.CharField(max_length = 15)
    finger_hand = models.CharField(max_length = 15)
    fingerprint = models.ImageField(upload_to = upload_path_handler, blank = True)

    def __str__(self):
        return f"{self.profile.user.email} - {self.finger_hand} {self.finger_type}"

class Location(models.Model):
    profile = models.ForeignKey(Profile, on_delete = models.CASCADE)
    lat = models.CharField(max_length = 31)
    long = models.CharField(max_length = 31)
    date = models.DateField(default = django.utils.timezone.now)
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return f"{self.profile.user.email} - {self.date}"

class Attendance(models.Model):
    profile = models.ForeignKey(Profile, on_delete = models.CASCADE)
    date = models.DateField(default = django.utils.timezone.now)
    hours_assigned = models.FloatField()
    hours_present = models.FloatField(default = 0.0)
    type = models.CharField(max_length = 31)

    def __str__(self):
        return f"{self.profile.user.email} - {self.date}"

def upload_log_handler(instance, filename):
    return "logs/{date}/{emp}/{file}".format(
        date=str(instance.log_for.date), emp = instance.profile.user.email, file=filename
    )

class Timer(models.Model):
    log_for = models.ForeignKey(Attendance, on_delete = models.CASCADE)
    lat = models.CharField(max_length = 31)
    long = models.CharField(max_length = 31)
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_active = models.BooleanField(default = True)
    log_picture = models.ImageField(upload_to = upload_log_handler, blank = True)

    def __str__(self):
        return f"{self.log_for.profile.user.email} - {self.log_for.date}({self.start_time} {self.end_time})"

class Efficiency(models.Model):
    profile = models.ForeignKey(Profile, on_delete = models.CASCADE)
    efficiency = models.FloatField(default = 0.0)
    month = models.CharField(max_length = 15)
    year = models.PositiveIntegerField(default = int(django.utils.timezone.now().year))
    
    def __str__(self):
        return f"{self.profile.user.email} - {self.month} {self.year}"

class Project(models.Model):
    leader = models.ForeignKey(Profile, on_delete = models.CASCADE)
    title = models.CharField(max_length = 127, unique = True)
    description = models.TextField(max_length = 1023, blank = True, null = True)
    status = models.PositiveIntegerField(default = 0)
    deadline =  models.DateTimeField()
    no_of_employees = models.PositiveIntegerField(default = 1)

    def __str__(self):
        return self.title

class ProjectEmployee(models.Model):
    project = models.ForeignKey(Project, on_delete = models.CASCADE)
    member = models.ForeignKey(Profile, on_delete = models.CASCADE)

    def __str__(self):
        return self.project.title

class Task(models.Model):
    assigned_by = models.ForeignKey(Profile, on_delete = models.CASCADE, related_name='task_assigned_by')
    assigned_to = models.ForeignKey(Profile, on_delete = models.CASCADE, related_name='task_assigned_to')
    project = models.ForeignKey(Project, on_delete = models.CASCADE, blank = True, null = True)
    title = models.CharField(max_length = 127)
    description = models.TextField(max_length = 1023, blank = True, null = True)
    for_project = models.BooleanField(default = False)
    due_time =  models.DateTimeField()
    closing_time =  models.DateTimeField()
    is_complete = models.BooleanField(default = False)
    rating = models.PositiveIntegerField(default = 0)

    def __str__(self):
        return self.title

class Review(models.Model):
    given_by = models.ForeignKey(Profile, on_delete = models.CASCADE, related_name='review_given_for')
    given_for = models.ForeignKey(Profile, on_delete = models.CASCADE, related_name='review_given_by')
    project = models.ForeignKey(Project, on_delete = models.CASCADE, blank = True, null =True)
    rating = models.PositiveIntegerField(default = 1)
    description = models.TextField(max_length = 1023)

class Meeting(models.Model):
    created_by = models.ForeignKey(Profile, on_delete = models.CASCADE, related_name='meeting_created_by')
    project = models.ForeignKey(Project, on_delete = models.CASCADE, blank = True, null =True)
    title = models.CharField(max_length = 127)
    description = models.TextField(max_length = 1023, blank = True, null = True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    mode = models.CharField(max_length = 127)
    for_project = models.BooleanField(default = False)

    def __str__(self):
        return self.title

class Attendee(models.Model):
    attendee = models.ForeignKey(Profile, on_delete = models.CASCADE)
    meeting = models.ForeignKey(Meeting, on_delete = models.CASCADE)

    def __str__(self):
        return self.meeting.title

class Notification(models.Model):
    sender = models.ForeignKey(Profile, on_delete = models.CASCADE, related_name='notification_sender')
    receiver = models.ForeignKey(Profile, on_delete = models.CASCADE, related_name='notification_receiver')
    title = models.CharField(max_length = 127)
    description = models.TextField(max_length = 1023, blank = True, null = True)
    sent_at = models.DateTimeField(auto_now_add = True)