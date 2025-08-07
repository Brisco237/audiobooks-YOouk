from django.shortcuts import render,redirect
from django.contrib.auth import logout, authenticate, login
from .models import User
from django.contrib import messages
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

# Create your views here.
def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f'Bienvenue {user.username} Vous etes connectez !')
            return redirect('home')
        else:
            messages.error(request, 'Mot de passe ou nom d\'utilisateur incorrect !')
            return redirect('login_user')
    if 'next' in request.GET:
        messages.error(request, "Désolé, pour lire les PDF vous devez être connecté sur le site.")
    return render(request, 'authapp/login.html')

def register_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        if User.objects.filter(username=username):
            messages.error(request,"Ce username est deja utilisé !")
            return redirect('register_user')
        if not username.isalpha():
            messages.error(request, "Désolé, mais le username doit etre en lettre uniquement !")
            return redirect('register_user') 
        if User.objects.filter(email=email):
            messages.error(request,"Cet adresse email est deja utilisé !")
            return redirect('register_user') 
            
        try: 
            validate_password(password)
        except ValidationError as errors:
            messages.error(request, f'{errors}')
            return render(request, 'authapp/register.html',{'errors':errors})

        # Création de l'utilisateur seulement si toutes les validations sont passées
        user = User.objects.create_user(username, email, password)
        user.save()
        messages.success(request, 'Utilisateur crée avec success !')
        return redirect('login_user')
    return render(request, 'authapp/register.html')

def logout_user(request):
    logout(request)
    messages.success(request, 'Vous etes bien déconnecté !')
    return redirect('login_user')