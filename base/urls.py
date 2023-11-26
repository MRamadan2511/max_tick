from django.urls import path,include
from . import views
from .views import AgentLoginView, CourierLoginView


urlpatterns = [
    path('home/', views.home, name='home'),
    path('agent-login/', AgentLoginView.as_view(), name='agent_login'),
    path('courier-login/', CourierLoginView.as_view(), name='courier_login'),
    path('ticket_create/', views.ticket_create, name='ticket_create'),

]