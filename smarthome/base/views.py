from django.shortcuts import render, redirect

def home(request): 
    if request.user.is_authenticated: return redirect('dashboard')
    else: return render(request, 'home.html',{'title':'Home'})

def dashboard(request):
    if not request.user.is_authenticated:
        return redirect('Home')
    return render(request, 'dashboard.html', {'title': 'Dashboard'})


def dashboard(request): return render(request, 'dashboard.html', {'title':'Dashboard'})

