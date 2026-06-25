from .models import ReadingSession
from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import ReadingSessionForm
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login


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
            session = form.save(commit=False)
            session.User = request.user
            session.save()
            messages.success(request, 'Reading session added successfully.')
            return redirect('RecentSessions')
    else:
        form = ReadingSessionForm()
    return render(request, 'base/session.html', {'form': form})


def edit_session(request, pk):
    session = ReadingSession.objects.get(pk=pk)
    if request.method == 'POST':
        form = ReadingSessionForm(request.POST, instance=session)
        if form.is_valid():
            form.save()
            messages.success(request, 'Reading session updated successfully.')
            return redirect('RecentSessions')
    else:
        form = ReadingSessionForm(instance=session)
    context = {'form': form, 'session': session}
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
