from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User, Company, UserType, Warehouse
# Register your models here.
# admin.site.register(User)
admin.site.register(Company)
admin.site.register(UserType)
admin.site.register(Warehouse)




class UserAdminConfig(UserAdmin):
    model = User
    search_fields = ('name',)
    list_filter = ('name',)
    ordering = ('email',)
    list_display = ('email','is_active', 'is_staff','company',)
    fieldsets = (
        (None, {'fields': ( 'email', 'name', 'password', )}),
        ('Permissions', {'fields': ( 'is_superuser','is_staff', 'is_active', 'user_type', 'company',)}),
        
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email','password1', 'password2', 'is_active', 'is_staff', 'user_type', 'company',)}
         ),
    )


admin.site.register(User, UserAdminConfig)