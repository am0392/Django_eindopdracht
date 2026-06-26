from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .forms import ProfileForm

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.shortcuts import redirect

from django.contrib import messages

# Create your views here.
def index(request):
    return render(request, "base/index.html")

'''
def profile(requests):
    form = profile()
    context = {"form": form}

    if requests.method == "POST":
        name = requests.POST.get("your_name")
        context["greeting"] = f"What would you do if when you okay, so he said yes would go,  {name}?"
    return render(requests, "base/nameform.html", context)
'''

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