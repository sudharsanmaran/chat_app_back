from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from chat import models


admin.site.register(models.User)
admin.site.register(models.ChatRoom)
admin.site.register(models.Message)