from django.urls import path,include
from . import views
from .views import AgentLoginView, CourierLoginView


urlpatterns = [
    path('home/', views.home, name='home'),
    path('agent_login/', AgentLoginView.as_view(), name='agent_login'),
    path('courier_login/', CourierLoginView.as_view(), name='courier_login'),
    path('ticket_create/', views.ticket_create, name='ticket_create'),
    path('ticket_detail/<int:pk>/', views.ticket_detail, name='ticket_detail'),

]