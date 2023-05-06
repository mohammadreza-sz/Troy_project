from django.db import models
# from django.contrib.auth import get_user_model
from Profile.models import Person
from Troy.settings import AUTH_USER_MODEL
# User = get_user_model()

# from Profile.models import Person
User = AUTH_USER_MODEL

class Chat(models.Model):
    
    class SenderType(models.TextChoices):
        server = 'SERVER'
        Client = 'CLIENT'
    
    sender = models.ForeignKey(
        User, related_name='send_chats', on_delete=models.CASCADE)
    message = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    room_name = models.CharField(max_length=250)
    sender_type= models.CharField(max_length=6, choices=SenderType.choices, null=True)



# we must modify it...
# class Contact(models.Model):
#     user = models.ForeignKey(User, on_delete = models.CASCADE)
#     friends = models.ManyToManyField('self', blank = True)

#     def __str__(self):
#         return self.user.username


# class Message(models.Model):
#     contact = models.ForeignKey(Contact, related_name='messages', on_delete= models.CASCADE)
#     content = models.TextField()
#     timestamp = models.DateTimeField(auto_now_add = True)

#     def __str__(self): 
#         return self.contact.user.username

# class Chat(models.Model):
#     participants = models.ManyToManyField(Contact, related_name= 'chats')
#     messages = models.ManyToManyField(Message, blank = True)

#     def last_30_messages():
#         return self.messages.objects.order_by('-timestamp').all()[:30]

#     def __str__(self) : 
#         return "{}".format(self.pk)