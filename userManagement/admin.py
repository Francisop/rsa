from django.contrib import admin
from django.contrib import admin
from .models import User
from django.contrib.auth.admin import UserAdmin
from django.forms import TextInput, Textarea


class UserAdminConfig(UserAdmin):
    model = User
    search_fields = ('username', 'full_name')
    list_filter = ('username', 'full_name', 'is_active', 'is_staff',)
    ordering = ('start_date',)
    list_display = ('username', 'full_name', "role", "matric", "session",  "start_date", 'is_active', 'is_staff')
    fieldsets = (
        (None, {'fields': ('username', 'full_name', "role", "start_date")}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    # formfield_overrides = {
    #     User.about: {'widget': Textarea(attrs={'rows': 10, 'cols': 40})},
    # }
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'full_name', 'password1', 'password2', 'is_active', 'is_staff')}
         ),
    )


admin.site.register(User, UserAdminConfig)
