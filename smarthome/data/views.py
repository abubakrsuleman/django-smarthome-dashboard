from django.http import JsonResponse
import psutil

def system_status(request):
    cpu = psutil.cpu_percent(interval=0.5)
    mem = psutil.virtual_memory()
    disk = psutil.disk_usage("/")

    data = {
        "cpu": cpu,
        "memory": {
            "percent": mem.percent,
            "used": mem.used,
            "total": mem.total,
        },
        "disk": {
            "percent": disk.percent,
            "used": disk.used,
            "total": disk.total,
        },
    }
    return JsonResponse(data)

