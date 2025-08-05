from django.db import models
from users.models import User

class Job(models.Model):
    employer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='jobs')
    title = models.CharField(max_length=100)
    description = models.TextField()
    location = models.CharField(max_length=100)
    salary_min = models.IntegerField()
    salary_max = models.IntegerField()
    posted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
