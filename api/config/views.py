from django.http import HttpResponse

def readiness(request): return HttpResponse("Readines!!")

def liveness(request): return HttpResponse("Liveness!!")