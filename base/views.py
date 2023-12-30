from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.contrib import messages
from django.db import models
from django.db.models import Count

import plotly.express as px
from datetime import datetime, timedelta

from .forms import AgentLoginForm, CourierLoginForm, TicketForm, CommentForm, UpdateLocationForm, UpdateStatusForm, DateForm
from .models import Ticket, Comment, User
from .decorators import user_role_required



@login_required
def user_inbox(request):
# View for tickets created by each user
    tickets =  Ticket.objects.filter(user=request.user) | Ticket.objects.filter(assigned_to=request.user)
    ####
    # To Do: need add filter by status here if ticket closed remove from user view
    ####
    return render(request, 'base/user_inbox.html', context={"tickets":tickets, })



@login_required
@user_role_required(allowed_roles=['admin',])
def location_inbox(request):
    # Filter tickets based on the user's location
    user_location = request.user.location
    ticket = Ticket.objects.filter(location=user_location)

    # Get ticket count for the filtered tickets
    all_ticket = ticket.count()   

    # Filter tickets for open status
    open_count          = ticket.filter(status__status='Open').count()
    closed_count        = ticket.filter(status__status='Closed').count()
    overdue_count       =  ticket.filter(status__status='Overdue').count()
    waiting_count       =  ticket.filter(status__status='Waiting').count() 
    inprogress_count       =  ticket.filter(status__status='In Progress').count()
    new_count           =  ticket.filter(status__status='New').count() 

    return render(request, 'base/location_inbox.html', context={"ticket":ticket, "open_count":open_count,
                                                      "closed_count":closed_count,"overdue_count":overdue_count,
                                                      "waiting_count":waiting_count,"inprogress_count":inprogress_count,
                                                      "new_count":new_count,"all_ticket":all_ticket,
                                                },)


@login_required
# @user_role_required(allowed_roles=['admin', 'editor'])
def ticket_create(request):
    if request.method == 'POST':
        form = TicketForm(request.POST, request.FILES)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.user = request.user  # Assuming you have user authentication in place
            ticket.location = request.user.location
            ticket.save()
            return redirect('ticket_detail', pk=ticket.pk)  # Redirect to ticket detail page
    else:
        form = TicketForm()

    return render(request, 'base/ticket_create.html', {'form': form})


@login_required
# @user_role_required(allowed_roles=['admin', 'editor'])
def ticket_detail(request, pk):
    print(request.user.user_type.type)
    ticket = get_object_or_404(Ticket, pk=pk)
    comments = ticket.comment_set.all()

    if request.method == 'POST':
        location_form = UpdateLocationForm(request.POST, instance=ticket)
        status_form = UpdateStatusForm(request.POST, instance=ticket)
    
        if 'location-submit' in request.POST and location_form.is_valid():
            location_form.save()
            messages.success(request, "Location Updated Successfully")
            return redirect('ticket_detail', pk=pk)
        else:
            'status-submit' in request.POST and status_form.is_valid()
            status_form.save()
            messages.success(request, "Status Updated Successfully")
            return redirect('ticket_detail', pk=pk)
    else:
        comment_form = CommentForm()
        location_form = UpdateLocationForm(instance=ticket)
        status_form = UpdateStatusForm(instance=ticket)

    return render(request, 'base/ticket_detail.html', {'ticket': ticket, 'comments': comments, 
                                                       'comment_form': comment_form,
                                                         'location_form': location_form,
                                                         'status_form':status_form})
@login_required
def add_comment(request, pk):
    ticket = get_object_or_404(Ticket, pk=pk)

    if request.method == 'POST':
        form = CommentForm(request.POST, request.FILES)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.ticket = ticket
            comment.user = request.user  # Assuming you have user authentication
            comment.save()
            messages.info(request, "comment added Successfully")
            return redirect('ticket_detail', pk=pk)
        else:
            # Form is not valid, comment is blank
            messages.error(request, "blaaaaaaaaaaank")
            return redirect('ticket_detail', pk=pk)
    else:
        form = CommentForm()
        
    return render(request, 'base/ticket_detail.html', {'form': form, 'ticket': ticket, })





class AgentLoginView(LoginView):
    template_name = 'base/agent_login.html'
    authentication_form = AgentLoginForm

    def get_success_url(self):
        return reverse_lazy('home') 

class CourierLoginView(LoginView):
    template_name = 'base/courier_login.html'
    authentication_form = CourierLoginForm

    def get_success_url(self):
        return reverse_lazy('home')



def generate_pie_chart(data, names_column, title):
    '''
        model for generating a pie charts
    '''
    chart_data = data.values(names_column).annotate(count=Count(names_column))

    if not chart_data:
        return f"No data available for {title}."

    fig = px.pie(
        chart_data,
        names=names_column,
        values='count',
        title=title,
        labels={names_column: title, 'count': 'Ticket Count'})

    fig.update_layout(
        title={
            'font_size': 24,
            'xanchor': 'center',
            'x': 0.5
            })

    return fig.to_html()


@login_required
@user_role_required(allowed_roles=['admin',])
def dashboard(request):

    #date from the form
    start = request.GET.get('start')
    end = request.GET.get('end')

    tickets = Ticket.objects.all()

    if end:
        # Set the end date to include the entire day
        end_date = datetime.strptime(end, "%Y-%m-%d") + timedelta(days=1)
        tickets = tickets.filter(created_at__lt=end_date)

    if start:
        tickets = tickets.filter(created_at__gte=start)
    
    # Chart for Location
    location_chart = generate_pie_chart(tickets, 'location__name', 'Ticket Locations')

    # Chart for Status
    status_chart = generate_pie_chart(tickets, 'status__status', 'Ticket Status')

    return render(request, 'base/chart.html', 
                  context= {'location_chart': location_chart,  'status_chart': status_chart,
                            'form': DateForm(initial={'start': start, 'end': end})})
