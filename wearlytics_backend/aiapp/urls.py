from django.urls import path
from .views import chat_view, suggestive_question_view, register, login, token_login, generate_login_link, upload_audio,bot
from . views import dashboard
# from .views import queries_over_time
from .views import upload_audio2
from .views import broadcast
from .views import submit_text_message, submit_media_message, submit_new_number_message
from .views import upload_contacts, display_contacts
from .views import chatindex, chat_view2,submit_text_message_chat
from .views import home
from .views import settings
from .views import shut_down_backend, re_enable_backend, reload_backend

urlpatterns = [
    path('api/bot/', bot, name='bot'),
    path('api/chat/', chat_view, name='chat'),
    path('api/suggestions/', suggestive_question_view, name='suggestive_questions'),
    path('api/register/', register, name='register'),
    path('api/login/', login, name='login'),
    path('api/token-login/', token_login, name='token-login'),
    path('api/generate-login-link/<int:user_id>/', generate_login_link, name='generate-login-link'),
    path('api/upload-audio/', upload_audio, name='upload_audio'),
    # path('queries_over_time/', queries_over_time, name='queries_over_time'),
    path('dashboardhealthbot/', dashboard, name='dashboard'),
    path('broadcast/', broadcast, name='broadcast'),
    path('upload/', upload_audio2, name='upload_audio'),
    path('submit_text_message/', submit_text_message, name='submit_text_message'),
    path('submit_media_message/', submit_media_message, name='submit_media_message'),
    path('submit_new_number_message/', submit_new_number_message, name='submit_new_number_message'),
    path('upload-contacts/', upload_contacts, name='upload_contacts'),
    path('contacts/', display_contacts, name='display_contacts'),
    path('chatindex', chatindex, name='chatindex'),
    path('chat/<str:phone_number>/', chat_view2, name='chat_view'),
    path('submit_text_message_chat/', submit_text_message_chat, name='submit_text_message_chat'),
    path('', home, name='home'),
    path('settings', settings, name='settings'),
    path('shutdown-backend/', shut_down_backend, name='shutdown-backend'),
    path('re-enable-backend/', re_enable_backend, name='re-enable-backend'),
    path('reload-backend/', reload_backend, name='reload-backend'),
]
