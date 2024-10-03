from django.contrib import admin
from .models import Chat
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from .models import UserQuery
from .models import Feedback
from .models import Contact

# Register the Chat model to make it accessible in the admin interface
@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'query', 'response', 'created_at')
    search_fields = ('user_id', 'query', 'response')
    list_filter = ('created_at',)
    ordering = ('-created_at',)

class UserQueryAdmin(admin.ModelAdmin):
    list_display = ('message_internal_id', 'profile_name',  'phone_no_from',   'bot_response', 'created_at','currentstate','response_message_segregation',"message_count",)
    list_filter = ('profile_name', 'phone_no_from')
    search_fields = ('user_message', 'bot_response', 'phone_no_from', "profile_name")
    ordering = ("-message_internal_id",)


class FeedbackAdmin(admin.ModelAdmin):
    list_display = ("feedback_id", "phone_no_from", "question", "feedback", "timestamp")
    ordering = ("feedback_id",)

class ContactAdmin(admin.ModelAdmin):
    list_display = ("name","phone_number","channel")


# Extend the default UserAdmin to customize the admin view for User
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    ordering = ('username',)

# Register the User model with the extended UserAdmin class
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
admin.site.register(Contact, ContactAdmin)
admin.site.register(UserQuery, UserQueryAdmin)
admin.site.register(Feedback, FeedbackAdmin)
