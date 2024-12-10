from pyexpat.errors import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from compte.forms import LoginForm, MessageForm, Messageform, SignupForm
from compte.models import Message, User
from django.contrib.auth import login, authenticate,logout
from django.contrib.auth.decorators import login_required
# Create your views here.

def login_page(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')

            try:
                # On cherche d'abord un utilisateur ayant cet email
                user = User.objects.get(email=email)
                # Ensuite, on vérifie que le mot de passe est correct
                user = authenticate(request, username=user.username, password=password)
                
                if user is not None:
                    login(request, user)
                    return redirect('app_user:homepage')  # Redirige vers le tableau de bord après connexion
                else:
                    form.add_error(None, 'Identifiants invalides.')
            except User.DoesNotExist:
                form.add_error(None, "Aucun utilisateur n'est enregistré avec cet email.")
    else:
        form = LoginForm()

    return render(request, 'compte/login.html', {'form': form})
#####

def signup_page(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            print("email:",email,"username:",username)
            # Créer l'utilisateur avec un mot de passe haché
            # Création manuelle de l'utilisateur avec hachage du mot de passe
            user = User(username=username, email=email)
            user.set_password(password)  # Hacher manuellement le mot de passe
            user.save()
            
            return redirect('compte:login')
    else:
        form = SignupForm()

    return render(request, 'compte/signup.html', {'form': form})
#####
def logout_user(request):
    logout(request)
    
    return redirect('app_user:homepage')
##
@login_required
def message(request):
    user=request.user
    messages=Message.objects.filter(receiver=user).order_by('-date').prefetch_related('responses')
    messages_envoyer=Message.objects.filter(sender=user).order_by('-date')

    ###
    messages_non_lu=0
    if request.user.is_authenticated:
        messages_non_lu=Message.objects.filter(receiver=request.user)
        message_sans_reponse=messages_non_lu.filter(responses__isnull=True)
        messages_non_lu_nombre = message_sans_reponse.count()
  
    context={
        'messages':messages,
        'message_non_lu_nombre':messages_non_lu_nombre,
        'messages_envoyer':messages_envoyer
    }
    return render(request,'compte/inbox.html',context)
#####
@login_required
def send_message(request):
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            username=form.cleaned_data['receiver']
            receiver=get_object_or_404(User,username=username)
            message=form.cleaned_data['contenu']
            message=Message(sender=request.user,receiver=receiver,contenu=message)
            message.save()
            return redirect('compte:message')  # Redirige vers une page de confirmation ou autre
    else:
        form = MessageForm()
    
    return render(request, 'compte/send_message.html', {'form': form})
####

def rep_message(request, message_id):
    # Récupérer le message auquel l'utilisateur veut répondre
    messages = get_object_or_404(Message, id=message_id)
    
    # Si le formulaire est soumis
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            response_message = form.save(commit=False)
            response_message.sender = request.user
            response_message.receiver = messages.sender  # L'expéditeur du message original est maintenant le destinataire
            response_message.response_to=messages
            response_message.save()

            return redirect('compte:message')  # Rediriger vers la boîte de réception après l'envoi

    else:
        # Pré-remplir le formulaire pour la réponse
        form = MessageForm(initial={'receiver': messages.sender})

    return render(request, 'compte/reponse.html', {'form': form, 'messages':messages})