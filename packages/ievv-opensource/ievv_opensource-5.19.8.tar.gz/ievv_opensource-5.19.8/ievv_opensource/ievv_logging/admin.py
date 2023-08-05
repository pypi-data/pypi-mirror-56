import json
from django.utils.html import format_html
from django.contrib import admin
from .models import IevvLoggingEventBase, IevvLoggingEventItem


@admin.register(IevvLoggingEventBase)
class IevvLoggingEventBaseAdmin(admin.ModelAdmin):
    list_display = [
        'slug',
        'last_started',
        'last_finished',
        'time_spent_in_seconds',
    ]
    search_fields = [
        'slug'
    ]
    list_filter = [
        'last_started',
    ]
    readonly_fields = [
        'slug',
        'last_started',
        'last_finished',
        'time_spent_in_seconds',
        'time_spent',
    ]


@admin.register(IevvLoggingEventItem)
class IevvLoggingEventItemAdmin(admin.ModelAdmin):
    list_display = [
        'logging_base',
        'created_datetime',
        'time_spent_in_seconds',
        'time_spent',
    ]
    search_fields = [
        'logging_base'
    ]
    list_filter = [
        'logging_base',
        'created_datetime',
    ]
    readonly_fields = [
        'logging_base',
        'get_data_pretty',
        'created_datetime',
        'start_datetime',
        'end_datetime',
        'time_spent',
        'time_spent_in_seconds',
    ]
    exclude = [
        'data',
    ]

    def get_data_pretty(self, obj):
        return format_html('<pre>{}</pre>', json.dumps(obj.data, indent=2, sort_keys=True))
    get_data_pretty.short_description = 'Data pretty formatted'
