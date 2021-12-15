from django.urls import path
from rest_framework import routers
from rest_framework.routers import SimpleRouter
from api.views.views import UserViewSet, ForgotPassword

router = SimpleRouter()

router.register('user', UserViewSet, basename="user")
router.register('forgotpassword', ForgotPassword, basename="forgotpassword")

urlpatterns=[] + router.urls
