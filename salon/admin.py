from django.contrib import admin

from salon.models import Appointment, Service, Specialist


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'duration_minutes')


@admin.register(Specialist)
class SpecialistAdmin(admin.ModelAdmin):
    list_display = ('name',)
    filter_horizontal = ('services',)


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('starts_at', 'client_name', 'client_phone', 'service', 'specialist')
    list_filter = ('service', 'specialist')
