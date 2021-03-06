from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

class Room(models.Model):
    """
    a chat room model
    """

    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name='created_rooms')
    members = models.ManyToManyField(settings.AUTH_USER_MODEL, 
        related_name='rooms')
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True, null=True)
    public = models.BooleanField(default=True)
    created = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name

class Message(models.Model):
    """
    chat message
    """

    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name='chat_messages')
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='messages',
        null=True, blank=True)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.body[:10] + ' ...'

    class Meta:
        ordering = ('created',)

@receiver(post_save, sender=Room)
def post_save_room_receiver(sender, instance, created, **kwargs):
    if created:
        instance.members.add(instance.creator)