from rest_framework import serializers
from .models import Professor, Lecture, ClassroomPhoto


class ProfessorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Professor
        fields = ['id', 'username', 'email', 'department', 'password']
        extra_kwargs = {'password': {'write_only': True}}


class LectureSerializer(serializers.ModelSerializer):
    professor_name = serializers.CharField(source='professor.username', read_only=True)
    
    class Meta:
        model = Lecture
        fields = ['id', 'name', 'classroom_number', 'capacity', 'current_people_count', 'professor', 'professor_name']


class ClassroomPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassroomPhoto
        fields = ['id', 'lecture', 'image', 'number_of_people', 'uploaded_at']
