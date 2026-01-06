from rest_framework import serializers
from .models import Concept, Task

class ConceptSerializer(serializers.ModelSerializer):
    class Meta:
        model = Concept
        fields = '__all__'

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'


class TaskFilterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'concept', 'description']
