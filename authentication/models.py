from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class User(AbstractUser):
    MALE = 'M'
    FEMALE = 'F'
    SEX = [(FEMALE, 'Female'), (MALE, "Male")]

    HR = "hr"
    EMPLOYEE = "employee"
    UNKNOWN = "unknown"
    ROLE = [(HR, HR), (EMPLOYEE, EMPLOYEE), (UNKNOWN, UNKNOWN)]

    sex = models.CharField(max_length=1, choices=SEX, default=MALE)
    role = models.CharField(max_length=8, choices=ROLE, default=UNKNOWN)
