from django.shortcuts import render, redirect
from data.services.storage_scan import scan_storage_devices
def home(request):
    if request.user.is_authenticated: return redirect('Dashboard')
    else: return render(request, 'home.html',{'title':'Home'})

def dashboard(request):
    storages = scan_storage_devices()
    context = {
        "title": "Dashboard",
        "storages": storages,
    }
    if not request.user.is_authenticated: return redirect('Home')
    if request.user.is_authenticated: return render(request, "dashboard.html", context)


