from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, EmailOTP, PasswordResetOTP

# =============================== User Admin ==============================================================
@admin.register(User)
class UserAdmin(BaseUserAdmin):
    # Fields to display in the list view
    list_display = ('email', 'is_verified', 'is_active', 'is_staff', 'is_superuser', 'date_joined')
    list_filter = ('is_verified', 'is_active', 'is_staff', 'is_superuser')
    search_fields = ('email',)
    ordering = ('-date_joined',)

    # Fields shown when editing a user
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'is_verified', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    # Fields shown when create a new user
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_active', 'is_staff', 'is_superuser', 'is_verified'),
        }),
    )

# ========================= EmailOTP Admin =================================================================
@admin.register(EmailOTP)
class EmailOTPAdmin(admin.ModelAdmin):
    list_display = ('user', 'code', 'attempts', 'created_at', 'is_expired')
    list_filter = ('created_at',)
    search_fields = ('user__email', 'code')
    readonly_fields = ('created_at',)
    ordering = ('-created_at',)

    def is_expired(self, obj):
        return obj.is_expired()
    is_expired.boolean = True
    is_expired.short_description = 'Expired'

# ================================ PasswordResetOTP Admin ====================================================
@admin.register(PasswordResetOTP)
class PasswordResetOTPAdmin(admin.ModelAdmin):
    list_display = ('user', 'code', 'attempts', 'created_at', 'is_expired')
    list_filter = ('created_at',)
    search_fields = ('user__email', 'code')
    readonly_fields = ('created_at')
    ordering = ('-created_at')

    def is_expired(self, obj):
        return obj.is_expired()
    is_expired.boolean = True
    is_expired.short_description = 'Expired'