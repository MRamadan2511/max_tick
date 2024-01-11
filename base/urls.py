from django.urls import path,include
from . import views
from .views import AgentLoginView, CourierLoginView
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', views.user_inbox, name='user_inbox'),
    path('home/', views.location_inbox, name='home'),
    path('ticket_create/', views.ticket_create, name='ticket_create'),
    path('ticket_detail/<int:pk>/', views.ticket_detail, name='ticket_detail'),
    path('ticket_detail/<int:pk>/add_comment/', views.add_comment, name='add_comment'),
    path('ticket_detail/<int:pk>/update_location/', views.ticket_location_update, name='update_location'),
    path('ticket_detail/<int:pk>/update_status/', views.ticket_status_update, name='update_status'),
    path('ticket_detail/<int:pk>/update_tag/', views.ticket_tag_update, name='update_tag'),
    path('ticket_detail/<int:pk>/update_department/', views.ticket_department_update, name='update_department'),
    path('ticket_detail/<int:pk>/update_assigned/', views.ticket_assigned_update, name='update_assigned'),
    path('dashboard/', views.dashboard, name='dashboard'),

    path('login/', views.login, name='login'),
    path('login/agent/', AgentLoginView.as_view(), name='agent_login'),
    path('login/courier/', CourierLoginView.as_view(), name='courier_login'),
    path('logout/', LogoutView.as_view(next_page='/login/'), name='logout'),
    
    

]