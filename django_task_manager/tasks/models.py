from uuid import uuid4
from django.db import models


# Create your models here.
class Task(models.Model):
    # pylint:disable=too-many-ancestors
    class Status(models.TextChoices):
        CREATED = "CRTE", "Create"
        WORK = "WORK", "Work"
        DONE = "DONE", "Done"

    uuid = models.UUIDField(
        default=uuid4, editable=False, verbose_name="id задачи", unique=True
    )
    name = models.CharField(max_length=255, verbose_name="Название задачи")
    description = models.TextField(blank=True, null=True, verbose_name="Описание")
    status = models.CharField(
        choices=Status.choices,
        default=Status.CREATED,
        max_length=4,
        verbose_name="Статус",
    )
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "tasks"
        verbose_name = "Задача"
        verbose_name_plural = "Задачи"
        ordering = ["-created"]
