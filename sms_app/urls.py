from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register, name='register'),  # ✅ ADD THIS

    path('dashboard/', views.dashboard, name='dashboard'),
    path('add_student/', views.add_students, name='add_student'),
    path('students/', views.students, name='students'),
    path('analytics/', views.analytics, name='analytics'),
    path('export/', views.export_students, name='export'),
    path('delete/<int:id>/', views.delete_student, name='delete_student'),
    path('profile/', views.profile, name='profile'),
    path('logout/', views.logout_view, name='logout'),
]