from django.db import models

# Create your models here.
from django.db import models

class Concept(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Task(models.Model):
    concept = models.ForeignKey(Concept, on_delete=models.CASCADE, related_name='tasks')
    description = models.TextField()

    def __str__(self):
        return f"{self.concept.name} - {self.description[:50]}"

