from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.permissions import IsAuthenticated
from tasks.filters import TaskFilter, TaskChangeFilter
from tasks.models import Task, TaskChange
from tasks.serializers import TaskChangeSerializer, TaskSerializer
from django_filters.rest_framework import DjangoFilterBackend

class TaskViewSet(ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]
    filterset_class = TaskFilter
    filter_backends = [DjangoFilterBackend]

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user, deleted=False)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        task = Task.objects.get(id=self.kwargs['pk'])
        if task.status != serializer.validated_data['status']:
            TaskChange.objects.create(task=task, prev_status=task.status, curr_status=serializer.validated_data['status'])
        serializer.save()

class TaskChangeViewSet(ReadOnlyModelViewSet):
    serializer_class = TaskChangeSerializer
    queryset = TaskChange.objects.all()
    permission_classes = [IsAuthenticated]
    filterset_class = TaskChangeFilter
    filter_backends = [DjangoFilterBackend]
    
    def get_queryset(self):
        return TaskChange.objects.filter(task__user=self.request.user)
