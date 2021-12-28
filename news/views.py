from django.shortcuts import render
from .models import New #add

# Create your views here.
def index(request):      #add
    news = New.objects.order_by('-created_datetime')
    return render(request, 'news/index.html', {'news': news})

def detail(request, new_id):
    new = New.objects.get(id=new_id)
    news = New.objects.order_by('-created_datetime')
    context = {
        "new": new,
        "news":news
    }

    return render(request, "news/detail.html", context)
