from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User, Company, UserType, Location, Department, Ticket, Tag, Status, Comment, UserRole

admin.site.register(Company)
admin.site.register(UserType)
admin.site.register(Location)
admin.site.register(Tag)
admin.site.register(Ticket)
admin.site.register(Department)
admin.site.register(Status)
admin.site.register(Comment)
admin.site.register(UserRole)



class UserAdminConfig(UserAdmin):
    model = User
    search_fields = ('name',)
    list_filter = ('name',)
    ordering = ('email',)
    
    list_display = ('email','is_active', 'is_staff','company','user_role','user_type',)

    fieldsets = (
        (None, {'fields': ( 'email', 'name', 'password', )}),
        ('Permissions', {'fields': ( 'is_superuser','is_staff', 'is_active', 'user_type', 'company','user_role',)}),)
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email','password1', 'password2', 'is_active', 'is_staff', 'user_type', 'company',)}),)

admin.site.register(User, UserAdminConfig)