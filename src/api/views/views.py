from user.models import User
from rest_framework import viewsets
from api.serializers.serializers import IntegrationSerializer, UserSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework_simplejwt.tokens import RefreshToken
from django.db.models import Q
from integration.models import Integration
from integration.paginations import StandardResultsSetPagination
from .user_email import send_activation_email, verify_email_by_token
from django.contrib.auth.hashers import check_password, make_password
import django_filters

class UserViewSet(viewsets.GenericViewSet):
    """ Create ViewSet for performing User API """
    serializer_class = UserSerializer
    permissions_classes = [IsAuthenticated]

    @action(detail=False, methods=['POST'], url_path='signup')
    def signup(self, request):
        """ Getting data from request and create new User """
        user_name = request.data.get('username', None)
        pass_word = request.data.get('password', None)
        mobile = request.data.get('mobile', None)
        email = request.data.get('email', None)
        if not(user_name and pass_word and mobile and email):
            return Response({'Message': "Creadientials are not provied"},
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            User.objects.create(username=user_name,password=make_password(pass_word),email=email,mobile=mobile,is_active=False)
            send_activation_email(email,sub_='Activate Account',msg_='Activate your account here://127.0.0.1:8000/api/user/verify_email/?verifytoken=')
            return Response({'message': 'User created successfully.'})
        except User.DoesNotExist:
            pass
        return Response({'Message': "Your credentials are not valid"},
                status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['POST'], url_path='login')
    def login(self, request):
        """ User is able to login with username/mobilenumber/email """
        user = None
        user_name = request.data.get('username', None)
        pass_word = request.data.get('password', None)
        if not(user_name and pass_word):
            return Response({'Message': "Creadientials are not provied"},
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            user = User.objects.get(Q(username=user_name)|Q(email=user_name)|Q(mobile=user_name))
            if user.check_password(pass_word):
                user.is_active = True
                user.save()
                refresh = RefreshToken.for_user(user)
                access = refresh.access_token
                return Response({
                    'refresh': str(refresh),
                    'access': str(access),
                    'expires_in(SEC)': int(access.lifetime.total_seconds()),
                    'is_verify' : str(user.verification),
                    })
        except User.DoesNotExist:
            pass
        return Response({'Message': "Your credentials are not valid"},
                        status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['GET'], url_path='logout')
    def logout(self, request):
        """ User able to logout with token """
        user = request.user
        if User.objects.filter(id = user.id).exists():
            User.objects.filter(id = user.id).update(is_active=False)
            return Response({'message': 'User Logout successfully.'})
        return Response({'message': 'User are not authenticated.'},status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['GET'], url_path='verify_email')
    def verify_email(self, request):
        """ Getting token from request if token is valid then email verification is done otherwise verification is not done. """
        verifytoken = request.query_params.get('verifytoken')
        try:
            tk = str.encode(verifytoken)
            user = verify_email_by_token(tk)
            val = user.split("%")
            if User.objects.filter(id = val[0]).exists() and val[1] == 'Activate Account':
                User.objects.filter(id = val[0]).update(verification=True)
            return Response({'message': 'Token is verify successfully.'})
        except:
            pass
        return Response({'message': 'Invalid Token'},status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['GET'], url_path='me')
    def get_userme(self, request):
        """ API giving logged in User Info. """
        qs = User.objects.filter(id=request.user.id).first()
        ser = UserSerializer(qs)
        return Response(ser.data)

class ForgotPassword(viewsets.GenericViewSet):
    """ Create ViewSet for performing Password related API """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permissions_classes = [IsAuthenticated]

    @action(detail=False, methods=['POST'], url_path='forgot_password')
    def forgot_password(self, request):
        """ In case User forgot password then getting token for updating new password. """
        email = request.data.get('email', None)
        user = User.objects.get(email = email)
        if not user:
            return Response({'message': 'No User found with this Email.'})
        try:
            send_activation_email(email,sub_='Reset Password',msg_='Verify your account here //127.0.0.1:8000/api/forgotpassword/verify_email_forgot/?verifytoken=')
            return Response({'message': 'Email send successfully.'})
        except:
            pass
        return Response({'Message': "Your credentials are not valid"},
                status=status.HTTP_400_BAD_REQUEST) 

    @action(detail=False, methods=['POST'], url_path='verify_email_forgot')
    def verify_email_forgot(self, request):
        verifytoken = request.query_params.get('verifytoken')
        new_password = request.data.get('newpassword', None)
        try:
            tk = str.encode(verifytoken)
            user = verify_email_by_token(tk)
            val = user.split("%")
            if User.objects.filter(id = val[0]).exists() and val[1] == 'Reset Password':
                User.objects.filter(id = val[0]).update(password=make_password(new_password))
            return Response({'message': 'Password change successfully.'})
        except:
            pass
        return Response({'message': 'Invalid Token'},status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['POST'], url_path='reset_password')
    def reset_password(self, request):
        """ In case User want to change existing password with new password. """
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

class IntegrationFilter(django_filters.FilterSet):
    """ Customize Filtering """
    class Meta:
        model = Integration
        fields = {
            'business_legal_name': ['exact', 'icontains'],
            'license_number' : ['exact'],
            'expiration_date' : ['exact'],
        }

class IntegrateData(viewsets.ModelViewSet):
    """ Create ViewSet for getting Integration Info. """
    queryset = Integration.objects.all()
    serializer_class = IntegrationSerializer
    pagination_class = StandardResultsSetPagination
    filterset_class = IntegrationFilter

