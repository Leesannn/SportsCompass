from django.contrib import admin

from .models import ExternalJobPosting, Work24FetchStatus


@admin.register(ExternalJobPosting)
class ExternalJobPostingAdmin(admin.ModelAdmin):
    list_display = ('title', 'company_name', 'source', 'region_text', 'period_text', 'fetched_at')
    search_fields = ('title', 'company_name', 'region_text')
    list_filter = ('source', 'fetched_at')
    readonly_fields = (
        'source', 'external_id', 'title', 'company_name', 'pay_text', 'career_text',
        'region_text', 'period_text', 'source_url', 'fetched_at',
    )


@admin.register(Work24FetchStatus)
class Work24FetchStatusAdmin(admin.ModelAdmin):
    list_display = ('source', 'last_checked_at', 'last_success_at', 'last_success_count')
    readonly_fields = ('source', 'last_checked_at', 'last_success_at', 'last_success_count', 'last_error')
