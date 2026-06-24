from django.shortcuts import render
from .models import ReadingSession

# Create your views here.
def index(request):
    return render(request, "base/index.html")

def newsfeed(request):
    sessions = ReadingSession.objects.all()
    context = {"sessions": sessions}
    return render(request, "base/newsfeed.html", context)