from django.shortcuts import render, redirect
from django.conf import settings

from socket import create_connection
from time import sleep
import requests as send_request


def like(request, id):
    if request.method == "POST":
        try:
            like_order = int(request.POST.get('like_value', 1))
        except (TypeError, ValueError):
            like_order = 1

        url = settings.API_BASE_URL + "likes"
        headers = request.session.get('auth_token')
        data = {
            'post_id': id,
            'order': like_order
        }
        try:
            get_response = send_request.put(url, json=data, headers=headers, timeout=5)
            if get_response.status_code == 400:
                data['order'] = 0
                send_request.put(url, json=data, headers=headers, timeout=5)
        except send_request.RequestException as e:
            return render(request, 'error.html', {'message': e})

        return redirect("Post", id=id)


def check_internet():
    try:
        create_connection(("8.8.8.8", 53), timeout=3)
        return True
    except OSError:
        return False


def root(request):
    api_up = False
    internet_down = not check_internet()

    if not internet_down:
        for i in range(5):
            try:
                get_response = send_request.get(settings.API_BASE_URL, timeout=5)
                response = send_request.get(settings.API_TEST, timeout=5)
                if get_response.status_code == 200 and response.status_code == 200:
                    api_up = True
                    break
                sleep(5)
            except Exception as e:
                print("API Error: ", e)
                sleep(5)

    if not api_up:
        if internet_down:
            message = "No internet connection. Please check your network and try again."
        else:
            message = "API is currently down. Please try again later."
        return render(request, 'error.html', {'message': message})

    return render(request, 'home.html')
