from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status, permissions
from tasks.models import Task
from tasks.serializers import TaskSerializer

User = get_user_model()


class TaskAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        task = None
        uuid = kwargs.get("uuid", None)
        if uuid:
            try:
                task = get_object_or_404(Task, uuid=uuid)
                return Response(
                    {"task": TaskSerializer(task).data}, status=status.HTTP_200_OK
                )
            except ValueError:
                return Response(
                    {"error": "Invalid UUID format"}, status=status.HTTP_400_BAD_REQUEST
                )

        tasks = Task.objects.filter(author=request.user).order_by("-created")
        return Response({"tasks": TaskSerializer(tasks, many=True).data})

    def post(self, request):
        serializer = TaskSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            {"task created": serializer.data}, status=status.HTTP_201_CREATED
        )

    def put(self, request, *args, **kwargs):
        instance = None
        uuid = kwargs.get("uuid", None)
        if not uuid:
            return Response(
                {"error": "UUID not reseived or has invalid format"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            instance = get_object_or_404(Task, uuid=uuid)
        except ValueError:
            return Response(
                {"error": "Invalid UUID format"}, status=status.HTTP_400_BAD_REQUEST
            )

        serializer = TaskSerializer(data=request.data, instance=instance)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {"task updated": serializer.data}, status=status.HTTP_201_CREATED
        )

    def delete(self, request, *args, **kwargs):
        uuid = kwargs.get("uuid", None)
        if not uuid:
            return Response(
                {"error": "UUID not reseived or has invalid format"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            Task.objects.get(uuid=uuid).delete()
        except Task.DoesNotExist:
            return Response(
                {"error": "Task not found"}, status=status.HTTP_404_NOT_FOUND
            )
        except ValueError:
            return Response(
                {"error": "Invalid UUID format"}, status=status.HTTP_400_BAD_REQUEST
            )

        return Response({"task deleted": "ok"}, status=status.HTTP_200_OK)
