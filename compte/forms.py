from django.contrib.auth import get_user_model
from django import forms

from compte.models import Message

##################3 
User = get_user_model()  # Récupère le modèle d'utilisateur personnalisé

class LoginForm(forms.Form):
    # Utilisation de l'email pour la connexion
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control'}),
        max_length=63,
        label="Email",
        error_messages={
            'required': ('Le mail est requis.'),
            'invalid': ('Veuillez entrer une adresse email valide.')
        }
    )

    password = forms.CharField(
        max_length=63,
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label='Mot de passe',
        error_messages={
            'required': ('Le mot de passe est requis.')
        }
    )
    ###
    
class SignupForm(forms.ModelForm):  # Utilisation de ModelForm pour se baser sur le modèle User
    username = forms.CharField(
        max_length=63,
        label=('Nom d’utilisateur'),
        error_messages={
            'required': ('Le nom d’utilisateur est requis.'),
            'max_length': ('Le nom d’utilisateur ne peut pas dépasser 63 caractères.')
        },
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control'}),
        label=('Email'),
        error_messages={
            'required': ('Le mail est requis.'),
            'invalid': ('Veuillez entrer une adresse email valide.')
        }
    )

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label=('Mot de passe'),
        min_length=6,
        error_messages={
            'required': ('Le mot de passe est requis.'),
            'min_length': ('Le mot de passe doit contenir au moins 6 caractères.')
        }
    )

    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label=('Confirmer le mot de passe'),
        error_messages={
            'required': ('La confirmation du mot de passe est requise.')
        }
    )

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', ('Les mots de passe ne correspondent pas.'))

    class Meta:
        model = User  # Utilisation du modèle User personnalisé
        fields = ['username', 'email', 'password']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control'})
        }
###
class Messageform(forms.Form):
    username = forms.ModelChoiceField(
        queryset=User.objects.all(),  # Récupère tous les utilisateurs

        label=('Nom d’utilisateur'),
        error_messages={
            'required': ('Le nom d’utilisateur est requis.'),
            'max_length': ('Le nom d’utilisateur ne peut pas dépasser 63 caractères.')
        },
        widget=forms.Select(attrs={'class': 'form-control'})
    )
     
    message = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control', 
            'rows': 10, 
            'cols': 11, 
            'placeholder': 'Entrez votre message ici...'
        }),
        label='Message',
        error_messages={
            'required': 'Le message est vide.',
            'invalid': 'Veuillez envoyer un message valide.'
        }
    )
   
   
   
class MessageForm(forms.ModelForm):
    # Define the field for secondary images correctly

    class Meta:
        model = Message
        fields = ['receiver', 'contenu']
        widgets = {
           
            'contenu': forms.Textarea(attrs={'class': 'form-control'}),
           
            'receiver': forms.Select(attrs={'class': 'form-control'}),
          
        }
        
    
    def clean_contenu(self):
        message = self.cleaned_data.get('contenu')
     
        if(message==''):
            raise forms.ValidationError("Message vide")

        return message
    #
    def clean_receiver(self):
        receveur = self.cleaned_data.get('receiver')
     
        if(receveur==''):
            raise forms.ValidationError("Choisir votre destinataire")

        return receveur

