from django.contrib import admin

# Register your models here.
from django.contrib import admin
from compte.models import Message, User
# Register your models here.
class AdminUser(admin.ModelAdmin):
    list_display=('username','email','password','is_staff','is_active','date_joined')
admin.site.register(User,AdminUser)
###
class AdminMessage(admin.ModelAdmin):
    list_display=('sender','receiver','contenu','date','lu')
admin.site.register(Message,AdminMessage)