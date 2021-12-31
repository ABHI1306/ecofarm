from django.contrib import admin
from .models import Integration
from rangefilter.filter import DateRangeFilter
from import_export.admin import ExportActionMixin

class ArrayFieldListFilter(admin.SimpleListFilter):
    """This is a list filter based on the values
    from a model's `activity` ArrayField. """

    title = 'Activity'
    parameter_name = 'activity'

    def lookups(self, request, model_admin):
        activity = Integration.objects.values_list("activity", flat=True)  
        activity = [(kw, kw) for sublist in activity for kw in sublist if kw]
        activity = sorted(set(activity))
        return activity

    def queryset(self, request, queryset):
        lookup_value = self.value()
        if lookup_value:
            queryset = queryset.filter(activity__contains=[lookup_value])
        return queryset

class IntegrationAdmin(ExportActionMixin, admin.ModelAdmin):
    list_display = ('business_legal_name', 'license_number', 'expiration_date', 'business_dba_name', 'activity', 'created_at', 'updated_at')
    search_fields = ('business_legal_name', 'license_number', 'business_dba_name')
    list_filter = (ArrayFieldListFilter, 'license_status', ('issue_date', DateRangeFilter), ('expiration_date', DateRangeFilter), 'licensing_authority')
    readonly_fields = ('dcc_number','license_number','license_status','license_status_date','license_term','license_type',
    'license_designation','issue_date','expiration_date','licensing_authority_id','licensing_authority','business_legal_name',
    'business_dba_name','business_owner_name','business_structure','activity','premise_street_address','premise_city',
    'premise_state','premise_county','premise_zip_code','business_email','business_phone','parcel_number','premise_latitude',
    'premise_longitude','data_refreshed_date','created_at','updated_at')
admin.site.register(Integration, IntegrationAdmin)