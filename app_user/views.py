from django.shortcuts import render

from compte.models import Message

# Create your views here.
def home(request):
    messages_non_lu=0
    if request.user.is_authenticated:
        messages_non_lu=Message.objects.filter(receiver=request.user,lu=False).count()
        print('ssss',messages_non_lu)
    context={
        'messages':messages_non_lu
    }
    return render(request,'app_user/body/index.html',context)