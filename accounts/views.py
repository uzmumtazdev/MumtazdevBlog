from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
# Create your views here.
def login_view(request):
    if request.method == 'POST':
        user = authenticate(request, username=request.POST["username"],
                            password=request.POST["password"])
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Logged in Fail!")
            return redirect('login')
    else:
        return render(request, 'accounts/login.html')

def logout_view(request):
    logout(request)
    return redirect("/")

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'accounts/signup.html', {'form': form})
