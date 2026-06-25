from django.shortcuts import render

#from .forms import ProfileForm
from .forms import RegisterForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.shortcuts import redirect
# Create your views here.
def index(request):
    return render(request, "base/index.html")

'''
def ProfileForm(requests):
    form = ProfileForm()
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