from user.models import User
from rest_framework import viewsets
from api.serializers.serializers import IntegrationSerializer, UserSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework_simplejwt.tokens import RefreshToken
from django.db.models import Q
from datetime import datetime
import time
from cryptography.fernet import Fernet
from django.core.mail import send_mail
from integration.models import Integration
from django.contrib.auth.hashers import make_password, check_password

key = Fernet.generate_key()
fernet = Fernet(key)

class UserViewSet(viewsets.GenericViewSet):
    serializer_class = UserSerializer
    permissions_classes = [IsAuthenticated]

    @action(detail=False, methods=['POST'], url_path='signup')
    def signup(self, request):
        user_name = request.data.get('username', None)
        pass_word = request.data.get('password', None)
        mobile = request.data.get('mobile', None)
        email = request.data.get('email', None)
        if not(user_name and pass_word and mobile and email):
            return Response({'Message': "Creadientials are not provied"},
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            user = User.objects.create(username=user_name,password=make_password(pass_word),email=email,mobile=mobile)
            return Response({'message': 'User created successfully.'})
        except User.DoesNotExist:
            pass
        return Response({'Message': "Your credentials are not valid"},
                        status=status.HTTP_400_BAD_REQUEST)

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

    @action(detail=False, methods=['GET'], url_path='userme')
    def get_queryset(self, request):
        qs = User.objects.filter(id=request.user.id)
        ser = UserSerializer(qs, many=True)
        return Response(ser.data)

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

    @action(detail=False, methods=['POST'], url_path='reset_password')
    def reset_password(self, request):
        old_password = request.data.get('oldpassword', None)
        new_password = request.data.get('newpassword', None)
        re_password = request.data.get('repassword', None)
        
        user = request.user
        if check_password(old_password,user.password):
            if new_password == re_password:
                user.password = make_password(new_password)
                user.save()
                return Response({'message': 'Password change successfully'})
            return Response({'message': 'New Password and Confirm Password does not matched'},
                                status=status.HTTP_400_BAD_REQUEST)
        return Response({'message': 'Old Password is not match'},
                              status=status.HTTP_400_BAD_REQUEST)

class IntegrateData(viewsets.ModelViewSet):
    queryset = Integration.objects.all()
    serializer_class = IntegrationSerializer

    @action(detail=False, methods=['GET'], url_path='integrate')
    def get_data(self, request):
        legal_bussiness_name = request.query_params.get('legalBussinessName', None)
        license_number = request.query_params.get('licenseNumber', None)
        expiration_date = request.query_params.get('expirationDate', None)

        integrate = Integration.objects.get(Q(business_legal_name=legal_bussiness_name)|Q(license_number=license_number)|Q(expiration_date=expiration_date))
        ser = IntegrationSerializer(integrate, many=True)
        return Response(ser.data)