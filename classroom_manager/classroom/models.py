from django.contrib.auth.models import AbstractUser
from django.db import models


class Professor(AbstractUser):
    department = models.CharField(max_length=100, null=True, blank=True)
    
    class Meta:
        db_table = 'classroom_professor'
        verbose_name = 'professor'
        verbose_name_plural = 'professors'


class Lecture(models.Model):
    name = models.CharField(max_length=255)
    classroom_number = models.CharField(max_length=50)
    capacity = models.PositiveIntegerField(null=True, blank=True)
    current_people_count = models.PositiveIntegerField(default=0)
    professor = models.ForeignKey(Professor, on_delete=models.CASCADE, related_name='lectures')

    class Meta:
        unique_together = ['name', 'classroom_number', 'professor']

    def __str__(self):
        return f"{self.name} - Room {self.classroom_number} (Prof. {self.professor.username})"


class ClassroomPhoto(models.Model):
    lecture = models.ForeignKey(Lecture, on_delete=models.CASCADE, related_name='photos')
    image = models.ImageField(upload_to='classroom_photos/')
    number_of_people = models.PositiveIntegerField(default=0)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Photo for {self.lecture.name} - {self.number_of_people} people"