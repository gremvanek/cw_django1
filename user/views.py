from django.shortcuts import render, redirect

from .forms import UserForm
from .models import User


def user_list(request):
    users = User.objects.all()
    return render(request, 'user/u_list.html', {'users': users})


def user_detail(request, pk):
    user = User.objects.get(pk=pk)
    return render(request, 'user/u_detail.html', {'user': user})


def user_create(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('u_list')
    else:
        form = UserForm()
    return render(request, 'user/u_form.html', {'form': form})


def user_update(request, pk):
    user = User.objects.get(pk=pk)
    if request.method == 'POST':
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('u_list')
    else:
        form = UserForm(instance=user)
    return render(request, 'user/u_form.html', {'form': form})


def user_delete(request, pk):
    user = User.objects.get(pk=pk)
    user.delete()
    return redirect('u_list')
