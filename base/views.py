from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.contrib import messages
from django.db import models,connection
from django.db.models import Count
from django.http import JsonResponse


import plotly.express as px
from datetime import datetime, timedelta

from .forms import (AgentLoginForm, CourierLoginForm,TicketForm, 
                    CommentForm, UpdateLocationForm, UpdateStatusForm,
                    UpdateDepartmentForm, UpdateTagForm, DateForm,
                    UpdateAssignedToForm)
from .models import Ticket, Comment, User, Location, Status,TicketLog
from .decorators import user_role_required



@login_required
def user_inbox(request):
# View for tickets created or assigend on each user
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

    # get user type for the form to change failed lable names if user is courier
    user_type = request.user.user_type.type if request.user.is_authenticated else None

    if request.method == 'POST':
        form = TicketForm(request.POST, request.FILES, user_type=user_type)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.user = request.user  # Assuming you have user authentication in place
            ticket.location = request.user.location
            ticket.save()
            return redirect('ticket_detail', pk=ticket.pk)  # Redirect to ticket detail page
    else:
        form = TicketForm(user_type=user_type)

    return render(request, 'base/ticket_create.html', {'form': form})


@login_required
def ticket_detail(request, pk):
    ticket = get_object_or_404(Ticket, pk=pk)
    comments = ticket.comment_set.all()
    logs = TicketLog.objects.filter(ticket=ticket)
    user_role = request.user.user_role.role

    if request.method == 'POST':
        location_form = UpdateLocationForm(request.POST, instance=ticket)
        status_form = UpdateStatusForm(request.POST, instance=ticket)
        tag_form = UpdateTagForm(request.POST, instance=ticket)
        department_form = UpdateDepartmentForm(request.POST, instance=ticket)
        assigned_to_form = UpdateAssignedToForm(request.POST, instance=ticket)
       

        if location_form.is_valid():
            ticket = get_object_or_404(Ticket, pk=pk)
            new_location = location_form.cleaned_data['location']

            if ticket.location != new_location:
                ticket.log_update(user=request.user, message=f"Location updated by {request.user}")
                location_form.save()
                # messages.success(request, "Location Updated Successfully")
                print("OKKK")
                return JsonResponse({'status': 'success', 'message': 'Location Updated Successfully'})
            else:
                print("nooooo")
                return JsonResponse({'status': 'info', 'message': 'Location is the same, no update'})
        
        elif 'status-submit' in request.POST and status_form.is_valid():
            ticket.log_update(user=request.user, message=f"Status updated by {request.user}")
            status_form.save()
            messages.success(request, "Status Updated Successfully")
            return redirect('ticket_detail', pk=pk)
        
        elif 'assigned-submit' in request.POST and assigned_to_form.is_valid():
            ticket.log_update(user=request.user, message=f"Assigned to updated by {request.user}")
            assigned_to_form.save()
            messages.success(request, "Assigned To Updated Successfully")
            return redirect('ticket_detail', pk=pk)
        
        elif 'department-submit' in request.POST and department_form.is_valid():
            ticket.log_update(user=request.user, message=f"Department updated by {request.user}")
            department_form.save()
            messages.success(request, "Department Updated Successfully")
            return redirect('ticket_detail', pk=pk)

        else:
            'tag-submit' in request.POST and tag_form.is_valid()
            tag_form.save()
            messages.success(request, "Tag Updated Successfully")
            return redirect('ticket_detail', pk=pk)
    else:
        comment_form = CommentForm()
        location_form = UpdateLocationForm(instance=ticket, )
        status_form = UpdateStatusForm(instance=ticket)
        tag_form = UpdateTagForm(instance=ticket)
        department_form = UpdateDepartmentForm(instance=ticket)
        assigned_to_form = UpdateAssignedToForm(instance=ticket)

    return render(request, 'base/ticket_detail.html', {'ticket': ticket, 'comments': comments,'user_role':user_role,
                                                       'comment_form': comment_form,'department_form':department_form,
                                                         'location_form': location_form,'tag_form':tag_form,'logs':logs,
                                                         'status_form':status_form,'assigned_to_form':assigned_to_form})


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
            messages.error(request, "Comment can't be blank")
            return redirect('ticket_detail', pk=pk)
    else:
        form = CommentForm()
        
    return render(request, 'base/ticket_detail.html', {'form': form, 'ticket': ticket, })



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


    ## ## Ticket / warehouse ### ####
    unique_locations = Location.objects.all()
    unique_status = Status.objects.all()    

    # If using PostgreSQL, you might need to apply distinct to the entire queryset
    if 'postgresql' in connection.vendor:
        # unique_locations = unique_locations.distinct()
        unique_locations = unique_locations.order_by('name').distinct()
        unique_status = unique_status.order_by('status').distinct()

       
    status_counts = Ticket.objects.values('location__name', 'status__status').annotate(count=Count('id'))

    status_counts_dict = {}
    for count in status_counts:
        location_name = count['location__name']
        status_name = count['status__status']
        status_counts_dict.setdefault(location_name, {})[status_name] = count['count']
        ## ## End Ticket / warehouse ### ####

    return render(request, 'base/chart.html', 
                  context= {'location_chart': location_chart,  'status_chart': status_chart,
                            'form': DateForm(initial={'start': start, 'end': end}),'status_counts':status_counts,
                            'unique_locations':unique_locations,'unique_status':unique_status,
                            'status_counts_dict':status_counts_dict,})





def login(request):
    if request.user.is_authenticated:
        return redirect('user_inbox') 

    return render(request, 'base/login.html',)



class AgentLoginView(LoginView):
    template_name = 'base/agent_login.html'
    authentication_form = AgentLoginForm

    def get_success_url(self):
        return reverse_lazy('user_inbox') 
    
    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect(self.get_success_url())

        return super().dispatch(request, *args, **kwargs)

    

class CourierLoginView(LoginView):
    template_name = 'base/courier_login.html'
    authentication_form = CourierLoginForm

    def get_success_url(self):
        return reverse_lazy('user_inbox')
    
    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect(self.get_success_url())

        return super().dispatch(request, *args, **kwargs)

