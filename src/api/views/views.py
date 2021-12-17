from django.http.response import HttpResponse
from user.models import User
from rest_framework import viewsets
from api.serializers.serializers import UserSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework_simplejwt.tokens import RefreshToken
from django.db.models import Q
import requests
from datetime import datetime
import time
from cryptography.fernet import Fernet
from django.core.mail import send_mail
from integration.models import Integration
from bulk_update.helper import bulk_update

key = Fernet.generate_key()
fernet = Fernet(key)

class UserViewSet(viewsets.GenericViewSet):
    serializer_class = UserSerializer
    permissions_classes = [IsAuthenticated]

    @action(detail=False, methods=['POST'], url_path='login')
    def login(self, request):
        user = None
        user_name = request.data.get('username', None)
        pass_word = request.data.get('password', None)
        if not(user_name and pass_word):
            return Response({'Message': "Creadientials are not provied"},
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            user = User.objects.get(Q(username=user_name)|Q(email=user_name)|Q(mobile=user_name))
            if user.check_password(pass_word):
                refresh = RefreshToken.for_user(user)
                user_data = User.objects.get(username=user)
                return Response({
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                    })
        except User.DoesNotExist:
            pass
        return Response({'Message': "Your credentials are not valid"},
                        status=status.HTTP_400_BAD_REQUEST)

    
class ForgotPassword(viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permissions_classes = [IsAuthenticated]

    @action(detail=False, methods=['POST'], url_path='send_email')
    def send_email(self, request):
        try:
            email = request.data.get('email', None)
            user = User.objects.get(email = email)
            encMessage = fernet.encrypt_at_time(str(user.id).encode(),current_time=int(time.time()))
            send_mail(
                'ForgotPassword Request',
                f'Hello { user }, Recently received a request for a forgotten password. To change your password, Please send the below link { encMessage }.',
                'abhijitshete13@gmail.com',
                [email],
                fail_silently=False,
            )
            return Response({'message': 'Email send successfully on provided mail.'})
        except:
            return Response({'message': 'Invalid Token'},status=status.HTTP_400_BAD_REQUEST)
        
    @action(detail=False, methods=['POST'], url_path='verify_email')
    def verify_email(self, request):
        verifytoken = request.data.get('verifytoken', None)
        tk = str.encode(verifytoken)
        try:
            timestamp = datetime.datetime.fromtimestamp(fernet.extract_timestamp(tk))
            user_id = fernet.decrypt_at_time(tk,ttl=3600,current_time=int(time.time())).decode()
            if User.objects.filter(id = user_id).exists():
                return Response({'message': 'Token is matched'})
        except:
            pass  
        return Response({'message': 'Invalid Token'},status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['POST'], url_path='forgot_password')
    def forgot_password(self, request):
        verifytoken = request.data.get('verifytoken', None)
        new_password = request.data.get('newpassword', None)
        tk = str.encode(verifytoken)
        try:
            user_id = fernet.decrypt_at_time(tk,ttl=3600,current_time=int(time.time())).decode()
            user = User.objects.filter(id = user_id)
            if len(user):
                user[0].set_password(new_password)
                user[0].save()
                return Response({'message': 'Password change successfully'})
        except:
            pass
        return Response({'message': 'Invalid Token'},status=status.HTTP_400_BAD_REQUEST)

class IntegrateData(viewsets.GenericViewSet):

    @action(detail=False, methods=['POST'], url_path='integrate')
    def get_data_from_url(self, request):
        url = 'https://as-cdt-pub-vip-cannabis-ww-p-002.azurewebsites.net/licenses/filteredSearch?pageSize=&pageNumber='
        totalPages = requests.get(url).json()["metadata"]["totalPages"]
        qs = Integration.objects.all()
        for page in range(1,totalPages+1):
            res = requests.get(url + str(page))
            insert_list = []
            update_list = []
            for val in res.json()["data"]:
                if Integration.objects.filter(licenseNumber=val['licenseNumber']).exists():
                    print("In Update")
                    update_list.append(Integration(dccnumber=val['id'],licenseStatus=val['licenseStatus'],
                    licenseStatusDate=self.convert(val['licenseStatusDate']),licenseTerm=val['licenseTerm'],licenseType=val['licenseType'],
                    licenseDesignation=val['licenseDesignation'],issueDate=self.convert(val['issueDate']),expirationDate=self.convert(val['expirationDate']),
                    licensingAuthorityId=val['licensingAuthorityId'],licensingAuthority=val['licensingAuthority'],businessLegalName=val['businessLegalName'],
                    businessDbaName=val['businessDbaName'],businessOwnerName=val['businessOwnerName'],businessStructure=val['businessStructure'],
                    activity=val['activity'],premiseStreetAddress=val['premiseStreetAddress'],premiseCity=val['premiseCity'],
                    premiseState=val['premiseState'],premiseCounty=val['premiseCounty'],premiseZipCode=val['premiseZipCode'],
                    businessEmail=val['businessEmail'],businessPhone=val['businessPhone'],parcelNumber=val['parcelNumber'],
                    premiseLatitude=val['premiseLatitude'],premiseLongitude=val['premiseLongitude'],dataRefreshedDate=self.convert_f(val['dataRefreshedDate'])))
                else:
                    print("In Insert")
                    insert_list.append(Integration(dccnumber=val['id'],licenseNumber=val['licenseNumber'],licenseStatus=val['licenseStatus'],
                    licenseStatusDate=self.convert(val['licenseStatusDate']),licenseTerm=val['licenseTerm'],licenseType=val['licenseType'],
                    licenseDesignation=val['licenseDesignation'],issueDate=self.convert(val['issueDate']),expirationDate=self.convert(val['expirationDate']),
                    licensingAuthorityId=val['licensingAuthorityId'],licensingAuthority=val['licensingAuthority'],businessLegalName=val['businessLegalName'],
                    businessDbaName=val['businessDbaName'],businessOwnerName=val['businessOwnerName'],businessStructure=val['businessStructure'],
                    activity=val['activity'],premiseStreetAddress=val['premiseStreetAddress'],premiseCity=val['premiseCity'],
                    premiseState=val['premiseState'],premiseCounty=val['premiseCounty'],premiseZipCode=val['premiseZipCode'],
                    businessEmail=val['businessEmail'],businessPhone=val['businessPhone'],parcelNumber=val['parcelNumber'],
                    premiseLatitude=val['premiseLatitude'],premiseLongitude=val['premiseLongitude'],dataRefreshedDate=self.convert_f(val['dataRefreshedDate'])))
            Integration.objects.bulk_create(insert_list)
            bulk_update(update_list)
            # Integration.objects.bulk_update(update_list, ['dccnumber','licenseNumber','licenseStatus','licenseStatusDate',
            # 'licenseTerm','licenseType','licenseDesignation','issueDate','expirationDate','licensingAuthorityId','licensingAuthority',
            # 'businessLegalName','businessDbaName','businessOwnerName','businessStructure','activity','premiseStreetAddress',
            # 'premiseCity','premiseState','premiseCounty','premiseZipCode','businessEmail','businessPhone','parcelNumber',
            # 'premiseLatitude','premiseLongitude','dataRefreshedDate'])
        return Response({'message': 'Fetching Data is Done'})
    
    def convert(self, date_time_str):
        if date_time_str:
            return datetime.strptime(date_time_str, "%Y-%m-%dT%H:%M:%S")

    def convert_f(self, date_time_str):
        if date_time_str:
            return datetime.strptime(date_time_str, "%Y-%m-%dT%H:%M:%S.%f")
