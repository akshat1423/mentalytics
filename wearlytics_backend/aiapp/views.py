from rest_framework.exceptions import ParseError
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken

from .models import Feedback
from .models import UserQuery
from .models import Contact
from .models import Chat

from .forms import CSVUploadForm
from .forms import AudioFileForm

from django.http import JsonResponse
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.contrib import messages
from django.urls import path
from django.shortcuts import render, redirect
from django.db import IntegrityError
from django.db.models import Count, Max
from django.contrib.auth.decorators import user_passes_test
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.core.files.storage import default_storage
from django.core.files import File

from .serializers import ChatSerializer

import google.generativeai as genai
import assemblyai as aai
import speech_recognition as sr
from pydub import AudioSegment
from heyoo import WhatsApp
from decouple import config

import json
import requests
import os
import csv
import time
from datetime import datetime, timedelta
from urllib.parse import quote
from pathlib import Path
PHONE_NUM_ID=config('PHONE_NUM_ID')
WHATSAPP_TOKEN=config('WHATSAPP_TOKEN')
messenger = WhatsApp(token=config('WHATSAPP_TOKEN'),phone_number_id=config('PHONE_NUM_ID'))
GOOGLE_API_KEY=config('GOOGLE_API_KEY')
ASSEMBLYAI_API_KEY=config('ASSEMBLYAI_API_KEY'  )

genai.configure(api_key=GOOGLE_API_KEY)

# @csrf_exempt
# def bot(request):
#     if (request.GET.get('hub.mode') == 'subscribe' and
#             request.GET.get('hub.verify_token') == "HELLO"):
#             return HttpResponse(request.GET.get('hub.challenge'))

#     else:
#             return HttpResponse('Error, invalid token', status=403)
#     response = messenger.send_message(
#         message=str("Testing"),
#         recipient_id="918128612391"
#     )
#     return HttpResponse(status=200)



def get_completion_from_messages(message):
    model = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            system_instruction="You are a mental health expert . Give adises in points format, dont give bullet points in 40 words with no formatting of bold etc."
        )
    response = model.generate_content([message])
    response_mess = response.text.strip()
    return response_mess

def message_segregator(message):
    model = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            system_instruction="""what user wants to do from the following category(respond in one word) : "is the user asking a query about is mental health ? then say "query"/(if want to know about platform or feels new user say = know)/"want to give feedback or exit or has finished with his questions say feedback"""
        )
    response = model.generate_content([message])
    response_mess = response.text.strip()
    return response_mess

def messangerbot(body,phone_no_from):
                response = messenger.send_message(
                message=(body),
                recipient_id=phone_no_from,
        )




def messagebutton(header,body,button1,button2,button3,button4,phone_no_from):
                response = messenger.send_button(
                recipient_id=phone_no_from,
                button={
                    "header": "Mentalytics-"+header,
                    "body": body,
                    # "footer": "Evolving Planet",
                    "action": {
                        "button": "Choose an option",
                        "sections": [
                            {
                                "title": "iBank",
                                "rows": [
                                    {"id": "row 1", "title": button1, "description": ""},
                                    {"id": "row 2", "title": button2, "description": ""},
                                    {"id": "row 3", "title": button3, "description": ""},
                                    {"id": "row 4", "title": button4, "description": ""},
                                ],
                            }
                        ],
                    },
                },
            )

def ask_to_feedback_message(phone_no_from):
                # print("hi")
                url = f"https://graph.facebook.com/v18.0/{PHONE_NUM_ID}/messages"
                headers = {
        'Authorization': f'Bearer {WHATSAPP_TOKEN}'
    }

                data = {
                    "recipient_type": "individual",
                    "messaging_product": "whatsapp",
                    "to": phone_no_from,
                    "type": "interactive",
                    "interactive": {
                        "type": "list",
                        # "header": {
                        #     "type": "text",
                        #     "text": "A.Y.U.R"
                        # },
                        "body": {
                            "text": "Would you like to answer some questions, This would help us improve our services. 😊"
                        },
                        # "footer": {
                        #     "text": "Evolving Planet"
                        # },
                        "action": {
                            "button": "Choose an option",
                            "sections": [
                                {
                                    "rows": [
                                        {
                                            "id": "1",
                                            "title": "🌟",
                                            "description": "Yes"
                                        },
                                        {
                                            "id": "2",
                                            "title": "😊",
                                            "description": "No"
                                        }
                                    ]
                                }
                            ]
                        }
                    }
                }
                response = requests.post(url, json=data, headers=headers)
                print(response.text)

def send_feedback_message(Question,phone_no_from):
                url = f"https://graph.facebook.com/v18.0/{PHONE_NUM_ID}/messages"
                headers = {
        'Authorization': f'Bearer {WHATSAPP_TOKEN}'
    }

                data = {
                    "recipient_type": "individual",
                    "messaging_product": "whatsapp",
                    "to": phone_no_from,
                    "type": "interactive",
                    "interactive": {
                        "type": "list",
                        # "header": {
                        #     "type": "text",
                        #     "text": "A.Y.U.R"
                        # },
                        "body": {
                            "text": Question
                        },
                        # "footer": {
                        #     "text": "Evolving Planet"
                        # },
                        "action": {
                            "button": "Choose an option",
                            "sections": [
                                {
                                    "rows": [
                                        {
                                            "id": "1",
                                            "title": "5",
                                            "description": "Awesome 🌟"
                                        },
                                        {
                                            "id": "2",
                                            "title": "4",
                                            "description": "Good 😊"
                                        },
                                        {
                                            "id": "3",
                                            "title": "3",
                                            "description": "Average 👍"
                                        },
                                        {
                                            "id": "4",
                                            "title": "2",
                                            "description": "Poor 👎"
                                        },
                                        {
                                            "id": "5",
                                            "title": "1",
                                            "description": "Very Poor 😞"
                                        }
                                    ]
                                }
                            ]
                        }
                    }
                }

                response = requests.post(url, json=data, headers=headers)
                print(response.text)

