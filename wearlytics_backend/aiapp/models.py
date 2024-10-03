from django.db import models
from django.utils import timezone

class Chat(models.Model):
    user_id = models.CharField(max_length=255)
    query = models.TextField()
    response = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Chat({self.user_id}, {self.created_at})"

class UserQuery(models.Model):
    message_internal_id = models.AutoField(primary_key=True)
    user_message = models.TextField()
    bot_response = models.TextField()
    response_message_segregation=models.TextField()
    profile_name = models.CharField(max_length=255, null=True, blank=True)
    phone_no_from = models.CharField(max_length=20, null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    message_count = models.IntegerField(default=1)
    currentstate = models.IntegerField(default=0)

class Feedback(models.Model):
    phone_no_from = models.CharField(max_length=20, null=True, blank=True)
    question = models.TextField()
    feedback = models.TextField()
    feedback_id = models.AutoField(primary_key=True)
    timestamp = models.DateTimeField(auto_now_add=True)

class Contact(models.Model):
    name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20, unique=True)
    channel =models.TextField()
    def __str__(self):
        return self.name

class AudioFile(models.Model):
    title = models.CharField(max_length=100)
    audio = models.FileField(upload_to='audios/')
    # upload_to determines where the file will be stored within MEDIA_ROOT

    def __str__(self):
        return self.title

