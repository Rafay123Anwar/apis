# admin.py
from django.contrib import admin
from .models import User, Patient

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['user_id', 'email']  # Only display email, not password
    
    def save_model(self, request, obj, form, change):
        if 'password' in form.cleaned_data:  # Check if password was provided
            raw_password = form.cleaned_data['password']
            obj.set_password(raw_password)  # Hash the password
        super().save_model(request, obj, form, change)

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ['patient_id', 'first_name', 'last_name', 'contact_number']
    search_fields = ['first_name', 'last_name', 'contact_number']
