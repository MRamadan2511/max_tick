from django.urls import path,include
from . import views
from .views import AgentLoginView, CourierLoginView


urlpatterns = [
    path('', views.user_inbox, name='my_inbox'),
    path('home/', views.location_inbox, name='home'),
    path('ticket_create/', views.ticket_create, name='ticket_create'),
    path('ticket_detail/<int:pk>/', views.ticket_detail, name='ticket_detail'),
    path('ticket_detail/<int:pk>/add_comment', views.add_comment, name='add_comment'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('agent_login/', AgentLoginView.as_view(), name='agent_login'),
    path('courier_login/', CourierLoginView.as_view(), name='courier_login'),

]