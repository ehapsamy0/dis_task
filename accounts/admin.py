from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Status
User = get_user_model()

# Remove Group Model from admin. We're not using it.
admin.site.unregister(Group)

class UserAdmin(BaseUserAdmin):

    list_display = ['phone','first_name','last_name']
    # list_filter = ['admin']
    fieldsets = (
        (None, {'fields': ('phone',)}),
        ('Personal info', {'fields': ('first_name','last_name','gender','country_code','avatar','birthdate','email','is_active')}),

    )








    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone','first_name','last_name',"birthdate",'gender','avatar','country_code', 'password1', 'password2')}
        ),
    )
    search_fields = ['phone']
    ordering = ['phone']


admin.site.register(User, UserAdmin)
admin.site.register(Status)