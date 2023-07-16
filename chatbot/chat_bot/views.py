from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.utils import timezone
from .models import Chat
from decouple import config
import openai


openai.api_key = config("API_KEY")


# Create your views here.
def ask_openai(message):
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=message,
        max_tokens=100,
        temperature=0,
    )
    answer = response.choices[0].text.strip()  # type: ignore
    return answer


def chatbot(request):
    chats = Chat.objects.filter(user=request.user)

    if request.method == "POST":
        message = request.POST.get("message")
        response = ask_openai(message)

        chat = Chat(
            user=request.user,
            message=message,
            response=response,
            created_at=timezone.now(),
        )
        chat.save()
        return JsonResponse({"message": message, "response": response})
    return render(request, "chatbot.html", {"chats": chats})


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
        error_message = "Invalid Username or Password"
        return render(request, "login.html", {"error_message": error_message})


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
