from django.db import models

from departments.models import Department
from skills.models import Skill


class Student(models.Model):

    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    ]

    CITY_CHOICES = [
        ('Nashik', 'Nashik'),
        ('Pune', 'Pune'),
        ('Mumbai', 'Mumbai'),
        ('Nagpur', 'Nagpur'),
    ]

    first_name = models.CharField(
        max_length=100
    )

    last_name = models.CharField(
        max_length=100
    )

    email = models.EmailField(
        unique=True
    )

    mobile = models.CharField(
        max_length=10
    )

    dob = models.DateField()

    gender = models.CharField(
        max_length=10,
        choices=GENDER_CHOICES
    )

    address = models.TextField()

    city = models.CharField(
        max_length=50,
        choices=CITY_CHOICES
    )

    is_active = models.BooleanField(
        default=True
    )

    department = models.ForeignKey(
        Department,
        on_delete=models.CASCADE
    )

    skills = models.ManyToManyField(
        Skill
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return f"{self.first_name} {self.last_name}"