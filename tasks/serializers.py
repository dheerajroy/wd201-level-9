from rest_framework import serializers
from .models import Task, TaskChange

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'status']
        read_only_fields = ['id']

class TaskChangeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskChange
        fields = '__all__'
        read_only_fields = ['__all__']