def send_interactive_message(row1_description, row2_description, row3_description, row4_description,phone_no_from):
                url = f"https://graph.facebook.com/v18.0/{PHONE_NUM_ID}/messages"
                headers = {
        'Authorization': f'Bearer {WHATSAPP_TOKEN}'
    }

                data = {
                    "recipient_type": "individual",
                    "messaging_product": "whatsapp",
                    "to": phone_no_from,
                    "type": "interactive",
                    "interactive": {
                        "type": "list",
                        # "header": {
                        #     "type": "text",
                        #     "text": "A.Y.U.R"
                        # },
                        "body": {
                            "text": "Some suggestive questions to ask based on your conversation till now:😉 "
                        },
                        # "footer": {
                        #     "text": "Evolving Planet"
                        # },
                        "action": {
                            "button": "Choose an option",
                            "sections": [
                                {
                                    "rows": [
                                        {
                                            "id": "1",
                                            "title": "1",
                                            "description": row1_description
                                        },
                                        {
                                            "id": "2",
                                            "title": "2",
                                            "description": row2_description
                                        },
                                        {
                                            "id": "3",
                                            "title": "3",
                                            "description": row3_description
                                        },
                                        {
                                            "id": "4",
                                            "title": "4",
                                            "description": row4_description
                                        }
                                    ]
                                }
                            ]
                        }
                    }
                }

                response = requests.post(url, json=data, headers=headers)
                print(response.text)

def split_string(text, chunk_size=1300):
        return [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]

def messagebutton_together(header,body,row1_description, row2_description, row3_description, row4_description,phone_no_from):
                response = messenger.send_button(
                recipient_id=phone_no_from,
                button={
                    "header": header,
                    "body": body,
                    "footer": "Also find some suggestive question below: 😉",
                    "action": {
                        "button": "Suggested Questions",
                        "sections": [
                            {
                                # "title": "iBank",
                                "rows": [

                                     {
                                            "id": "1",
                                            "title": "1",
                                            "description": row1_description
                                        },
                                        {
                                            "id": "2",
                                            "title": "2",
                                            "description": row2_description
                                        },
                                        {
                                            "id": "3",
                                            "title": "3",
                                            "description": row3_description
                                        },
                                        {
                                            "id": "4",
                                            "title": "4",
                                            "description": row4_description
                                        },

                                ],
                            }
                        ],
                    },
                },
            )

