from django.db import models
from django.contrib.postgres.fields import ArrayField
from bulk_update_or_create import BulkUpdateOrCreateQuerySet

class Integration(models.Model):
    """ Creating Integration model license_number is unique field 
        and activity contain array fields """
    objects = BulkUpdateOrCreateQuerySet.as_manager()

    dcc_number = models.IntegerField(verbose_name="dcc_number")
    license_number = models.CharField(max_length=225, verbose_name="license_Number")
    license_status = models.CharField(max_length=225, verbose_name="license_Status")
    license_status_date = models.DateField(verbose_name="license_StatusDate", default=None, null=True, blank=True)
    license_term = models.CharField(max_length=225, verbose_name="license_Term", default=None, null=True, blank=True)
    license_type = models.CharField(max_length=225, verbose_name="license_Type")
    license_designation = models.CharField(max_length=225, verbose_name="license_Designation", default=None, null=True, blank=True)
    issue_date = models.DateField(verbose_name="issue_Date")
    expiration_date = models.DateField(verbose_name="expiration_Date")
    licensing_authority_id = models.CharField(max_length=225,verbose_name="licensing_AuthorityId", default=None, null=True, blank=True)
    licensing_authority = models.CharField(max_length=225, verbose_name="licensing_Authority", default=None, null=True, blank=True)
    business_legal_name = models.CharField(max_length=500, verbose_name="business_LegalName")
    business_dba_name = models.CharField(max_length=500, verbose_name="business_DbaName",default=None, null=True, blank=True)
    business_owner_name = models.CharField(max_length=500, verbose_name="business_OwnerName", default=None, null=True, blank=True)
    business_structure = models.CharField(max_length=225, verbose_name="business_Structure", default=None, null=True, blank=True)
    activity = ArrayField(models.CharField(max_length=225), default=list, null=True, blank=True)
    premise_street_address = models.CharField(max_length=225, verbose_name="premise_StreetAddress", default=None, null=True, blank=True)
    premise_city = models.CharField(max_length=225, verbose_name="premise_City", default=None, null=True, blank=True)
    premise_state = models.CharField(max_length=225, verbose_name="premise_State", default=None, null=True, blank=True)
    premise_county = models.CharField(max_length=225, verbose_name="premise_County", default=None, null=True, blank=True)
    premise_zip_code = models.CharField(max_length=225, verbose_name="premise_ZipCode", default=None, null=True, blank=True)
    business_email = models.CharField(max_length=225, verbose_name="business_Email")
    business_phone = models.CharField(max_length=225, verbose_name="business_Phone", default=None, null=True, blank=True)
    parcel_number = models.CharField(max_length=225, verbose_name="parcel_Number", default=None, null=True, blank=True)
    premise_latitude = models.FloatField(verbose_name="premise_Latitude", default=None, null=True, blank=True)
    premise_longitude = models.FloatField(verbose_name="premise_Longitude", default=None, null=True, blank=True)
    data_refreshed_date = models.DateTimeField(verbose_name="data_RefreshedDate")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="created_On")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="updated_On")
