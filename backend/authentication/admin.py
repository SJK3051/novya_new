from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Student, Parent, PasswordResetToken


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """
    Admin configuration for custom User model
    """
    list_display = ('username', 'email', 'firstname', 'lastname', 'role', 'is_active', 'createdat')
    list_filter = ('role', 'is_active', 'is_staff', 'is_superuser', 'createdat')
    search_fields = ('username', 'email', 'firstname', 'lastname')
    ordering = ('-createdat',)

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('firstname', 'lastname', 'email', 'phonenumber')}),
        ('Role & Permissions', {'fields': ('role', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'createdat')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'firstname', 'lastname', 'role', 'password1', 'password2'),
        }),
    )


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    """
    Admin configuration for Student model
    """
    list_display = ('student', 'class_field', 'parent')
    list_filter = ('class_field',)
    search_fields = ('student__username', 'student__firstname', 'student__lastname')
    raw_id_fields = ('student', 'parent')


@admin.register(Parent)
class ParentAdmin(admin.ModelAdmin):
    """
    Admin configuration for Parent model
    """
    list_display = ('parent',)
    search_fields = ('parent__username', 'parent__firstname', 'parent__lastname')
    raw_id_fields = ('parent',)


@admin.register(PasswordResetToken)
class PasswordResetTokenAdmin(admin.ModelAdmin):
    """
    Admin configuration for PasswordResetToken model
    """
    list_display = ('user', 'token', 'created_at', 'expires_at', 'is_used')
    list_filter = ('is_used', 'created_at', 'expires_at')
    search_fields = ('user__username', 'user__email', 'token')
    readonly_fields = ('token', 'created_at')

