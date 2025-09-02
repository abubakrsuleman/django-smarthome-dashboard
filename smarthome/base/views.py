from django.shortcuts import render

def home(request): return render(request, 'home.html',{'title':'Home'})

def dashboard(request):
    if not request.user.is_authenticated:
        return redirect('Home')
    return render(request, 'dashboard.html', {'title': 'Dashboard'})


def dashboard(request): return render(request, 'dashboard.html', {'title':'Dashboard'})

