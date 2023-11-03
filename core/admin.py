from django.contrib import admin
from .models import Company, Department, Tag, Warehouse, Ticket

admin.site.register(Company)
admin.site.register(Department)
admin.site.register(Tag)
admin.site.register(Warehouse)
admin.site.register(Ticket)