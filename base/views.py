from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.contrib import messages


from .forms import AgentLoginForm, CourierLoginForm, TicketForm, CommentForm, UpdateLocationForm, UpdateStatusForm
from .models import Ticket, Comment


def home(request):
    ticket = Ticket.objects.all()
    all_ticket = ticket.count()
    all_status_counts = Ticket.get_status_counts()
    # Filter tickets for open status
    open_tickets_count = all_status_counts.get('Open', 0)
    closed_tickets_count = all_status_counts.get('Closed', 0)
    overdue_tickets_count = all_status_counts.get('Overdue', 0)
    waiting_tickets_count = all_status_counts.get('Waiting', 0)
    inprogress_tickets_count = all_status_counts.get('In Progress', 0)
    new_tickets_count = all_status_counts.get('New', 0)

    return render(request, 'base/home.html', context={"ticket":ticket, 
                                                      "open_tickets_count":open_tickets_count,
                                                      "closed_tickets_count":closed_tickets_count,
                                                      "overdue_tickets_count":overdue_tickets_count,
                                                      "waiting_tickets_count":waiting_tickets_count,
                                                      "inprogress_tickets_count":inprogress_tickets_count,
                                                      "new_tickets_count":new_tickets_count,
                                                      "all_ticket":all_ticket,
                                                      },)


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


# def ticket_detail(request, pk):
#     ticket = get_object_or_404(Ticket, pk=pk)

#     comments = ticket.comment_set.all()
#     comment_form = CommentForm()

#     return render(request, 'base/ticket_detail.html', {'ticket': ticket, 'comments': comments, 'comment_form': comment_form})


def ticket_detail(request, pk):
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
