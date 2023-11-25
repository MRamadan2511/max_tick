from django.shortcuts import render
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from .forms import AgentLoginForm, CourierLoginForm

from .models import Ticket


def home(request):
    tic = Ticket.objects.all()

    return render(request, 'base/home.html', context={"tic":tic},)
# views.py


class AgentLoginView(LoginView):
    template_name = 'base/agent_login.html'
    authentication_form = AgentLoginForm

    def get_success_url(self):
        return reverse_lazy('home') 

class CourierLoginView(LoginView):
    template_name = 'base/courier_login.html'
    authentication_form = CourierLoginForm
    print(authentication_form)

    def get_success_url(self):
        return reverse_lazy('home')
