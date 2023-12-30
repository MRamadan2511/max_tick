from django.urls import path,include
from . import views
from .views import AgentLoginView, CourierLoginView


urlpatterns = [
    path('', views.inbox, name='my_inbox'),
    path('home/', views.home, name='home'),
    path('agent_login/', AgentLoginView.as_view(), name='agent_login'),
    path('courier_login/', CourierLoginView.as_view(), name='courier_login'),
    path('ticket_create/', views.ticket_create, name='ticket_create'),
    path('ticket_detail/<int:pk>/', views.ticket_detail, name='ticket_detail'),
    path('ticket_detail/<int:pk>/add_comment', views.add_comment, name='add_comment'),

]