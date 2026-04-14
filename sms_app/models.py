from django.db import models

# --------------------
# USER MODEL
# --------------------
class User(models.Model):
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=255)

    def __str__(self):
        return self.username


# --------------------
# STUDENT MODEL
# --------------------
class Student(models.Model):
    name = models.CharField(max_length=100)
    age = models.PositiveIntegerField()
    course = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    department = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name