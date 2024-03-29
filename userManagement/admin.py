from django.contrib import admin
from django.contrib import admin
from .models import User
from django.contrib.auth.admin import UserAdmin
from django.forms import TextInput, Textarea


class UserAdminConfig(UserAdmin):
    model = User
    search_fields = ('username',  'school_class', 'class_name', 'session','gender', 'other_name', 'last_name', 'first_name',)
    list_filter = (
        'username',  'school_class', 'gender', 'class_name', 'session','other_name', 'last_name', 'first_name', 'is_active',
        'is_staff',)
    ordering = ('start_date',)
    list_display = (
        'username',  'school_class', 'gender', 'class_name','session', 'other_name', 'last_name', 'session_name', 'class_name', 'first_name', "role",
        "matric", "session", "start_date", 'is_active', 'is_staff')
    fieldsets = (
        (None, {'fields': (
            'username',  'school_class', 'gender', 'class_name', 'session','other_name', 'last_name', 'first_name', "role",
            
            "start_date")}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    # formfield_overrides = {
    #     User.about: {'widget': Textarea(attrs={'rows': 10, 'cols': 40})},
    # }
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'username', 'other_name', 'last_name', 'first_name', 'password1', 'password2', 'is_active',
                'is_staff')}
         ),
    )


admin.site.register(User, UserAdminConfig)
