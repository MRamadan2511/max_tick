from django import template

register = template.Library()

@register.filter
def status_class(ticket_status):
    status = ticket_status.status

    if status == 'Open':
        return 'badge bg-primary'
    elif status == 'In Progress':
        return 'badge bg-info'
    elif status == 'Waiting':
        return 'badge bg-warning'
    elif status == 'Closed':
        return 'badge bg-success'
    elif status == 'Overdue':
        return 'badge bg-danger'
    else:
        return 'badge bg-secondary'