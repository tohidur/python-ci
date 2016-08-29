from django.contrib.auth import (
    authenticate,
    get_user_model,
    login,
    logout,
)
from django.shortcuts import render, redirect
from .forms import UserLoginForm, UserRegistrationForm
from collection.models import Collection
from collection.forms import CollectionForm
from django.http import HttpResponse


def login_view(request):
    next_request = request.GET.get('next')
    form_board = CollectionForm(None)
    form = UserLoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        login(request, user)
        if next_request:
            return redirect(next_request)
        collection = Collection.objects.filter(user=request.user)
        if not collection:
            return render(request, 'create_board.html', {'form': form_board})
        link = collection.first().slug
        return redirect("/"+link+'/')
    if request.user.is_authenticated():
        collection = Collection.objects.filter(user=request.user)
        if not collection:
            return render(request, 'create_board.html', {'form': form_board})
        return redirect('/'+collection.first().slug+'/')
    return render(request, 'login.html', {'form': form})


def register_view(request):
    next_request = request.GET.get('next')
    form_board = CollectionForm(None)
    form = UserRegistrationForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user.set_password(password)
        user.email = username
        user.save()
        new_user = authenticate(username=username, password=password)
        login(request, new_user)
        if next_request:
            return redirect(next_request)
        return render(request, 'create_board.html', {'form': form_board})

    if request.user.is_authenticated():
        collection = Collection.objects.filter(user=request.user)
        if not collection:
            return render(request, 'create_board.html', {'form': form_board})
        return redirect('/'+collection.first().slug+'/')

    context = {
        'form': form,
    }

    return render(request, 'signup.html', context)


def logout_view(request):
    logout(request)
    return render(request, 'home.html', {})
    # return redirect('/')
