from django.urls import path
from . import views

urlpatterns = [
    path('', views.home),
    path('register/', views.register),
    path('login/', views.login_view),
    path('dashboard/', views.dashboard),
    path('profile/', views.profile),
    path('analytics/', views.analytics),
    path('add_student/', views.add_students),
    path('add_student/', views.add_students, name='add_student'),
    path('edit/<int:id>/', views.edit_student),
    path('export/', views.export_students),
    path('students/', views.students),
    path('delete/<int:id>/', views.delete_student),
    path('logout/', views.logout_view),
]