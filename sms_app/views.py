from django.db.models import Count
from django.shortcuts import render, redirect
from .models import User, Student


# ---------------- HOME (Login Page) ----------------
def home(request):
    return render(request, 'login.html')


# ---------------- REGISTER ----------------
def register(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm = request.POST.get('confirm_password')

        if password != confirm:
            return render(request, 'register.html', {
                'error': 'Passwords do not match'
            })

        if User.objects.filter(username=username).exists():
            return render(request, 'register.html', {
                'error': 'Username already exists'
            })

        User.objects.create(username=username, password=password)
        return redirect('/')   # goes to login page

    return render(request, 'register.html')


# ---------------- LOGIN ----------------
def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = User.objects.filter(username=username, password=password).first()

        if user:
            request.session['user'] = username
            return redirect('/dashboard/')
        else:
            return render(request, 'login.html', {
                'error': 'Invalid Username or Password'
            })

    return render(request, 'login.html')   # ✅ FIXED


# ---------------- DASHBOARD ----------------
from .models import Student
from datetime import datetime

def dashboard(request):
    total_students = Student.objects.count()

    total_courses = Student.objects.values('course').distinct().count()

    total_departments = Student.objects.values('department').distinct().count()

    year = datetime.now().year

    return render(request, 'dashboard.html', {
        'total_students': total_students,
        'total_courses': total_courses,
        'total_departments': total_departments,
        'year': year
    })
# ---------------- PROFILE  ---------------- 
def profile(request):
    username = request.session.get('user')

    if not username:
        return redirect('/login/')

    user = User.objects.get(username=username)

    return render(request, 'profile.html', {'user': user})
    
# ---------------- ANALYTICS ----------------

from django.shortcuts import render
from .models import Student
from collections import Counter
import json

def analytics(request):
    students = Student.objects.all()

    # Course data
    courses = [s.course for s in students]
    course_count = Counter(courses)

    context = {
        'course_labels': json.dumps(list(course_count.keys())),
        'course_data': json.dumps(list(course_count.values())),
        'growth_labels': json.dumps([f"Student {i}" for i in range(1, len(students)+1)]),
        'growth_data': json.dumps(list(range(1, len(students)+1))),
    }

    return render(request, 'analytics.html', context)
# ---------------- ADD STUDENTS ----------------
from django.db import IntegrityError

def add_students(request):
    if 'user' not in request.session:
        return redirect('/')

    if request.method == "POST":
        email = request.POST['email']

        # ✅ Check if email already exists
        if Student.objects.filter(email=email).exists():
            return render(request, 'add_students.html', {
                'error': '⚠️ Email already exists! Try another email.'
            })

        try:
            Student.objects.create(
                name=request.POST['name'],
                age=request.POST['age'],
                course=request.POST['course'],
                email=email,
                phone=request.POST.get('phone'),
                department=request.POST.get('department')
            )
        except IntegrityError:
            return render(request, 'add_students.html', {
                'error': '⚠️ Something went wrong. Try again.'
            })

        return redirect('/students/')

    return render(request, 'add_students.html')
# ---------------- VIEW STUDENTS ----------------
def students(request):
    if 'user' not in request.session:
        return redirect('/')

    data = Student.objects.all()
    return render(request, 'students.html', {'students': data})

 #----------------Edit_Student----------------
from django.shortcuts import render, redirect, get_object_or_404
from .models import Student

def edit_student(request, id):
    student = get_object_or_404(Student, id=id)

    if request.method == "POST":
        student.name = request.POST['name']
        student.age = request.POST['age']
        student.course = request.POST['course']
        student.email = request.POST['email']
        student.phone = request.POST['phone']
        student.department = request.POST['department']
        student.save()

        return redirect('/students/')

    return render(request, 'edit_student.html', {'student': student})

# ---------------- EXPORT_STUDENTS  ----------------
import csv
from django.http import HttpResponse
from .models import Student

def export_students(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="students.csv"'

    writer = csv.writer(response)
    writer.writerow(['ID', 'Name', 'Email', 'Phone', 'Course', 'Department', 'Age'])

    students = Student.objects.all()

    for s in students:
        writer.writerow([s.id, s.name, s.email, s.phone, s.course, s.department, s.age])

    return response
# ---------------- DELETE STUDENT ----------------
def delete_student(request, id):
    if 'user' not in request.session:
        return redirect('/')

    try:
        student = Student.objects.get(id=id)
        student.delete()
    except Student.DoesNotExist:
        pass

    return redirect('/students/')


# ---------------- LOGOUT ----------------
def logout_view(request):
    request.session.flush()   # 🔥 clears session (logs user out)
    return redirect('/login/')