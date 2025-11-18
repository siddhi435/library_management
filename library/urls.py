from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.user_login, name='login'),
    path('register/', views.user_register, name='register'),
    path('logout/', views.user_logout, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('books/', views.book_list, name='book_list'),
    path('members/', views.member_list, name='member_list'),
    path('issue-book/', views.issue_book, name='issue_book'),
    path('return-book/', views.return_book, name='return_book'),
    path('reports/', views.report, name='reports'),
]