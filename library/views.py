from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Book, Member, Issue
from datetime import date, timedelta

def home(request):
    return render(request, 'home.html')

# ------------------ Authentication ------------------

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'library/login.html')

def user_register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 != password2:
            messages.error(request, 'Passwords do not match.')
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
            return redirect('register')

        user = User.objects.create_user(username=username, email=email, password=password1)
        user.save()
        messages.success(request, 'Account created successfully! Please log in.')
        return redirect('login')

    return render(request, 'library/register.html')

@login_required
def user_logout(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('login')

# ------------------ Dashboard ------------------

@login_required
def dashboard(request):
    total_books = Book.objects.count()
    total_members = Member.objects.count()
    total_issued = Issue.objects.filter(is_returned=False).count()
    
    context = {
        'total_books': total_books,
        'total_members': total_members,
        'total_issued': total_issued,
    }
    return render(request, 'library/dashboard.html', context)

# ------------------ Books ------------------

@login_required
def book_list(request):
    books = Book.objects.all()
    if request.method == 'POST':
        title = request.POST['title']
        author = request.POST['author']
        category = request.POST['category']
        isbn = request.POST['isbn']
        quantity = request.POST['quantity']

        if not title or not author:
            messages.error(request, 'Please fill all required fields.')
        else:
            Book.objects.create(
                title=title,
                author=author,
                category=category,
                isbn=isbn,
                quantity=quantity
            )
            messages.success(request, f'Book "{title}" added successfully!')
            return redirect('book_list')

    return render(request, 'library/book_list.html', {'books': books})

# ------------------ Members ------------------

@login_required
def member_list(request):
    members = Member.objects.all()
    if request.method == 'POST':
        name = request.POST['name']
        roll_no = request.POST['roll_no']
        email = request.POST['email']
        phone = request.POST.get('phone', '')
        address = request.POST.get('address', '')

        if not name or not roll_no:
            messages.error(request, 'Please fill all required fields.')
        else:
            Member.objects.create(
                name=name, 
                roll_no=roll_no, 
                email=email,
                phone=phone,
                address=address
            )
            messages.success(request, f'Member "{name}" added successfully!')
            return redirect('member_list')

    return render(request, 'library/member_list.html', {'members': members})

# ------------------ Issue Book ------------------

@login_required
def issue_book(request):
    members = Member.objects.all()
    books = Book.objects.filter(quantity__gt=0)
    issues = Issue.objects.filter(is_returned=False)  # Add currently issued books

    if request.method == 'POST':
        member_id = request.POST.get('member')
        book_id = request.POST.get('book')
        return_date = request.POST.get('return_date')

        member = get_object_or_404(Member, id=member_id)
        book = get_object_or_404(Book, id=book_id)

        # Reduce book quantity
        if book.quantity <= 0:
            messages.error(request, 'Book not available.')
        else:
            Issue.objects.create(
                member=member,
                book=book,
                return_date=return_date,
                is_returned=False
            )
            book.quantity -= 1
            book.save()
            messages.success(request, f'Book "{book.title}" issued to {member.name}.')
            return redirect('issue_book')

    return render(request, 'library/issue_book.html', {
        'members': members,
        'books': books,
        'issues': issues
    })

# ------------------ Return Book ------------------

@login_required
def return_book(request):
    if request.method == 'POST':
        issue_id = request.POST['issue_id']
        issue = get_object_or_404(Issue, id=issue_id)
        
        issue.is_returned = True
        issue.return_date = date.today()
        issue.save()
        
        # Return book to inventory
        issue.book.quantity += 1
        issue.book.save()
        
        messages.success(request, f'Book "{issue.book.title}" returned successfully!')
        return redirect('return_book')
    
    issued_books = Issue.objects.filter(is_returned=False)
    return render(request, 'library/return_book.html', {'issued_books': issued_books})

# ------------------ Reports ------------------

@login_required
def report(request):
    total_books = Book.objects.count()
    total_members = Member.objects.count()
    total_issued = Issue.objects.filter(is_returned=False).count()
    total_returned = Issue.objects.filter(is_returned=True).count()
    issue_records = Issue.objects.select_related('book', 'member').all()

    context = {
        'total_books': total_books,
        'total_members': total_members,
        'total_issued': total_issued,
        'total_returned': total_returned,
        'issue_records': issue_records
    }
    return render(request, 'library/reports.html', context)