@csrf_exempt
def bot(request):
    try:
        bodyy=json.loads(request.body.decode('utf-8'))
        if 'statuses' in bodyy['entry'][0]['changes'][0]['value']:
            # If statuses exist
            statuses = bodyy['entry'][0]['changes'][0]['value']['statuses']
            # Process statuses
            print("Statuses exist:")
        else:
            # If statuses do not exist
            print("No statuses found.")

            if bodyy['entry'][0]['changes'][0]['value']['messages'][0]['type'] == 'audio':
                print("audio")
                message_id = bodyy['entry'][0]['changes'][0]['value']['messages'][0]['id']
                messenger.mark_as_read(message_id)
                timestamp = int(bodyy['entry'][0]['changes'][0]['value']['messages'][0]['timestamp'])
                message_time = datetime.utcfromtimestamp(timestamp)
                current_time = datetime.utcnow()
                time_difference = current_time - message_time
                if time_difference > timedelta(hours=1):
                    print(bodyy)
                    print("ignoring message")
                    print("Message Time:", message_time)
                    print("Time Difference:", time_difference)
                    return HttpResponse(status=200)
                phone_no_from =  bodyy['entry'][0]['changes'][0]['value']['messages'][0]['from']
                process_audio_from_link(bodyy['entry'][0]['changes'][0]['value']['messages'][0]['audio']['id'],bodyy,phone_no_from)
            else:
                print(bodyy)
                message_id = bodyy['entry'][0]['changes'][0]['value']['messages'][0]['id']
                messenger.mark_as_read(message_id)
                timestamp = int(bodyy['entry'][0]['changes'][0]['value']['messages'][0]['timestamp'])
                message_time = datetime.utcfromtimestamp(timestamp)
                current_time = datetime.utcnow()

                time_difference = current_time - message_time
                if time_difference > timedelta(hours=1):
                    print(bodyy)
                    print("ignoring message")
                    print("Message Time:", message_time)
                    print("Time Difference:", time_difference)
                    return HttpResponse(status=200)

                phone_no_from = "None"
                profile_name = "None"
                message_from_user = "None"
                interactive_message = "None"
                interactive_message_description = "None"

                phone_no_from =  bodyy['entry'][0]['changes'][0]['value']['messages'][0]['from']
                profile_name = bodyy['entry'][0]['changes'][0]['value']['contacts'][0]['profile']['name']
                message_data = bodyy.get('entry', [{}])[0].get('changes', [{}])[0].get('value', {}).get('messages', [{}])[0]
                text_data = message_data.get('text')
                if text_data:
                    message_from_user = text_data.get('body', "None")
                interactive_data = message_data.get('interactive')
                if interactive_data:
                    list_reply_data = interactive_data.get('list_reply')
                    if list_reply_data:
                        interactive_message = list_reply_data.get('title', "None")
                        interactive_message_description = list_reply_data.get("description","None")
                chunk_size = 1350
                contact, created = Contact.objects.get_or_create(
                    phone_number=phone_no_from,
                    defaults={'name': profile_name, 'channel': "via whatsapp chat"}
                )


                def intro(profile_name):
                    # messangerbot(f"🌼 Welcome to Mentalytics, {profile_name}! Your personal Wellness and Mental Health Bot Menta is here for you. 🤖\n💚 We specialize in holistic approaches to mental well-being, offering support, resources, and guidance for your journey. 🌿\nWhat’s on your mind today?",phone_no_from)
                    messangerbot(f"🌼 Welcome to Mentalytics, {profile_name}! Your personal Wellness and Mental Health Bot Menta is here for you. 🤖\n💚 We specialize in holistic approaches to mental well-being, offering support, resources, and guidance for your journey. 🌿\n",phone_no_from)

                def processing():
                    messangerbot("🌱 We're here to listen and support you. 💬 thinking ...  we'll work through it together.",phone_no_from)

                def thinker(message):
                    response_doctor=get_completion_from_messages(message)
                    response_doctor_splitted = split_string(response_doctor, chunk_size)
                    response=response_doctor_splitted[0]
                    return response

                def update_database_and_sheet(user_message, bot_response, response_message_segregation,
                                    phone_no_from, profile_name, message_count, currentstate):
                    Query = UserQuery.objects.create(
                        user_message=user_message,
                        bot_response=bot_response,
                        response_message_segregation=response_message_segregation,
                        phone_no_from=phone_no_from,
                        profile_name=profile_name,
                        message_count=message_count,
                        currentstate=currentstate
                    )
                    Query.save()
                    message_internal_id = Query.message_internal_id

                def updatefeedback(Question,interactive_message_description,phone_no_from):
                    feedback = Feedback.objects.create(
                        phone_no_from=phone_no_from,
                        question=Question,
                        feedback=interactive_message_description
                    )
                    feedback.save()

                def pipeline():
                    ques_feedback=[]
                    response_message_segregation = message_segregator(message_from_user)
                    existing_query = UserQuery.objects.filter(phone_no_from=phone_no_from).first()
                    if existing_query:
                        existing_query.message_count += 1
                        message_count = existing_query.message_count
                        existing_query.save()
                    else:
                        message_count=1
                        reply = ("🎉 Heyyya! "+profile_name+", 🌟 Welcome to our Platform! 🎊\n"
                                "👋 We're *THRILLED* you're here!\n"
                                "💡 Ready to explore something AMAZING? We've got a universe of cool stuff just waiting for you. 🌌\n"
                                "👇 So what are you waiting for? Dive in and let's make some magic happen! 🎩\n"
                                "👉 What's troubling you today?📝")
                        messangerbot(reply,phone_no_from)
                        ask_to_feedback_message(phone_no_from)
                        currentstate=-999
                        update_database_and_sheet(message_from_user, "FIRST MESSAGE",response_message_segregation,
                                                phone_no_from, profile_name, message_count, currentstate)
                    if UserQuery.objects.filter(phone_no_from=phone_no_from).order_by('-message_internal_id').first().currentstate:
                        currentstate=UserQuery.objects.filter(phone_no_from=phone_no_from).order_by('-message_internal_id').first().currentstate
                    else:
                        currentstate=-999
                    print(interactive_message_description)

                    if interactive_message_description=="Yes":
                        currentstate=1000
                        update_database_and_sheet(message_from_user, "None", "feedback_menu",
                                                phone_no_from, profile_name, message_count, currentstate)
                    if interactive_message_description=="No":
                        currentstate=1004
                        update_database_and_sheet(message_from_user, "None", "feedback_menu",
                                                phone_no_from, profile_name, message_count, currentstate)
                    if currentstate==1000:
                        send_feedback_message("Did the bot answer your query?",phone_no_from)
                        currentstate=1001
                        update_database_and_sheet(message_from_user, "None", "feedback_menu",
                                                phone_no_from, profile_name,  message_count, currentstate)
                    elif message_from_user.lower()=="exit" or currentstate==10:
                            messangerbot("Thanks for using our Bot!", phone_no_from    )
                            ask_to_feedback_message(phone_no_from)
                            currentstate=-999
                            update_database_and_sheet(message_from_user, "Thank you Message", response_message_segregation,
                                                    phone_no_from, profile_name, message_count,  currentstate)
                    elif currentstate==1001:
                        updatefeedback("Did the bot answer your query?",interactive_message_description,phone_no_from)
                        send_feedback_message("Were you comfortable with the answers provided?",phone_no_from)
                        currentstate=1002
                        update_database_and_sheet(message_from_user, "None", "feedback_menu",
                                                phone_no_from, profile_name, message_count, currentstate)
                    elif currentstate==1002:
                        updatefeedback("Were you comfortable with the answers provided?",interactive_message_description,phone_no_from)
                        send_feedback_message("Did you feel any difficulty while using the bot?",phone_no_from)
                        currentstate=1003
                        update_database_and_sheet(message_from_user, "None", "feedback_menu",
                                                phone_no_from, profile_name, message_count, currentstate)
                    elif currentstate==1003:
                        updatefeedback("Did you feel any difficulty while using the bot?",interactive_message_description,phone_no_from)
                        messangerbot("Thanks for giving us Feedback! ♥",phone_no_from)
                        currentstate=-999
                        update_database_and_sheet(message_from_user, "None", "feedback_menu",
                                                phone_no_from, profile_name, message_count, currentstate)

                    elif currentstate==1004:
                        messangerbot("Its Alright we appreciate your time using our bot!😊",phone_no_from)
                        currentstate=-999
                        update_database_and_sheet(message_from_user, "None", "feedback_menu",
                                                phone_no_from, profile_name, message_count, currentstate)
                    # elif response_message_segregation.lower() == "feedback":
                    #     messangerbot("Thanks for using our Bot!",phone_no_from)
                    #     ask_to_feedback_message(phone_no_from)

                    #     currentstate=-999
                    #     update_database_and_sheet(message_from_user, "None", response_message_segregation,
                    #                             phone_no_from, profile_name, message_count,currentstate)

                    elif (currentstate==-999 or currentstate==0):
                        intro(profile_name)
                        send_feedback_message("How is your mood now ? ",phone_no_from)
                        currentstate=1099
                        update_database_and_sheet(message_from_user, "None", response_message_segregation,
                                                phone_no_from, profile_name, message_count, currentstate)


                    elif currentstate==1099:
                        updatefeedback("How is your mood now ?",interactive_message_description,phone_no_from)
                        messangerbot("Cool! So Lets chat now, tell me whats going on your mind ?",phone_no_from)
                        currentstate=2
                        update_database_and_sheet(message_from_user, "None", "feedback_menu",
                                                phone_no_from, profile_name, message_count, currentstate)

                    elif currentstate==2:
                        message=UserQuery.objects.filter(phone_no_from=phone_no_from,currentstate=2).order_by('-message_internal_id').first().user_message
                        responsedoc="none"
                        if UserQuery.objects.filter(phone_no_from=phone_no_from,currentstate=2).order_by('-message_internal_id').first().bot_response:
                            responsedoc=UserQuery.objects.filter(phone_no_from=phone_no_from,currentstate=2).order_by('-message_internal_id').first().bot_response
                        if interactive_message=="None" or len(interactive_message_description)>12:

                            processing()
                            if message_from_user=="None":
                                message_bot=thinker(interactive_message_description)
                            else:
                                message_bot=thinker(message_from_user)
                            # messangerbot(message_bot,phone_no_from)
                            update_database_and_sheet(message_from_user,message_bot,  response_message_segregation,
                                                phone_no_from, profile_name, message_count, currentstate)
                            format="""{
                                "questions": [
                                    "How can I get out of this stress?",
                                    "What is the best way of dealing stress?",
                                    "Why is being positive important?",
                                    "Should I study harder?"
                            ]
                            }  """
                            prompt1 = f'''
                            generate similar 4 small questions(limit is of 20 char for each ques) based on these queries in list format give in a json type format {format}, give only the json no text above or below it
                            {message} and {message_from_user} and response {responsedoc} ... dont give the same question! give based on the use ques and chat
                            '''
                            model = genai.GenerativeModel("gemini-1.5-pro-latest")
                            openai_response = model.generate_content(
                                prompt1,
                                generation_config=genai.GenerationConfig(
                                    response_mime_type="application/json"
                                ),
                            )
                            openai_response=openai_response.text.strip()

                            response_query_choser2=(openai_response)
                            questions = json.loads(response_query_choser2[response_query_choser2.find("{"):response_query_choser2.rfind("}") + 1])["questions"]
                            question1, question2, question3, question4 = questions
                            messagebutton_together("Menta",message_bot, question1 , question2 , question3 , question4,phone_no_from)
                            update_database_and_sheet(message_from_user+interactive_message_description, message_bot , response_message_segregation,
                                                    phone_no_from, profile_name, message_count,  currentstate)


                pipeline()

        return HttpResponse(status=200)

    except json.JSONDecodeError:
        print("things aint working out")
        return HttpResponse(status=400)


