from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages



def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('users:login')  # Replace 'login' with the URL name where you want to redirect after registration
    else:
        form = UserCreationForm()

    return render(request, 'registration/register.html', {'form': form})