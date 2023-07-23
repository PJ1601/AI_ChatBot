from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.utils import timezone
from asgiref.sync import sync_to_async
from .models import Chat
from decouple import config
import openai
import asyncio


openai.api_key = config("API_KEY")

# openai request processing


async def handle_request(user_query):
    # Analyze user input and categorize the query
    query_category = await analyze_query(user_query)
    if query_category == "text_completion":
        # Use text-davinci-003 model for text completion
        completion_response = await complete_text(user_query, model="text-davinci-003")
        # Process and extract relevant information from completion_response
        # Return the processed response
        return format_text_completion_response(completion_response)

    elif query_category == "conversational_engagement":
        # Use gpt-4 model for conversational engagement
        conversation_response = await engage_in_conversation(user_query, model="gpt-4")
        # Process and extract relevant information from conversation_response
        # Return the processed response
        return format_conversational_response(conversation_response)

    else:
        completion_response = await complete_text_and_engage_in_conversation(user_query)
        # Handle unsupported query category or error
        return format_conversational_response(completion_response)


async def analyze_query(user_query):
    keywords_completion = ["complete", "suggest", "fill in"]
    keywords_conversation = ["chat", "talk", "engage"]

    # Check if query contains keywords related to text completion
    if any(keyword in user_query.lower() for keyword in keywords_completion):
        return "text_completion"

    # Check if query contains keywords related to conversational engagement
    if any(keyword in user_query.lower() for keyword in keywords_conversation):
        return "conversational_engagement"

    # If no specific category is identified, return a default category
    return "default"


async def complete_text(prompt, model):
    # Make API call to text-davinci-003 model endpoint
    completion_response = openai.Completion.create(
        engine=model, prompt=prompt, max_tokens=100, temperature=0
    )
    return completion_response


async def engage_in_conversation(query, model):
    # Make API call to gpt-4 model endpoint
    conversation_response = openai.Completion.create(
        engine=model,
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": query},
        ],
    )
    return conversation_response


async def complete_text_and_engage_in_conversation(query):
    completion_response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": query},
        ],
    )
    return completion_response


async def format_text_completion_response(response):
    # Process and format the response from text-davinci-003 model

    completed_text = response.choices[0].text.strip()

    return completed_text


async def format_conversational_response(response):
    # Process and format the response from gpt-4 model

    generated_message = response.choices[0].message.content.strip()

    return generated_message


# Create your views


async def chatbot(request):
    user = await sync_to_async(auth.get_user)(request)
    chats = await sync_to_async(Chat.objects.filter)(user=user)

    if request.method == "POST":
        message = request.POST.get("message")
        response = await handle_request(message)

        chat = Chat(
            user=user,
            message=message,
            response=response,
            created_at=timezone.now(),
        )
        await chat.asave()
        response = await response
        return JsonResponse({"message": message, "response": response})
    sync_chats = await sync_to_async(tuple)(chats)
    return render(
        request,
        "chatbot.html",
        {
            "chats": sync_chats,
            "is_authenticated": await sync_to_async(
                lambda: request.user.is_authenticated
            )(),
            "user": user,
        },
    )


def login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = auth.authenticate(request, username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect("chatbot")
        else:
            error_message = "Invalid Login Credentials"
            return render(request, "login.html", {"error_message": error_message})
    else:
        return render(request, "login.html")


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password1 = request.POST["password1"]
        password2 = request.POST["password2"]
        if password1 == password2:
            try:
                user = User.objects.create_user(username, email, password1)
                user.save()
                return redirect("chatbot")
            except:
                error_message = "Error while creating account. Please try again later."
                return render(
                    request, "register.html", {"error_message": error_message}
                )
        else:
            error_message = "Passwords don't match"
            return render(request, "register.html", {"error_message": error_message})
    return render(request, "register.html")


def logout(request):
    auth.logout(request)
    return redirect("login")
