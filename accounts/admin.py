from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from accounts.models import User, Department, Subject


class CustomUserAdmin(UserAdmin):
    fieldsets = (
        *UserAdmin.fieldsets,
        (
            'User info',
            {
                'fields':(
                    'profile_pic' , 'phone_number' , 'date_of_birth' , 'department' , 'user_type' , 'position' , 'semester', 
                    'roll_number', 'subjects', 'year_of_admission'

                )
            }
        )
    )


admin.site.register(User, CustomUserAdmin)
admin.site.register(Department)
admin.site.register(Subject)