@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
@csrf_exempt
def chat_view(request):
    user = request.user
    print(f"Authenticated user: {user.username}")
    query = request.data.get('query')  # Ensure you're getting the right key

    if not query:
        return Response({"error": "Query not provided."}, status=status.HTTP_400_BAD_REQUEST)

    past_chats = Chat.objects.filter(user_id=user.id).order_by('created_at')
    chat_history = "\n".join([f"User: {chat.query}\nAssistant: {chat.response}" for chat in past_chats])

    prompt = f"\n\n{chat_history}\nUser: {query}\nAssistant:"

    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        system_instruction="You are a mental health expert. Give advice in points format, in 40 words with no formatting such as bold. If someone greets with hey, hello, or hi, respond accordingly without giving advice. No formatting like **."
    )
    response = model.generate_content([ prompt])

    # Remove all "*" characters from the response
    gemini_response = response.text.replace('*', '').strip()

    # Save the chat response
    chat = Chat.objects.create(user_id=user.id, query=query, response=gemini_response)

    chat_serializer = ChatSerializer(chat)
    return Response(chat_serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
@csrf_exempt
def suggestive_question_view(request):
    # Get the authenticated user from the request
    user = request.user
    print(f"Authenticated user: {user.username}")

    # Retrieve past chats for the authenticated user
    past_chats = Chat.objects.filter(user_id=user.id).order_by('created_at')
    chat_history = "\n".join([f"User: {chat.query}\nAssistant: {chat.response}" for chat in past_chats])

    # Use a specific query to generate suggestive questions
    query = """give 4 suggestive questions to ask based on the chat history of the user in JSON format... {
    "questions": "[
        "Have you been feeling more stressed lately?",
        "Are you getting enough sleep?",
        "How has your diet been?",
        "Is there anything you're concerned about with your health?"
    ]"
} """

    prompt = f"\n\n{chat_history}\nUser: {query}\nAssistant:"

    # Interact with the Gemini model
    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        system_instruction="You are a mental health expert . Give adises in points format, dont give bullet points in 40 words with no formatting of bold etc."
    )

    response = model.generate_content([prompt], generation_config=genai.GenerationConfig(response_mime_type="application/json"))
    gemini_response = response.text.strip()

    try:
        gemini_response_json = json.loads(gemini_response)  # Parse the response to ensure it's valid JSON
    except json.JSONDecodeError:
        raise ParseError("The model did not return a valid JSON response.")

    return Response(gemini_response_json, status=status.HTTP_200_OK)

