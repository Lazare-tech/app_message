from django.urls import path,include
import compte.views
#
app_name= "compte"
urlpatterns = [
    path('login/',compte.views.login_page,name='login'),
    path('signup/',compte.views.signup_page,name='signup'),
    path('logout/',compte.views.logout_user,name='logout'),
    # path('delete_account',compte.views.delete_account,name='delete_account'),
    path('message/',compte.views.message,name='message'),
        path('send/',compte.views.send_message,name='send_message'),
            path('reponse/<int:message_id>/', compte.views.rep_message, name='rep_message'),


    
]