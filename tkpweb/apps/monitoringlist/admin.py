from django.contrib import admin
from .models import MonitoringList


class MonitoringListAdmin(admin.ModelAdmin):
    pass


admin.site.register(MonitoringList, MonitoringListAdmin)