# Register a new user
@api_view(['POST'])
def register(request):
    username = request.data.get('user_id')
    password = request.data.get('password')
    name = request.data.get('name')

    if not username or not password:
        return Response({"error": "Please provide both username and password"}, status=status.HTTP_400_BAD_REQUEST)

    if User.objects.filter(username=username).exists():
        return Response({"error": "User already exists"}, status=status.HTTP_400_BAD_REQUEST)

    user = User.objects.create_user(username=username, password=password, first_name=name)
    return Response({"success": "User registered successfully"}, status=status.HTTP_201_CREATED)

# Login a user
@api_view(['POST'])
def login(request):
    username = request.data.get('user_id')
    password = request.data.get('password')

    user = authenticate(username=username, password=password)

    if user is not None:
        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)

        # Return the tokens in the response
        return Response({
            'refresh': str(refresh),
            'access': access_token,
            'user_name': user.first_name,
            'user_id': user.username,
            # "user_name": user.name
        }, status=status.HTTP_200_OK)
    else:
        return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['GET'])
def token_login(request):
    token_param = request.GET.get('token')
    if not token_param:
        return JsonResponse({'error': 'Token is missing'}, status=400)

    try:
        # Decode the token using Simple JWT
        access_token = AccessToken(token_param)
        user_id = access_token['user_id']

        # Get the user associated with the token
        user = User.objects.get(id=user_id)
        if user:
            # Log in the user
            login(request, user)
            return redirect('/')  # Redirect to the dashboard after login
        else:
            return JsonResponse({'error': 'User not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': 'Invalid token'}, status=400)

import urllib.parse

def generate_login_link(request, user_id):
    try:
        # Fetch the user based on the user_id from the URL
        user = User.objects.get(id=user_id)

        # Generate the access token for the user
        access_token = AccessToken.for_user(user)
        encoded_first_name = urllib.parse.quote(user.first_name)  # Use first_name
        encoded_username = urllib.parse.quote(user.username)

        # Create the login URL with the token
        login_url = f"http://localhost:3000/token-login/?token={str(access_token)}&name={encoded_first_name}&username={encoded_username}"

        # Return the login URL as a JSON response
        return JsonResponse({'login_url': login_url})

    except User.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)

aai.settings.api_key = ASSEMBLYAI_API_KEY

