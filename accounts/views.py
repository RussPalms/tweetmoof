from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

# Create your views here.

# Function based views to Class Based Views
def login_view(request, *args, **kwargs):
    form = AuthenticationForm(request, data=request.POST or None)
    #form = MyModelForm(request.POST or None)
    if form.is_valid():
        #username = form.cleaned_data.get("username")
        #user_ = authenticate(username, password)
        user_ = form.get_user()
        login(request, user_)
        return redirect("/")
    context = {
        "form": form,
        "btn_label": "Click to Confirm",
        "title": "Login"
    }
    return render(request, "accounts/auth.html", context)

def logout_view(request, *args, **kwargs):
    if request.method == "POST":
        logout(request)
        return redirect("/login")
    context = {
        "form": None,
        "description": "Are you sure you want to logout?",
        "btn_label": "Logout?",
        "title": "Logout"
    }
    return render(request, "accounts/auth.html", context)

def register_view(request, *args, **kwargs):
    form = UserCreationForm(request.POST or None)
    #form = MyModelForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=True)
        user.set_password(form.cleaned_data.get("password1"))
        # send a confirmation email to verify their account
        login(request, user)
        return redirect("/")
        #print(form.cleaned_data)
        #username = form.cleaned_data.get("username")
        # create my user??
        # User.objects.create(username=username)
    context = {
        "form": form,
        "btn_label": "Register",
        "title": "Register"
    }
    return render(request, "accounts/auth.html", context)
