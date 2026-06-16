from django.contrib import admin

from .models import Student


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'email', 'department', 'is_active', 'has_profile')
    list_filter = ('is_active', 'department', 'city')
    search_fields = ('first_name', 'last_name', 'email', 'mobile')

    @admin.display(boolean=True, description='Profile')
    def has_profile(self, obj):
        return bool(obj.profile_thumb)
