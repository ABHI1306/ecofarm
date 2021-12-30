from django.db import models
from django.contrib.postgres.fields import ArrayField
from bulk_update_or_create import BulkUpdateOrCreateQuerySet

class Integration(models.Model):
    """ Creating Integration model license_number is unique field 
        and activity contain array fields """
    objects = BulkUpdateOrCreateQuerySet.as_manager()

    dcc_number = models.IntegerField(verbose_name="dccnumber")
    license_number = models.CharField(max_length=225, verbose_name="licenseNumber")
    license_status = models.CharField(max_length=225, verbose_name="licenseStatus")
    license_status_date = models.DateField(verbose_name="licenseStatusDate", default=None, null=True, blank=True)
    license_term = models.CharField(max_length=225, verbose_name="licenseTerm", default=None, null=True, blank=True)
    license_type = models.CharField(max_length=225, verbose_name="licenseType")
    license_designation = models.CharField(max_length=225, verbose_name="licenseDesignation", default=None, null=True, blank=True)
    issue_date = models.DateField(verbose_name="issueDate")
    expiration_date = models.DateField(verbose_name="expirationDate")
    licensing_authority_id = models.CharField(max_length=225,verbose_name="licensingAuthorityId", default=None, null=True, blank=True)
    licensing_authority = models.CharField(max_length=225, verbose_name="licensingAuthority", default=None, null=True, blank=True)
    business_legal_name = models.CharField(max_length=500, verbose_name="businessLegalName")
    business_dba_name = models.CharField(max_length=500, verbose_name="businessDbaName",default=None, null=True, blank=True)
    business_owner_name = models.CharField(max_length=500, verbose_name="businessOwnerName", default=None, null=True, blank=True)
    business_structure = models.CharField(max_length=225, verbose_name="businessStructure", default=None, null=True, blank=True)
    activity = ArrayField(models.CharField(max_length=225), default=list, null=True, blank=True)
    premise_street_address = models.CharField(max_length=225, verbose_name="premiseStreetAddress", default=None, null=True, blank=True)
    premise_city = models.CharField(max_length=225, verbose_name="premiseCity", default=None, null=True, blank=True)
    premise_state = models.CharField(max_length=225, verbose_name="premiseState", default=None, null=True, blank=True)
    premise_county = models.CharField(max_length=225, verbose_name="premiseCounty", default=None, null=True, blank=True)
    premise_zip_code = models.CharField(max_length=225, verbose_name="premiseZipCode", default=None, null=True, blank=True)
    business_email = models.CharField(max_length=225, verbose_name="businessEmail")
    business_phone = models.CharField(max_length=225, verbose_name="businessPhone", default=None, null=True, blank=True)
    parcel_number = models.CharField(max_length=225, verbose_name="parcelNumber", default=None, null=True, blank=True)
    premise_latitude = models.FloatField(verbose_name="premiseLatitude", default=None, null=True, blank=True)
    premise_longitude = models.FloatField(verbose_name="premiseLongitude", default=None, null=True, blank=True)
    data_refreshed_date = models.DateTimeField(verbose_name="dataRefreshedDate")
