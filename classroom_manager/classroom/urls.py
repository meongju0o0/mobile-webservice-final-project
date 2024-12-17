from django.urls import path
from . import views

app_name = 'classroom'

urlpatterns = [
    path('', views.login_view, name='login'),
    path('index/', views.index, name='index'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    path('upload/', views.upload_class, name='upload_class'),
    path('api/login/', views.ProfessorLoginView.as_view(), name='api_login'),
    path('api/lectures/', views.LectureListAPI.as_view(), name='lecture_list'),
    path('api/classroom_photos/', views.ClassroomPhotoListAPI.as_view(), name='classroom_photo_list'),
    path('api/update_people_count/', views.update_people_count, name='update_people_count'),
]
