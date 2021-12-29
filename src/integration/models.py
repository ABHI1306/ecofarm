from django.db import models
from django.contrib.postgres.fields import ArrayField
from bulk_update_or_create import BulkUpdateOrCreateQuerySet

class Integration(models.Model):
    """ Creating Integration model license_number is unique field 
        and activity contain array fields """
    
    dcc_number = models.IntegerField(verbose_name="dccnumber", default=None)
    license_number = models.CharField(max_length=225, verbose_name="licenseNumber", default=None)
    license_status = models.CharField(max_length=225, verbose_name="licenseStatus", default=None)
    license_status_date = models.DateField(null=True, verbose_name="licenseStatusDate", default=None)
    license_term = models.CharField(max_length=225, verbose_name="licenseTerm", default=None)
    license_type = models.CharField(max_length=225, verbose_name="licenseType", default=None)
    license_designation = models.CharField(max_length=225, verbose_name="licenseDesignation", default=None)
    issue_date = models.DateField(verbose_name="issueDate", default=None)
    expiration_date = models.DateField(verbose_name="expirationDate", default=None)
    licensing_authority_id = models.CharField(max_length=225,verbose_name="licensingAuthorityId", default=None)
    licensing_authority = models.CharField(max_length=225, verbose_name="licensingAuthority", default=None)
    business_legal_name = models.CharField(max_length=500, verbose_name="businessLegalName", default=None)
    business_dba_name = models.CharField(max_length=500, verbose_name="businessDbaName", null=True, blank=True)
    business_owner_name = models.CharField(max_length=500, verbose_name="businessOwnerName", default=None)
    business_structure = models.CharField(max_length=225, verbose_name="businessStructure", default=None)
    activity = ArrayField(models.CharField(max_length=225),default=list)
    premise_street_address = models.CharField(max_length=225, verbose_name="premiseStreetAddress", default=None)
    premise_city = models.CharField(max_length=225, verbose_name="premiseCity", default=None)
    premise_state = models.CharField(max_length=225, verbose_name="premiseState", default=None)
    premise_county = models.CharField(max_length=225, verbose_name="premiseCounty", default=None)
    premise_zip_code = models.CharField(max_length=225, verbose_name="premiseZipCode", default=None)
    business_email = models.CharField(max_length=225, verbose_name="businessEmail", default=None)
    business_phone = models.CharField(max_length=225, verbose_name="businessPhone", default=None)
    parcel_number = models.CharField(max_length=225, verbose_name="parcelNumber", default=None)
    premise_latitude = models.FloatField(null=True, verbose_name="premiseLatitude", default=None)
    premise_longitude = models.FloatField(null=True, verbose_name="premiseLongitude", default=None)
    data_refreshed_date = models.DateTimeField(verbose_name="dataRefreshedDate", default=None)
