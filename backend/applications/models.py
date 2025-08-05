from django.db import models
from users.models import User
from jobs.models import Job

class Application(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('reviewed', 'Reviewed'),
        ('rejected', 'Rejected'),
        ('selected', 'Selected'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='job_applications')
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='applications')
    resume = models.FileField(upload_to='resumes/')
    cover_letter = models.TextField(blank=True)
    applied_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return f"{self.user.username} - {self.job.title}"