@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
@csrf_exempt
def upload_audio(request):
    # Check if an audio file is included in the request
    if 'audio' not in request.FILES:
        return Response({'error': 'No audio file provided.'}, status=status.HTTP_400_BAD_REQUEST)

    audio_file = request.FILES['audio']

    # Save the audio file temporarily
    audio_file_name = default_storage.save(f'temp/{audio_file.name}', audio_file)
    audio_file_path = default_storage.path(audio_file_name)

    # Convert audio to .wav if needed using pydub
    if audio_file.name.endswith('.webm'):
        audio = AudioSegment.from_file(audio_file_path, format="webm")
        wav_file_path = f"{audio_file_path}.wav"
        audio.export(wav_file_path, format="wav")
    else:
        wav_file_path = audio_file_path  # If already in wav format

    try:
        # Transcribe the audio using AssemblyAI
        transcriber = aai.Transcriber()
        transcript = transcriber.transcribe(wav_file_path)

        # Check for errors
        if transcript.status == aai.TranscriptStatus.error:
            return Response({'error': transcript.error}, status=status.HTTP_400_BAD_REQUEST)

        # Return the transcription
        return Response({'transcription': transcript.text}, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    finally:
        # Clean up: remove temp files
        if os.path.exists(wav_file_path):
            os.remove(wav_file_path)
        if os.path.exists(audio_file_path):
            os.remove(audio_file_path)


def custom_404(request, exception):
    return render(request, '404.html', {}, status=404)

def is_admin_user(user):
    return user.is_authenticated and user.is_staff

@user_passes_test(is_admin_user, login_url='/admin/')
def home(request):
    return render(request, 'home.html')

@user_passes_test(is_admin_user, login_url='/admin/')
def settings_1(request):
    return render(request, 'settings.html')

USERNAME = 'EvolvingPlanet'
TOKEN = 'b09fc7cf0bdc305e69ff5ba2f9458e4c4f9ec14f'
DOMAIN_NAME = 'evolvingplanet.pythonanywhere.com'
BASE_API_URL = f'https://www.pythonanywhere.com/api/v0/user/{USERNAME}/webapps/{DOMAIN_NAME}/'

@csrf_exempt
def call_api(action):
    """
    Function to call the PythonAnywhere API with a specific action.
    """
    url = f'{BASE_API_URL}{action}/'
    headers = {'Authorization': f'Token {TOKEN}'}
    response = requests.post(url, headers=headers)

    if response.status_code == 200:
        return True, "Action successful!"
    else:
        return False, response.text

@csrf_exempt
def shut_down_backend(request):
    """
    View to shut down the backend.
    """
    success, message = call_api('disable')
    return JsonResponse({'success': success, 'message': message})

@csrf_exempt
def re_enable_backend(request):
    """
    View to re-enable the backend.
    """
    success, message = call_api('enable')
    return JsonResponse({'success': success, 'message': message})

@csrf_exempt
def reload_backend(request):
    """
    View to reload the backend.
    """
    username = 'EvolvingPlanet'
    token = 'b09fc7cf0bdc305e69ff5ba2f9458e4c4f9ec14f'

    response = requests.post(
        'https://www.pythonanywhere.com/api/v0/user/{username}/webapps/{domain_name}/reload/'.format(
        # 'https://www.pythonanywhere.com/api/v0/user/{username}/always_on/'.format(

            username=username,
            domain_name='evolvingplanet.pythonanywhere.com'
        ),
        headers={'Authorization': 'Token {token}'.format(token=token)}
    )
    success, message = call_api('reload')
    return JsonResponse({'success': success, 'message': message})


def home_redirect(request):
    if request.user.is_authenticated:
        if request.user.is_staff:
            return redirect('home')
        else:
            messages.info(request, 'You must be an admin to view that page.')
            return redirect('admin:login')
    else:
        return redirect('admin:login')

@user_passes_test(is_admin_user, login_url='/admin/')
def chatindex(request):
    # Aggregate extra information: count of messages and latest timestamp per wa_id
    chat_info = (UserQuery.objects
                 .values('phone_no_from')
                 .annotate(last_message_time=Max('created_at'),
                           total_messages=Max('message_count'),
                           last_message=Max('bot_response', default='No messages'))  # Assuming 'answer' is the last message
                 .order_by('-last_message_time'))

    # If you want to include names and ensure uniqueness, consider how you'll handle multiple names per wa_id
    for chat in chat_info:
        chat['profile_name'] = UserQuery.objects.filter(phone_no_from=chat['phone_no_from']).first().profile_name

    return render(request, 'chatindex.html', {'chat_info': chat_info})

@user_passes_test(is_admin_user, login_url='/admin/')
def chat_view2(request, phone_number):
    messages = UserQuery.objects.filter(phone_no_from=phone_number).order_by('created_at')
    if messages.exists():  # Check if there are any messages
        user_name = messages.first().profile_name  # Get the name from the first message
    else:
        user_name = "Unknown"  # Default name if there are no messages
    return render(request, 'chat.html', {
        'messages': messages,
        'phone_number': phone_number,
        'user_name': user_name,
    })

# @user_passes_test(is_admin_user, login_url='/admin/')
def submit_text_message_chat(request):
    contacts = Contact.objects.all()
    success_message = None
    if request.method == 'POST':
        phone_number_select = request.POST.get('phoneNumberSelect', None)
        phone_number_manual = request.POST.get('phone_number', None)

        # Prioritize input box if not empty
        phone_number = phone_number_manual if phone_number_manual else phone_number_select
        message = request.POST.get('message')
        phonenum=str(phone_number)
        response = messenger.send_message(
                    message=(message),
                    recipient_id=phonenum,
            )
        success_message = f'Text message submitted successfully! to {phonenum} with {message} '

    return redirect('chat_view', phone_number=phone_number_manual)

@user_passes_test(is_admin_user, login_url='/admin/')
def upload_contacts(request):
    if request.method == 'POST':
        form = CSVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['file']
            decoded_file = csv_file.read().decode('utf-8').splitlines()
            reader = csv.DictReader(decoded_file)

            for row in reader:
                phone_number = "91" + str(row['PhoneNumber']).strip()

                # Check if wa_id matches the phone number in any Thread instance
                if Contact.objects.filter(phone_number=phone_number).exists():
                    messages.error(request, f'The phone number {phone_number} matches a wa_id in Threads and was not added.')
                    continue  # Skip this row and do not create a Contact

                # Attempt to create the Contact, catch IntegrityError if phone number is not unique
                try:
                    Contact.objects.create(
                        name=row['Name'],
                        phone_number=phone_number,
                        channel="via csv"
                    )
                except IntegrityError:
                    messages.error(request, f'Duplicate phone number {phone_number} not added.')
                    continue  # Skip this row

            messages.success(request, 'Contacts have been uploaded with validations.')
            return redirect('display_contacts')
    else:
        form = CSVUploadForm()

    return render(request, 'upload_contacts.html', {'form': form})

@user_passes_test(is_admin_user, login_url='/admin/')
def display_contacts(request):
    contacts = Contact.objects.all()
    return render(request, 'display_contacts.html', {'contacts': contacts})

def upload_csv_to_convertio(api_key, csv_file_path):
    url = 'https://api.convertio.co/convert'
    # csv_file_path = quote(csv_file_path, safe='')
    payload = {
        'apikey': api_key,
        'input': 'url',
        'file': csv_file_path,
        'outputformat': 'pdf'
    }
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, json=payload, headers=headers)
    response_json = response.json()

    if response.status_code == 200 and response_json['status'] == 'ok':
        return response_json['data']['id']
    else:
        print("Error uploading file:", response_json['error'])
        return None

def check_conversion_status(api_key, conversion_id):
    url = f'https://api.convertio.co/convert/{conversion_id}/status'
    payload = {
        'apikey': api_key
    }
    response = requests.get(url, params=payload)
    response_json = response.json()
    if response.status_code == 200 and response_json['status'] == 'ok':
        print("reached step 2")
        return response_json['data']['step'] == 'finish'
    else:
        print("Error checking conversion status:", response_json['error'])
        return False


def download_pdf(api_key, conversion_id, output_path):
    url = f'https://api.convertio.co/convert/{conversion_id}/dl'
    payload = {
        'apikey': api_key
    }
    response = requests.get(url, params=payload)
    response_json = response.json()

    if response.status_code == 200 and response_json['status'] == 'ok':
        pdf_content = response_json['data']['content']
        with open(output_path, 'wb') as pdf_file:
            pdf_file.write(pdf_content.encode('utf-8'))
        print("PDF file downloaded successfully.")
        return True
    else:
        print("Error downloading PDF:", response_json['error'])
        return False

