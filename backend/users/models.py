from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    EMPLOYER = 'employer'
    JOB_SEEKER = 'job_seeker'

    ROLE_CHOICES = [
        (EMPLOYER, 'Employer'),
        (JOB_SEEKER, 'Job Seeker'),
    ]
    

    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    full_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)

    def __str__(self):
        return f"{self.username} ({self.role})"

class JobSeekerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='jobseeker_profile')
    skills = models.TextField(blank=True)
    resume = models.FileField(upload_to='resumes/', blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}'s Job Seeker Profile"

class EmployerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='employer_profile')
    company_name = models.CharField(max_length=255)
    company_logo = models.ImageField(upload_to='company_logos/', blank=True, null=True)
    website = models.URLField(blank=True)

    def __str__(self):
        return self.company_name
