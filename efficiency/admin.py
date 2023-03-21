from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Profile, FingerPrint, Location, Attendance, Timer, Efficiency, Project, ProjectEmployee, Task, Review, Meeting, Attendee, Notification

# Register your models here.
class UserAdmin(UserAdmin):
    model = User
    list_display = ['email', 'phone', 'department', 'first_name', 'last_name', 'is_staff','is_active']
    list_filter = ['email', 'phone', 'department', 'first_name', 'last_name', 'is_staff','is_active']

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('department','first_name','last_name','phone')}),
        ('Permissions', {'fields': ('is_active','is_staff')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide,'),
            'fields': ('email', 'password1', 'password2', 'phone' ,'is_staff','is_active'),
        }),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()

admin.site.register(User, UserAdmin)
admin.site.register(Profile)
admin.site.register(FingerPrint)
admin.site.register(Location)
admin.site.register(Attendance)
admin.site.register(Timer)
admin.site.register(Efficiency)
admin.site.register(Project)
admin.site.register(ProjectEmployee)
admin.site.register(Task)
admin.site.register(Review)
admin.site.register(Meeting)
admin.site.register(Attendee)
admin.site.register(Notification)