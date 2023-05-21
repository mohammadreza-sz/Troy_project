from django.db import models

from django.conf import settings
# class settings.AUTH_USER_MODEL(models.Model):
#     username = models.CharField(max_length=50, unique=True)
#     email = models.EmailField(unique=True)
#     password = models.CharField(max_length=255)
#     profile_picture = models.ImageField(upload_to='profile_pics/', blank=True)

class Conversation(models.Model):
    room_name = models.CharField(max_length=10 , primary_key=True)
    # participants = models.ManyToManyField(settings.AUTH_USER_MODEL)
    created_at = models.DateTimeField(auto_now_add=True , null = True)

class Message(models.Model):
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='received_messages')
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE)

# class Notification(models.Model):
#     recipient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#     message = models.TextField()
#     timestamp = models.DateTimeField(auto_now_add=True)

class Connection(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE , null =True)
    status = models.BooleanField(default=False , null =True)
    last_seen = models.DateTimeField(auto_now=True , null = True)
    device_info = models.CharField(max_length=255, blank=True , null = True)

# class Group(models.Model):
#     name = models.CharField(max_length=50, unique=True)
#     members = models.ManyToManyField(settings.AUTH_USER_MODEL)

# class Bot(models.Model):
#     name = models.CharField(max_length=50)
#     profile_picture = models.ImageField(upload_to='bot_pics/', blank=True)
#     # Add any other fields that define your bot's behavior

