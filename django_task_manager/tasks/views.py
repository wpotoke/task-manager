from drf_spectacular.utils import extend_schema, OpenApiExample
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status, permissions
from tasks.models import Task
from tasks.serializers import TaskSerializer

User = get_user_model()


class TaskListCreateView(APIView):
    """
    list:
    Return a list of all tasks for the authenticated user.

    create:
    Create a new task instance.
    """

    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(
        description="Get list of user's tasks",
        responses={200: TaskSerializer(many=True)},
    )
    def get(self, request):
        """Get list of user's tasks"""
        tasks = Task.objects.filter(author=request.user).order_by("-created")
        return Response(
            {"tasks": TaskSerializer(tasks, many=True).data}, status=status.HTTP_200_OK
        )

    @extend_schema(
        description="Create a new task",
        request=TaskSerializer,
        responses={201: TaskSerializer},
        examples=[
            OpenApiExample(
                "Example request",
                value={
                    "name": "My task",
                    "description": "Task description",
                    "status": "CRTE",
                    "author": 1,
                },
                request_only=True,
            ),
            OpenApiExample(
                "Example response",
                value={
                    "uuid": "12345678-1234-5678-1234-567812345678",
                    "name": "My task",
                    "description": "Task description",
                    "status": "CRTE",
                    "author": 1,
                    "created": "2025-01-01T12:00:00Z",
                    "updated": "2025-01-01T12:00:00Z",
                },
                response_only=True,
            ),
        ],
    )
    def post(self, request):
        """Create a new task"""
        serializer = TaskSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(author=request.user)

        return Response({"task": serializer.data}, status=status.HTTP_201_CREATED)


class TaskDetailView(APIView):
    """
    retrieve:
    Return the given task.

    update:
    Update the given task.

    partial_update:
    Partial update the given task.

    destroy:
    Delete the given task.
    """

    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, uuid):
        """Helper method to get task with validation"""
        try:
            return get_object_or_404(Task, uuid=uuid, author=self.request.user)
        except ValueError:
            return None

    @extend_schema(
        description="Get task details",
        responses={200: TaskSerializer},
    )
    def get(self, request, uuid):
        """Get task detail"""
        task = self.get_object(uuid)
        if not task:
            return Response(
                {"error": "Invalid UUID format"}, status=status.HTTP_400_BAD_REQUEST
            )

        return Response({"task": TaskSerializer(task).data}, status=status.HTTP_200_OK)

    @extend_schema(
        description="Update task",
        request=TaskSerializer,
        responses={200: TaskSerializer},
        examples=[
            OpenApiExample(
                "Example request",
                value={
                    "name": "edit task",
                    "description": "edit description",
                    "status": "WORK",
                    "author": 1,
                },
                request_only=True,
            ),
            OpenApiExample(
                "Example response",
                value={
                    "name": "edited task",
                    "description": "edited description",
                    "status": "edited WORK",
                    "author": 1,
                    "created": "2025-01-01T12:00:00Z",
                    "updated": "2025-01-01T12:00:00Z",
                },
                response_only=True,
            ),
        ],
    )
    def put(self, request, uuid):
        """Full task update"""
        task = self.get_object(uuid)
        if not task:
            return Response(
                {"error": "Invalid UUID format or task not found"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = TaskSerializer(task, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({"task": serializer.data}, status=status.HTTP_200_OK)

    @extend_schema(
        description="Delete task",
        responses={204: None},
    )
    def delete(self, request, uuid):
        """Delete task"""
        task = self.get_object(uuid)
        if not task:
            return Response(
                {"error": "Invalid UUID format or task not found"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        task.delete()
        return Response(
            {"message": "Task deleted successfully"}, status=status.HTTP_204_NO_CONTENT
        )
