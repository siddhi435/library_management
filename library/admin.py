from django.contrib import admin
from .models import Book, Member, Issue

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'category', 'isbn', 'quantity']

@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ['name', 'roll_no', 'email', 'joined_date']

@admin.register(Issue)
class IssueAdmin(admin.ModelAdmin):
    list_display = ['book', 'member', 'issue_date', 'return_date', 'is_returned']