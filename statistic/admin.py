from django.contrib import admin
from .models import Report


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ('user', 'report_date')
    list_filter = ('user', 'report_date')
    search_fields = ('user__username', 'user__first_name', 'user__last_name')
    ordering = ('-report_date',)

# Register your models here.
