from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    isbn = models.CharField(max_length=13, unique=True)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.title

class Member(models.Model):
    name = models.CharField(max_length=200)
    roll_no = models.CharField(max_length=20, unique=True)
    email = models.EmailField()
    phone = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)
    joined_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.roll_no} - {self.name}"

class Issue(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    issue_date = models.DateField(default=timezone.now)
    return_date = models.DateField(null=True, blank=True)
    is_returned = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.book.title} - {self.member.name}"