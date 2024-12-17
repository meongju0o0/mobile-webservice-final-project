from django.contrib import admin
from .models import Professor, Lecture, ClassroomPhoto


@admin.register(Professor)
class ProfessorAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'department')
    search_fields = ('username', 'email')


@admin.register(Lecture)
class LectureAdmin(admin.ModelAdmin):
    list_display = ('name', 'classroom_number', 'capacity', 'current_people_count', 'professor')
    search_fields = ('name', 'classroom_number')
    list_filter = ('professor',)


@admin.register(ClassroomPhoto)
class ClassroomPhotoAdmin(admin.ModelAdmin):
    list_display = ('lecture', 'number_of_people', 'uploaded_at')
    list_filter = ('lecture', 'uploaded_at')
