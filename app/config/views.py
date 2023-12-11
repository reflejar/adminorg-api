from django.http import HttpResponse

def ready(request): return HttpResponse("OK")