from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib import messages

import requests as send_request
from Support.form import ContactForm

API_LINK = settings.EMAIL_SEND_APP_LINK


def contact(request):
    form = ContactForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        content = (
            f" User Name: {form.cleaned_data['name']}\n"
            f" User Email: {form.cleaned_data['email']}\n\n"
            f" User Problem: {form.cleaned_data['description']}"
        )
        data = {
            "title": form.cleaned_data['reason'],
            "content": content,
            "sendTo": settings.SYSTEM_MAIL,
        }
        headers = {"token": settings.MAIL_TOKEN}

        try:
            response = send_request.post(API_LINK, json=data, headers=headers, timeout=15)
            if response.status_code in [200, 201, 202]:
                messages.success(request, "Thanks for contacting us.")
                form = ContactForm()
                redirect("Contact")
            else:
                message = "Failed to submit. Please try again."
                return render(request, 'error.html', {'message': message})
        except send_request.exceptions.RequestException:
            message = "Server unreachable. Try again later."
            return render(request, 'error.html', {'message': message})

    return render(request, 'contactUs.html', {'form': form})

