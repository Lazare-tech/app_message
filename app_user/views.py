from django.shortcuts import render

from compte.models import Message

# Create your views here.
def home(request):
    messages_non_lu_nombre=0
    if request.user.is_authenticated:
        messages_non_lu=Message.objects.filter(receiver=request.user)
        message_sans_reponse=messages_non_lu.filter(responses__isnull=True)
        messages_non_lu_nombre = message_sans_reponse.count()

    context={
        'message_non_lu_nombre':messages_non_lu_nombre
    }
    return render(request,'app_user/body/index.html',context)