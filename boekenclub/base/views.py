from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import ReadingSessionForm
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):
    return render(request, "base/index.html")

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
    return render(request, 'base/reading_session_form.html', {'form': form})