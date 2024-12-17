from django.shortcuts import render
from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django import forms
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import JsonResponse
from rest_framework.authtoken.models import Token
from .serializers import ProfessorSerializer, LectureSerializer, ClassroomPhotoSerializer
from .models import Professor, ClassroomPhoto, Lecture
from .forms import ClassroomPhotoForm


class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=status.HTTP_200_OK)
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)


class ProfessorRegisterView(APIView):
    def post(self, request):
        serializer = ProfessorSerializer(data=request.data)
        if serializer.is_valid():
            professor = serializer.save()
            token, created = Token.objects.get_or_create(user=professor)
            return Response({
                'token': token.key,
                'user_id': professor.id,
                'username': professor.username
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProfessorLoginView(APIView):
    def get(self, request):
        return render(request, 'classroom/login.html')

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        
        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'token': token.key,
                'user_id': user.id,
                'username': user.username
            })
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)


class LectureListAPI(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        lectures = Lecture.objects.filter(professor=request.user)
        serializer = LectureSerializer(lectures, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = LectureSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(professor=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ClassroomPhotoListAPI(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        photos = ClassroomPhoto.objects.filter(
            lecture__professor=request.user
        ).order_by('-uploaded_at')
        serializer = ClassroomPhotoSerializer(photos, many=True)
        return Response(serializer.data, status=200)


class LecturePhotoListAPI(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        photos = ClassroomPhoto.objects.filter(
            lecture__professor=request.user
        ).order_by('-uploaded_at')
        serializer = ClassroomPhotoSerializer(photos, many=True)
        return Response(serializer.data, status=200)


@api_view(['POST'])
def update_people_count(request):
    people_count = request.data.get('people_count')
    classroom_number = request.data.get('classroom_number')
    lecture_name = request.data.get('lecture_name')
    professor_id = request.data.get('professor_id')
    
    if not all([people_count, classroom_number, lecture_name, professor_id]):
        return Response({
            "error": "people_count, classroom_number, lecture_name, and professor_id are required."
        }, status=status.HTTP_400_BAD_REQUEST)

    image_file = request.FILES.get('image', None)
    if image_file is None:
        return Response({"error": "No image uploaded."}, status=status.HTTP_400_BAD_REQUEST)

    try:
        professor = Professor.objects.get(username=professor_id)
        lecture, created = Lecture.objects.get_or_create(
            name=lecture_name,
            classroom_number=classroom_number,
            professor=professor,
            defaults={'capacity': None}
        )
    except Professor.DoesNotExist:
        return Response({"error": "Professor not found."}, status=status.HTTP_404_NOT_FOUND)

    photo = ClassroomPhoto.objects.create(
        lecture=lecture,
        image=image_file,
        number_of_people=people_count
    )

    lecture.current_people_count = people_count
    lecture.save()

    serializer = ClassroomPhotoSerializer(photo)
    return Response({
        "message": "Updated successfully",
        "lecture": {
            "name": lecture.name,
            "classroom_number": lecture.classroom_number,
            "current_people_count": lecture.current_people_count
        },
        "photo": serializer.data
    }, status=status.HTTP_201_CREATED)


@login_required
def upload_class(request):
    if request.method == 'POST':
        form = ClassroomPhotoForm(request.POST, request.FILES)
        if form.is_valid():
            photo = form.save()
            return redirect('classroom:index')
    else:
        form = ClassroomPhotoForm()
        form.fields['lecture_id'].queryset = Lecture.objects.filter(professor=request.user)
    return render(request, 'classroom/upload_class.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('classroom:index')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            next_url = request.GET.get('next')
            if next_url:
                return redirect(next_url)
            return redirect('classroom:index')
        else:
            return render(request, 'classroom/login.html', {'error': 'Invalid credentials'})
    return render(request, 'classroom/login.html')


def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        department = request.POST.get('department')
        
        try:
            professor = Professor.objects.create_user(
                username=username,
                email=email,
                password=password,
                department=department
            )
            login(request, professor)
            return redirect('classroom:index')
        except:
            return render(request, 'classroom/register.html', 
                        {'error': 'Registration failed. Try different username.'})
    
    return render(request, 'classroom/register.html')


@login_required
def index(request):
    photos = ClassroomPhoto.objects.filter(
        lecture__professor=request.user
    ).order_by('-uploaded_at')
    return render(request, 'classroom/index.html', {'photos': photos})


def logout_view(request):
    logout(request)
    return redirect('classroom:login')