def convertcsvtopdf(csv_file_path,company_name):
    api_key = 'cda4470b8ec7412545babcdde38d801a'
    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    output_path = f'{settings.MEDIA_ROOT}/{company_name}_{timestamp}.pdf'
    print("reached step 1")
    conversion_id = upload_csv_to_convertio(api_key, csv_file_path)

    if conversion_id:
        print("reached step 3")
        while True:
            if check_conversion_status(api_key, conversion_id):
                # Step 3: Download the PDF file if conversion is successful
                if download_pdf(api_key, conversion_id, output_path):
                    print("reached step 4")
                    break  # Exit the loop once the PDF is downloaded
            time.sleep(5)  # Wait for 1 second before checking again

def edit_product_message_prompt(request):
    instance, created = ProductMessagePrompt.objects.get_or_create(pk=1)
    form = ProductMessagePromptForm(request.POST or None, instance=instance)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return render(request, 'upload_success.html')

    return render(request, 'productmessage.html', {'form': form})

def some_view(request):
    product_message_prompt = ProductMessagePrompt.objects.first()
    if product_message_prompt:
        message = product_message_prompt.message
    else:
        message = "Default message if not set in the dashboard"

@user_passes_test(is_admin_user, login_url='/admin/')
def upload_audio2(request):
    print(request)
    print(request.FILES)
    if request.method == 'POST':
        form = AudioFileForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return render(request, 'upload_success.html', {'success_message':form.cleaned_data['audio'].name})
    else:
        form = AudioFileForm()
    return render(request, 'upload_audio.html',{ 'form': form})

@user_passes_test(is_admin_user, login_url='/admin/')
def productsadd(request):
    return render(request, 'productsadd.html')


def handle_uploaded_file(file_upload, company_name):
    file_path = f'{settings.MEDIA_ROOT}/{company_name}_{file_upload.name}'
    with open(file_path, 'wb+') as destination:
        for chunk in file_upload.chunks():
            destination.write(chunk)
    # file_path="https://.pythonanywhere.com/media/"+f"{company_name}_{file_upload.name}"
    return file_path


def submit_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            file_name = form.cleaned_data['file_name']
            # file_path="https://.pythonanywhere.com/medias/"+file_name+".csv"
            print(file_path)
            # api_key = ''
            timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
            output_path = f'{settings.MEDIA_ROOT}/{file_name}_{timestamp}.pdf'
            print("reached step 1")
            url = 'https://api.convertio.co/convert'
            # csv_file_path = quote(csv_file_path, safe='')
            payload = {
                'apikey': api_key,
                'input': 'url',
                'file': file_path,
                'outputformat': 'pdf'
            }
            headers = {'Content-Type': 'application/json'}
            response = requests.post(url, json=payload, headers=headers)
            response_json = response.json()

            if response.status_code == 200 and response_json['status'] == 'ok':
                conversion_id = response_json['data']['id']
            else:
                print("Error uploading file:", response_json['error'])


            if conversion_id:
                print("reached step 3")
                while True:
                    if check_conversion_status(api_key, conversion_id):
                        # Step 3: Download the PDF file if conversion is successful
                        if download_pdf(api_key, conversion_id, output_path):
                            print("reached step 4")
                            message = Product.objects.create( company_name=file_name, file_path=file_path)
                            message.save()
                            return redirect('productsadd')
                    time.sleep(5)  # Wait for 1 second before checking again
            # convertcsvtopdf(file_path, company_name)
 # Redirect to another page after successful form submission
    else:
        form = ProductForm()

    return render(request, 'productsadd.html', {'form': form})


@user_passes_test(is_admin_user, login_url='/admin/')
def dashboard(request):
    all_messages = UserQuery.objects.all()
    return render(request, 'dashboard.html', {'all_messages': all_messages})

@user_passes_test(is_admin_user, login_url='/admin/')
def broadcast(request):
    contacts = Contact.objects.all()
    return render(request, 'broadcast.html', {'contacts': contacts})

@user_passes_test(is_admin_user, login_url='/admin/')
def submit_text_message(request):
    contacts = Contact.objects.all()
    success_message = None
    if request.method == 'POST':
        phone_number_select = request.POST.get('phoneNumberSelect', None)
        phone_number_manual = request.POST.get('phoneNumberManual', None)

        # Prioritize input box if not empty
        phone_number = phone_number_manual if phone_number_manual else phone_number_select
        message = request.POST.get('message')
        phonenum=str(phone_number)
        response = messenger.send_message(
                    message=(message),
                    recipient_id=phonenum,
            )
        success_message = f'Text message submitted successfully! to {phonenum} with {message} '

    return render(request, 'broadcast.html', {'success_message': success_message, 'contacts': contacts})

@user_passes_test(is_admin_user, login_url='/admin/')
def submit_media_message(request):
    contacts = Contact.objects.all()
    success_message = None
    if request.method == 'POST':
        phone_number_select = request.POST.get('phoneNumberSelectMedia', None)
        phone_number_manual = request.POST.get('phoneNumberMedia', None)

        # Prioritize input box if not empty
        phone_number = phone_number_manual if phone_number_manual else phone_number_select
        phonenum=str(phone_number)
        attachment = request.POST.get('attachment')
        media_type = request.POST.get('mediaType')
        # media_message = request.POST.get('mediaMessage')
        # Process the form data and perform any necessary operations
        url = f'https://graph.facebook.com/v19.0/{PHONE_NUM_ID}/messages'
        # recipient_phone_number = '918128612391'
        # media_object_id="https://akshat1423.github.io/speechyz.aac"
        # media_object_id ="https://evolvingplanet.pythonanywhere.com/media/audios/"+answered_file_name_with_timestamp
        headers = {
            'Authorization': f'Bearer {WHATSAPP_TOKEN}',
            'Content-Type': 'application/json'
        }
        payload = {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": phonenum,
            "type": media_type,
            media_type: {
                "link": attachment
            }
        }
        json_payload = json.dumps(payload)
        response = requests.post(url, headers=headers, data=json_payload)

        # Assuming the submission was successful
        success_message = f'Media message submitted successfully! to {phonenum} link {attachment} of {media_type} with {response} '

    return render(request, 'broadcast.html', {'success_message': success_message,  'contacts': contacts})

