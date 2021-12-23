from django.contrib import admin
from .models import User

# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'mobile', 'verification', 'last_login')
    search_fields = ('username', 'email', 'mobile')
    readonly_fields = ('id',)
    
admin.site.register(User, UserAdmin)
