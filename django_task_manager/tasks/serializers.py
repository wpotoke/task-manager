from rest_framework import serializers
from tasks.models import Task


class TaskSerializer(serializers.ModelSerializer):
    description = serializers.CharField(default="")

    class Meta:
        model = Task
        fields = (
            "uuid",
            "author",
            "name",
            "description",
            "status",
            "created",
            "updated",
        )
