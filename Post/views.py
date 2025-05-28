from django.shortcuts import render, redirect
from django.conf import settings

from Post.form import CreatePostForm, EditPostForm
import requests as sendRequest


def posts(request):
    url = settings.API_BASE_URL + "posts/?limit=10&skip=0"
    try:
        getResponse = sendRequest.get(url, timeout=5)
        getResponse.raise_for_status()
        posts = getResponse.json()
    except (sendRequest.exceptions.RequestException, ValueError) as e:
        posts = []

    return render(request, 'all_posts.html', {'posts': posts})


def post(request, id):
    url = settings.API_BASE_URL + f"posts/{id}"
    try:
        getResponse = sendRequest.get(url, timeout=5)
        getResponse.raise_for_status()
        post = getResponse.json()
    except (sendRequest.exceptions.RequestException, ValueError) as e:
        post = {}

    return render(request, 'get_post.html', {'post': post})


def createPost(request):
    error = None
    success = False

    if request.method == 'POST':
        form = CreatePostForm(request.POST)
        if form.is_valid():
            data = {
                "title": form.cleaned_data['title'],
                "content": form.cleaned_data['content'],
                "published": bool(form.cleaned_data['published']),
            }
            headers = request.session.get('auth_token')
            try:
                get_response = sendRequest.post(settings.API_BASE_URL + "posts", json=data, headers=headers, timeout=5)
                if get_response.status_code == 201:
                    return redirect('Profile')
                else:
                    error = get_response.json().get('message', 'Post Creation failed.')
            except sendRequest.exceptions.RequestException:
                error = "Server unreachable. Try again later."
    else:
        form = CreatePostForm()

    return render(request, 'create_post.html', {
        'form': form,
        'error': error,
        'success': success,
    })


def updatePost(request, id):
    error = None
    success = False

    if request.method == "POST":
        form = EditPostForm(request.POST)
        if form.is_valid():
            data = {
                'title': form.cleaned_data['title'],
                'content': form.cleaned_data['content'],
            }
            headers = request.session.get('auth_token')
            try:
                url = settings.API_BASE_URL + f"posts/{id}"
                get_response = sendRequest.put(url, headers=headers, json=data, timeout=5)
                if get_response.status_code == 200:
                    return redirect('Profile')
                else:
                    error = get_response.json().get('message', 'Post update failed.')
            except sendRequest.exceptions.RequestException:
                error = "Server unreachable. Try again later."
    else:
        url = settings.API_BASE_URL + f"posts/{id}"
        try:
            getResponse = sendRequest.get(url, timeout=5)
            getResponse.raise_for_status()
            post = getResponse.json()
        except (sendRequest.exceptions.RequestException, ValueError) as e:
            post = {}
        form = EditPostForm(initial={
            'title': post.get('title'),
            'content': post.get('content')
        })
    return render(request, 'edit_post.html', {'form': form, 'error': error, 'success': success})


def deletePost(request, id):
    if request.method == 'POST':
        url = settings.API_BASE_URL + f"posts/{id}"
        header = request.session.get('auth_token')
        try:
            getResponse = sendRequest.delete(url, headers=header, timeout=5)
            getResponse.raise_for_status()
        except (sendRequest.exceptions.RequestException, ValueError) as e:
            print(e)

        return redirect("Profile")

    return redirect("Profile")
