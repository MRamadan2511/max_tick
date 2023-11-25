from django.shortcuts import render


from .models import Ticket


def home(request):
    tic = Ticket.objects.all()
   

    return render(request, 'core/home.html', context={"tic":tic},)