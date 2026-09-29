from django.contrib import admin

from .models import Application, CenterContact, JobPosting, PhoneIdentity


@admin.register(PhoneIdentity)
class PhoneIdentityAdmin(admin.ModelAdmin):
    list_display = ('phone_masked', 'first_seen_at')
    search_fields = ('phone_masked',)
    readonly_fields = ('phone_hash', 'phone_masked', 'first_seen_at')


@admin.register(CenterContact)
class CenterContactAdmin(admin.ModelAdmin):
    list_display = ('institution_name', 'phone_masked', 'institution', 'verified_at')
    search_fields = ('institution_name', 'phone_masked', 'business_reg_no')
    list_filter = ('verified_at',)
    autocomplete_fields = ('institution',)
    readonly_fields = ('phone_hash', 'phone_masked')


@admin.register(JobPosting)
class JobPostingAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'manager', 'employment_type', 'status', 'pay_amount', 'headcount')
    search_fields = ('title', 'manager__institution_name', 'sport__name', 'address')
    list_filter = ('status', 'employment_type', 'sport', 'pay_type')
    date_hierarchy = 'created_at'
    autocomplete_fields = ('manager', 'sport')


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('job_posting', 'phone_masked', 'certification_verified', 'applied_at')
    search_fields = ('phone_masked', 'job_posting__manager__institution_name')
    list_filter = ('certification_verified', 'applied_at')
    readonly_fields = ('phone_identity', 'phone_masked', 'applied_at')
