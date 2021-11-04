from django.shortcuts import render

def homepageView(request):
    return render(request, "index.html")