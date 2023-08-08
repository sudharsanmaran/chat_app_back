from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
import uuid


class CustomUserManager(BaseUserManager):

    def _create_or_update_user(self, password, user=None, **extra_fields):
        if not user:
            user = self.model(**extra_fields)
            user.set_password(password)
        else:
            for key, value in extra_fields.items():
                setattr(user, key, value)
            if password:
                user.set_password(password)

        user.save()
        return user

    def create_or_update_user(self, password, username=None, instance=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        if username:
            extra_fields.setdefault("username", username)
        return self._create_or_update_user(password=password, user=instance, **extra_fields)

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save()
        return user


class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, unique=True,
                          default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=255, unique=True, db_index=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # add config dictionary as field

    USERNAME_FIELD = "username"

    objects = CustomUserManager()

    def __str__(self):
        return self.username

    @classmethod
    def search_by_username(cls, query):
        return cls.objects.filter(username__icontains=query)


class ChatRoomManager(models.Manager):

    def create_private_chat_room(self, name, users):
        room = self.create(
            name=name, is_private=True
        )
        for user in users: 
            room.users.add(User.objects.get(pk=user.get('id')))
        room.save()
        return room

    # def create_room_or_add_user(self, room_name, user):
    #     try:
    #         chat_room = self.get(name=room_name)
    #     except ChatRoom.DoesNotExist:
    #         chat_room = self.create(name=room_name)

    #     if user not in chat_room.users.all():
    #         chat_room.users.add(user)
    #         chat_room.save()

    #     return chat_room


class ChatRoom(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, unique=True)
    users = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="chat_rooms")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_private = models.BooleanField(default=False)

    objects = ChatRoomManager()

    def __str__(self):
        return self.name


class Message(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    chat_room = models.ForeignKey(
        ChatRoom, on_delete=models.CASCADE, related_name="messages", blank=True, null=True)
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="messages_sent")
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        return f"{self.sender.username} in {self.chat_room.name}: {self.content}"
