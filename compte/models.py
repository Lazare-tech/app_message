from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
class User(AbstractUser):
    pass
###
class Message(models.Model):
    sender=models.ForeignKey(User,related_name='message_envoye',on_delete=models.CASCADE,verbose_name='message envoye par')
    receiver=models.ForeignKey(User,related_name='message_recu',on_delete=models.CASCADE,verbose_name="message recu")
    contenu=models.TextField(verbose_name='contenu message')
    date=models.DateTimeField(verbose_name='Date heure',auto_now=True)
    lu=models.BooleanField(default=False)
    response_to = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='responses')  # Réponse associée

    
    def __str__(self):
        return f'De {self.sender.username} a {self.receiver.username}'