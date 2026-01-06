from django.db import models

# Create your models here.
class Language(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name
    
class Concept(models.Model):
    language = models.ForeignKey(Language, on_delete=models.CASCADE, related_name='concepts')
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.language.name} - {self.name}"
    
class Task(models.Model):
    concept = models.ForeignKey(Concept, on_delete=models.CASCADE, related_name='tasks')
    description = models.TextField()

    def __str__(self):
        return f"{self.concept.language.name} | {self.concept.name} - {self.description[:30]}"
    
from django.db import models
from django.contrib.auth.models import User  # Mentor is the logged-in user

class Intern(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15, blank=True, null=True)
    joined_date = models.DateField(auto_now_add=True)
    mentor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='interns')

    def __str__(self):
        return f"{self.name} (Mentor: {self.mentor.username})"


from django.db import models
from django.utils import timezone
from datetime import timedelta

from django.db import models
from django.utils import timezone

class DailyTaskProgress(models.Model):
    intern = models.ForeignKey("Intern", on_delete=models.CASCADE)
    language = models.ForeignKey("Language", on_delete=models.CASCADE,null=True,blank=True)
    concept = models.ForeignKey("Concept", on_delete=models.CASCADE)
    current_task_index = models.IntegerField(default=0)
    active = models.BooleanField(default=True)
    last_sent_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.intern.name} - {self.concept.name} (Task {self.current_task_index})"




