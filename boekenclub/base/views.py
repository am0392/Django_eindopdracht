from .models import ReadingSession, Book
from .forms import ReadingSessionForm, BookForm, ProfileForm, RegisterForm
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.db import IntegrityError
from django.db.models import Avg


def index(request):
    return render(request, "base/index.html")

def newsfeed(request):
    sessions = ReadingSession.objects.all()
    context = {"sessions": sessions}
    return render(request, "base/newsfeed.html", context)

@login_required
def sessionform(request):
    if request.method == 'POST':
        form = ReadingSessionForm(request.POST)
        if form.is_valid():
            try:
                session = form.save(commit=False)
                session.User = request.user
                session.save()
                messages.success(request, 'Reading session added successfully.')
                return redirect('RecentSessions')
            except IntegrityError:
                messages.error(request, 'You already have a reading session for this book on this date.')
    else:
        book_pk = request.GET.get('book')
        initial = {'Book': book_pk} if book_pk else {}
        form = ReadingSessionForm(initial=initial)
    return render(request, 'base/session.html', {'form': form})


def edit_session(request, pk):
    session = ReadingSession.objects.get(pk=pk)
    if request.method == 'POST':
        form = ReadingSessionForm(request.POST, instance=session)
        if request.POST.get("Delete"):
            session.delete()
            messages.success(request, "Session deleted")
            return redirect('RecentSessions')
        if form.is_valid():
            form.save()
            messages.success(request, 'Reading session updated successfully.')
            return redirect('RecentSessions')
    else:
        form = ReadingSessionForm(instance=session)
    context = {'form': form, 'session': session, "edit": True}
    return render(request, 'base/reading_session_form.html', context)

def session_list(request):
    sessions = ReadingSession.objects.filter(User=request.user)
    context = {"sessions": sessions}
    return render(request, "base/session_list.html", context)


def register(request):
    if request.method == "POST":
        form=UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # log the user in and redirect to index
            login(request, user)
            return redirect("index")
    else:
        form = UserCreationForm()
    context = {"form": form}
    return render(request, "registration/register.html", context)

@login_required
def profile(request):
    profile = request.user.profile

    if request.method == "POST":
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Ok saved")
            return redirect("index")
    else:
        form = ProfileForm(instance=profile)

    return render(request, "base/profile.html", {"form": form})

@login_required
def new_book(request):
    if request.method == "POST":
        form = BookForm(request.POST)
        if form.is_valid():
            book = form.save(commit=False)
            if request.user.is_staff:
                book.Approved = True
                book.ApprovedBy = request.user

            book.save()

            messages.success(request, "Book added successfully")
            return redirect("new_book")
    else:
        form = BookForm()

    context = {"form": form}
    return render(request, "base/newbook.html", context)

@staff_member_required
def unapproved_books(request):
    books = Book.objects.filter(Approved=False)
    context = {"books": books}
    return render(request, "base/unapproved_books.html", context)

@staff_member_required
def approve_book(request, pk):
    book = Book.objects.get(pk=pk)
    book.Approved=True
    book.ApprovedBy = request.user
    book.save()
    messages.success(request, "Book approved")
    return redirect("unapproved_books")

@staff_member_required
def deny_book(request, pk):
    book = Book.objects.get(pk=pk)
    book.delete()
    messages.success(request, "Book denied")
    return redirect("unapproved_books")

@staff_member_required
def delete_session(request, pk):
    session = ReadingSession.objects.get(pk=pk)
    session.delete()
    messages.success(request, "Session deleted")
    return redirect("newsfeed")

def book_details(request, pk):
    book = get_object_or_404(Book, pk=pk)
    reading_sessions = ReadingSession.objects.filter(Book=book)
    times_read = reading_sessions.count()
    average_score = reading_sessions.aggregate(avg_score=Avg("Score"))["avg_score"]
    context = {
        "book": book,
        "times_read": times_read,
        "average_score": average_score,
    }
    return render(request, "base/bookdetails.html", context)