@user_passes_test(is_admin_user, login_url='/admin/')
def submit_new_number_message(request):
    threads = Thread.objects.all()
    success_message = None
    if request.method == 'POST':
        phone_number = request.POST.get('phoneNumberNewNumber')
        template = request.POST.get('templateMessageId')
        messenger.send_template(template, phone_number, components=[], lang="en_US")
        success_message = f'Template submitted successfully! to {phone_number} template {template} '

    return render(request, 'broadcast.html', {'success_message': success_message, 'threads': threads})

@user_passes_test(is_admin_user, login_url='/admin/')
def queries_over_time(request):
    # Group UserQuery by date of creation
    datewise_queries = UserQuery.objects.dates('created_at', 'day')

    dates = []
    counts = []
    for date in datewise_queries:
        dates.append(date)
        counts.append(UserQuery.objects.filter(created_at__date=date).count())

    plt.plot(dates, counts)
    plt.xlabel('Date')
    plt.ylabel('Number of Queries')
    plt.title('Queries over Time')
    plt.grid(True)
    plt.tight_layout()

    response = HttpResponse(content_type="image/png")
    plt.savefig(response, format="png")
    return response

from pydub import AudioSegment
import assemblyai as aai
import google.generativeai as genai
import os
import requests


genai.configure(api_key=GOOGLE_API_KEY)
aai.settings.api_key = ASSEMBLYAI_API_KEY

def transcribe_audio(file_path):
    if not os.path.isfile(file_path):
        return {'error': 'Audio file not found'}

    base_name = os.path.splitext(file_path)[0]
    wav_file_path = f"{base_name}.ogg"

    try:
        if file_path.endswith('.webm'):
            audio = AudioSegment.from_file(file_path, format="webm")
            audio.export(wav_file_path, format="ogg")
        else:
            wav_file_path = file_path

        transcriber = aai.Transcriber()
        transcript = transcriber.transcribe(wav_file_path)

        if transcript.status == aai.TranscriptStatus.error:
            return {'error': transcript.error}

        return {'transcription': transcript.text}

    except Exception as e:
        return {'error': str(e)}

def generate_text_response(input_text):
    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        system_instruction="You are a mental health expert. Give advice in 30 words with no formatting of bold etc."
    )
    response = model.generate_content([input_text])
    return response.text.strip()


def process_audio_from_link(id,bodyy,phone_no_from): #download #transcribe #reply #texttospeech #
    name = bodyy["entry"][0]["changes"][0]["value"]["contacts"][0]["profile"]["name"]
    wa_id = bodyy["entry"][0]["changes"][0]["value"]["contacts"][0]["wa_id"]
    folder_path = "/home/AkshatGoogleHackathon/wearlytics_backend/media/audios/"
    files_in_folder = os.listdir(folder_path)

    # Loop through each file and remove it
    for file_name in files_in_folder:
        file_path = os.path.join(folder_path, file_name)
        try:
            os.remove(file_path)
            print(f"Deleted: {file_path}")
        except Exception as e:
            print(f"Error deleting {file_path}: {e}")
    url = f"https://graph.facebook.com/v18.0/{id}"
    payload = {}
    headers = {
        'Authorization': f'Bearer {WHATSAPP_TOKEN}'
    }
    response1 = requests.request("GET", url, headers=headers, data=payload)
    response_data = response1.json()
    audio_url = response_data["url"]
    response = requests.get(audio_url, headers=headers)
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    file_name_with_timestamp = f"{timestamp}.ogg"
    file_path = os.path.join(settings.MEDIA_ROOT, 'audios', file_name_with_timestamp)
    with open(file_path, 'wb') as f:
        f.write(response.content)
    transcription_result = transcribe_audio(file_path)
    if 'transcription' in transcription_result:
        response_text = generate_text_response(transcription_result['transcription'])

        format="""{
            "questions": [
                "How can blinking frequently help with eye strain?",
                "What is the 20-20-20 rule for reducing eye strain?",
                "Why is proper lighting essential to reduce eye strain?",
                "When should you consult an eye care professional for eye strain?"
        ]
        }  """
        prompt1 = f'''
        generate similar 4 small questions(limit is of 20 char for each ques) based on these queries in list format give in a json type format {format}, give only the json no text above or below it
        {transcription_result['transcription']}and response {response_text} ... dont give the same question! give based on the use ques and chat
        '''
        model = genai.GenerativeModel("gemini-1.5-pro-latest")
        openai_response = model.generate_content(
            prompt1,
            generation_config=genai.GenerationConfig(
                response_mime_type="application/json"
            ),
        )
        openai_response=openai_response.text.strip()

        response_query_choser2=(openai_response)
        questions = json.loads(response_query_choser2[response_query_choser2.find("{"):response_query_choser2.rfind("}") + 1])["questions"]
        question1, question2, question3, question4 = questions
        messagebutton_together("Menta",response_text, question1 , question2 , question3 , question4,phone_no_from)





