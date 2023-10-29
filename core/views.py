from django.shortcuts import render
from .models import Ticket
# Create your views here.

def home(request):
    tic = Ticket.objects.all()
   

    return render(request, 'core/home.html', context={"tic":tic},)