from django.shortcuts import render, redirect
from django.conf import settings

from Auth.form import RegisterForm, LoginForm
import requests as sendRequest


def profile(request):
    if request.method == 'GET':
        if not request.session.get("username"):
            return redirect("login")

        name_of_user = ""

        try:
            url = settings.API_BASE_URL + "users"
            response = sendRequest.get(url, timeout=5)
            response.raise_for_status()
            users = response.json()

            for user in users:
                if user.get("email") == request.session["username"]:
                    name_of_user = user.get("name")
                    break

        except (sendRequest.exceptions.RequestException, ValueError):
            name_of_user = ""

        try:
            url = settings.API_BASE_URL + "posts/?limit=100&skip=0"
            response = sendRequest.get(url, timeout=5)
            response.raise_for_status()
            posts = response.json()
            user_post = [post for post in posts if post.get("user") == name_of_user]
        except (sendRequest.exceptions.RequestException, ValueError):
            user_post = []

        return render(request, 'profile.html', {'posts': user_post, 'user_name': name_of_user})


def signup(request):
    error = None
    success = False

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            data = {
                "name": form.cleaned_data['name'],
                "email": form.cleaned_data['email'],
                "phoneNo": form.cleaned_data['phone_Number'],
                "password": form.cleaned_data['password'],
                "confirm_password": form.cleaned_data['confirm_password'],
            }
            try:
                getResponse = sendRequest.post(settings.API_BASE_URL + "users", json=data, timeout=5)
                if getResponse.status_code == 201:
                    success = True
                    return redirect('Login')
                else:
                    error = getResponse.json().get('message', 'Registration failed.')
            except sendRequest.exceptions.RequestException:
                error = "Server unreachable. Try again later."
    else:
        form = RegisterForm()

    return render(request, 'signup.html', {
        'form': form,
        'error': error,
        'success': success,
    })


def login(request):
    form = LoginForm()
    error = None

    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            data = {
                "grant_type": "password",
                "username": form.cleaned_data["username"],
                "password": form.cleaned_data["password"],
            }
            try:
                url = settings.API_BASE_URL + "auth/login"
                getResponse = sendRequest.post(url, data=data, timeout=5)

                if getResponse.status_code == 200:
                    response_data = getResponse.json()
                    token = response_data.get("access_token")
                    token = {"Authorization": f"Bearer {token}"}

                    if token:
                        request.session["auth_token"] = token
                        request.session["username"] = data.get("username")
                        return redirect("Home")
                    else:
                        error = "Token not received from the server."
                else:
                    error = getResponse.json().get("detail", "Invalid credentials.")

            except sendRequest.exceptions.Timeout:
                error = "The request timed out. Please try again."
            except sendRequest.exceptions.RequestException:
                error = "Login service is unavailable."

    return render(request, "login.html", {"form": form, "error": error})


def logout(request):
    request.session.flush()
    return redirect("Home")
