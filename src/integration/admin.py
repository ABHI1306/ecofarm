from django.contrib import admin
from .models import Integration
from django.contrib.admin import DateFieldListFilter

class IntegrationAdmin(admin.ModelAdmin):
    list_display = ('business_legal_name', 'license_number', 'expiration_date', 'business_dba_name', 'activity')
    search_fields = ('business_legal_name', 'license_number', 'business_dba_name')
    list_filter = ('activity', 'license_status', ('issue_date',DateFieldListFilter), ('expiration_date',DateFieldListFilter), 'licensing_authority')
    readonly_fields = ('dcc_number','license_number','license_status','license_status_date','license_term','license_type',
    'license_designation','issue_date','expiration_date','licensing_authority_id','licensing_authority','business_legal_name',
    'business_dba_name','business_owner_name','business_structure','activity','premise_street_address','premise_city',
    'premise_state','premise_county','premise_zip_code','business_email','business_phone','parcel_number','premise_latitude',
    'premise_longitude','data_refreshed_date')

admin.site.register(Integration, IntegrationAdmin)