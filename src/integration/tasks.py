from __future__ import absolute_import, unicode_literals
import requests
from integration.models import Integration
from bulk_update.helper import bulk_update
from core import celery_app
from rest_framework.response import Response
from dateutil import parser

@celery_app.task
def get_data_from_url():
    url = 'https://as-cdt-pub-vip-cannabis-ww-p-002.azurewebsites.net/licenses/filteredSearch?pageSize=&pageNumber='
    totalPages = requests.get(url).json()["metadata"]["totalPages"]
    for page in range(1,totalPages+1):
        res = requests.get(url + str(page))
        insert_list = []
        update_list = []
        for val in res.json()["data"]:
            if Integration.objects.filter(licenseNumber=val['licenseNumber']).exists():
                update_list.append(Integration(dccnumber=val['id'],licenseStatus=val['licenseStatus'],
                licenseStatusDate=convert(val['licenseStatusDate']),licenseTerm=val['licenseTerm'],licenseType=val['licenseType'],
                licenseDesignation=val['licenseDesignation'],issueDate=convert(val['issueDate']),expirationDate=convert(val['expirationDate']),
                licensingAuthorityId=val['licensingAuthorityId'],licensingAuthority=val['licensingAuthority'],businessLegalName=val['businessLegalName'],
                businessDbaName=val['businessDbaName'],businessOwnerName=val['businessOwnerName'],businessStructure=val['businessStructure'],
                activity=val['activity'],premiseStreetAddress=val['premiseStreetAddress'],premiseCity=val['premiseCity'],
                premiseState=val['premiseState'],premiseCounty=val['premiseCounty'],premiseZipCode=val['premiseZipCode'],
                businessEmail=val['businessEmail'],businessPhone=val['businessPhone'],parcelNumber=val['parcelNumber'],
                premiseLatitude=val['premiseLatitude'],premiseLongitude=val['premiseLongitude'],dataRefreshedDate=convert(val['dataRefreshedDate'])))
            else:
                insert_list.append(Integration(dccnumber=val['id'],licenseNumber=val['licenseNumber'],licenseStatus=val['licenseStatus'],
                licenseStatusDate=convert(val['licenseStatusDate']),licenseTerm=val['licenseTerm'],licenseType=val['licenseType'],
                licenseDesignation=val['licenseDesignation'],issueDate=convert(val['issueDate']),expirationDate=convert(val['expirationDate']),
                licensingAuthorityId=val['licensingAuthorityId'],licensingAuthority=val['licensingAuthority'],businessLegalName=val['businessLegalName'],
                businessDbaName=val['businessDbaName'],businessOwnerName=val['businessOwnerName'],businessStructure=val['businessStructure'],
                activity=val['activity'],premiseStreetAddress=val['premiseStreetAddress'],premiseCity=val['premiseCity'],
                premiseState=val['premiseState'],premiseCounty=val['premiseCounty'],premiseZipCode=val['premiseZipCode'],
                businessEmail=val['businessEmail'],businessPhone=val['businessPhone'],parcelNumber=val['parcelNumber'],
                premiseLatitude=val['premiseLatitude'],premiseLongitude=val['premiseLongitude'],dataRefreshedDate=convert(val['dataRefreshedDate'])))
        Integration.objects.bulk_create(insert_list)
        bulk_update(update_list)
    return Response({'message': 'Fetching Data is Done'})

def convert(date_time_str):
    if date_time_str:
        return parser.parse(date_time_str)
