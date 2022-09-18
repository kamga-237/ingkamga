from django.shortcuts import render, redirect, HttpResponse
from  django.contrib.auth import authenticate, login, logout #fonction implémenter par django pour favciliter lauthentification
from django.shortcuts import get_object_or_404
from django.contrib import messages #fonction implémenter par django pour afficher un message derreur
from .forms import *  # la fonction loginForm importé depuis forms.py permet de crerr le formulaire
import time


def myhouse(request):
    if request.user.is_authenticated:  # si l'utilisateur est deja authentifié,
        return redirect('camer_house:liste_category_un')  # on le renvoi vers la page d'acceuil
    if request.method == "POST":  # si la methode utiliser par le formulaire est post
        form = LoginForm(request.POST)  # on recupere les donné du formulaire depuis la class loginform de  forms.py
        if form.is_valid():  # si les donnée sont valide
            username = form.cleaned_data['username']  # on recupère le nom
            pwd = form.cleaned_data['password1']  # on recupère le password
            user = authenticate(username=username, password=pwd)  # on envoi les données reçus à la methode authenticate importé depuis django.contrib.auth (elle prend en paramettre un username et un password)
            if user is not None:  # si le user exite, on le renvoi à sa page d'aceuil
                    login(request, user)  # apres connexion, la fonction login joue le role de SESSION
                    return redirect('myhouse')  # page dacceuil du client connecter
            else:  # si non
                messages.error(request, "Authentification échouée")  # on affiche un message derreur
                return render(request, 'authentification/login.html', {'form': form})  # on reste sur la page login
        else:
            for field in form.errors:
                form[field].field.widget.attrs[
                    'class'] += ' is-invalid'  # puis on rend les input rouge pour signaler lerreur
            return render(request, 'authentification/login.html', {'form': form})  # si les donner ne sont pas entrer, on reste sur la page
    else:
        form = LoginForm()
        return render(request, 'myhouse.html', {'form': form})  # on reste sur la page



def login_site(request):
    if request.user.is_authenticated: # si l'utilisateur est deja authentifié,
        return redirect('camer_house:liste_category_un') # on le renvoi vers la page d'acceuil
    if request.method == "POST": # si la methode utiliser par le formulaire est post
       form = LoginForm(request.POST) # on recupere les donné du formulaire depuis la class loginform de  forms.py
       if form.is_valid(): # si les donnée sont valide
           username =form.cleaned_data['username'] # on recupère le nom
           pwd = form.cleaned_data['password1'] # on recupère le password
           user = authenticate(username=username, password=pwd) #on envoi les données reçus à la methode authenticate importé depuis django.contrib.auth (elle prend en paramettre un username et un password)
           if user is not None: # si le user exite, on le renvoi à sa page d'aceuil
               login(request, user) #apres connexion, la fonction login joue le role de SESSION
               return redirect('myhouse') # page dacceuil du client connecter
           else: #si non
               messages.error(request,"Authentification échouée") #on affiche un message derreur

               return render(request, 'authentification/login.html', {'form':form}) #on reste sur la page login
       else:
           for field in form.errors:
               form[field].field.widget.attrs['class'] += ' is-invalid'  # puis on rend les input rouge pour signaler lerreur
           return render(request,'authentification/login.html', {'form':form})  #si les donner ne sont pas entrer, on reste sur la page
    else:

       form = LoginForm()
       return render(request,'authentification/login.html',{'form':form}) #on reste sur la page

def signin(request):
    codes ={
        'name': 'Algeria',
        'dial_code': '+213',
        'code': 'DZ'
    }, {
        'name': 'Benin',
        'dial_code': '+229',
        'code': 'BJ'
    }, {
        'name': 'Burkina Faso',
        'dial_code': '+226',
        'code': 'BF'
    }, {
        'name': 'Burundi',
        'dial_code': '+257',
        'code': 'BI'
    }, {
        'name': 'Cameroon',
        'dial_code': '+237',
        'code': 'CM'
    }, {
        'name': 'Canada',
        'dial_code': '+1',
        'code': 'CA'
    }, {
        'name': 'Cape Verde',
        'dial_code': '+238',
        'code': 'CV'
    }, {
        'name': 'Central African Republic',
        'dial_code': '+236',
        'code': 'CF'
    }, {
        'name': 'Chad',
        'dial_code': '+235',
        'code': 'TD'
    }, {
        'name': 'Congo (Rep.)',
        'dial_code': '+242',
        'code': 'CG'
    }, {
        'name': 'Congo (Dem. Rep.)',
        'dial_code': '+243',
        'code': 'CD'
    }, {
        'name': 'Cote d`Ivoire',
        'dial_code': '+225',
        'code': 'CI'
    }, {
        'name': 'Equatorial Guinea',
        'dial_code': '+240',
        'code': 'GQ'
    }, {
        'name': 'Gabon',
        'dial_code': '+241',
        'code': 'GA'
    }, {
        'name': 'Gambia',
        'dial_code': '+220',
        'code': 'GM'
    }, {
        'name': 'Ghana',
        'dial_code': '+233',
        'code': 'GH'
    }, {
        'name': 'Guinea',
        'dial_code': '+224',
        'code': 'GN'
    }, {
        'name': 'Guinea-Bissau',
        'dial_code': '+245',
        'code': 'GW'
    }, {
        'name': 'Kenya',
        'dial_code': '+254',
        'code': 'KE'
    }, {
        'name': 'Liberia',
        'dial_code': '+231',
        'code': 'LR'
    }, {
        'name': 'Libya',
        'dial_code': '+218',
        'code': 'LY'
    }, {
        'name': 'Madagascar',
        'dial_code': '+261',
        'code': 'MG'
    }, {
        'name': 'Morocco',
        'dial_code': '+212',
        'code': 'MA'
    }, {
        'name': 'Mozambique',
        'dial_code': '+258',
        'code': 'MZ'
    }, {
        'name': 'Niger',
        'dial_code': '+227',
        'code': 'NE'
    }, {
        'name': 'Nigeria',
        'dial_code': '+234',
        'code': 'NG'
    }, {
        'name': 'Senegal',
        'dial_code': '+221',
        'code': 'SN'
    }, {
        'name': 'Somalia',
        'dial_code': '+252',
        'code': 'SO'
    }, {
        'name': 'South Africa',
        'dial_code': '+27',
        'code': 'ZA'
    }, {
        'name': 'Sudan',
        'dial_code': '+249',
        'code': 'SD'
    }, {
        'name': 'Togo',
        'dial_code': '+228',
        'code': 'TG'
    }, {
        'name': 'Tunisia',
        'dial_code': '+216',
        'code': 'TN'
    }, {
        'name': 'Uganda',
        'dial_code': '+256',
        'code': 'UG'
    }, {
        'name': 'Zambia',
        'dial_code': '+260',
        'code': 'ZM'
    }, {
        'name': 'Zimbabwe',
        'dial_code': '+263',
        'code': 'ZW'
    }

    d = time.time()
    if request.user.is_authenticated:
        return redirect('myhouse') #si l'utilisateur est déja connecté on le renvoi vers sa page d'acceuil
    if request.method == "POST":
        form = UserForm(request.POST)
        profile = ProfileForm(request.POST)
        compte = CompteUser(request.POST)



        if form.is_valid() and profile.is_valid() and compte.is_valid():
            username = form.cleaned_data['username']
            pwd = form.cleaned_data['password1']
            email = form.cleaned_data['email']
#            user = User.objects.create_user(username=username, password=pwd, email=email)
          #  user.user_permissions.add(41, 42, 43, 44)  # voici comment on atribut les permition à un user

            if 1 == 1:
                profile = profile.save(commit=False)
                profile.day = d
                profile.pay = request.POST['pays']
                if profile.pay == "Algeria":
                    profile.code = "+213"

                if profile.pay == "Benin":
                    profile.code = "+229"

                if profile.pay == "Burkina Faso":
                    profile.code = "+226"

                if profile.pay == "Burundi":
                    profile.code = "+257"

                if profile.pay == "Cameroon":
                    profile.code = "+237"

                if profile.pay == "Canada":
                    profile.code = "+1"

                if profile.pay == "Cape Verde":
                    profile.code = "+238"

                if profile.pay == "Central African Republic":
                    profile.code = "+236"

                if profile.pay == "Chad":
                    profile.code = "+235"

                if profile.pay == "Congo  (Rep)":
                    profile.code = "+242"

                if profile.pay == "Congo  (Dem. Rep.)":
                    profile.code = "+243"

                if profile.pay == "Cote d`Ivoire":
                    profile.code = "+225"

                if profile.pay == "Equatorial Guinea":
                    profile.code = "+240"

                if profile.pay == "Gabon":
                    profile.code = "+241"

                if profile.pay == "Gambia":
                    profile.code = "+220"

                if profile.pay == "Ghana":
                    profile.code = "+233"

                if profile.pay == "Guinea":
                    profile.code = "+224"

                if profile.pay == "Guinea-Bissau":
                    profile.code = "+245"

                if profile.pay == "Kenya":
                    profile.code = "+254"

                if profile.pay == "Liberia":
                    profile.code = "+231"

                if profile.pay == "Libya":
                    profile.code = "+218"

                if profile.pay == "Madagascar":
                    profile.code = "+261"

                if profile.pay == "Morocco":
                    profile.code = "+212"

                if profile.pay == "Mozambique":
                    profile.code = "+258"

                if profile.pay == "Niger":
                    profile.code = "+227"

                if profile.pay == "Nigeria":
                    profile.code = "+234"

                if profile.pay == "Senegal":
                    profile.code = "+221"

                if profile.pay == "Somalia":
                    profile.code = "+252"

                if profile.pay == "South Africa":
                    profile.code = "+27"

                if profile.pay == "Sudan":
                    profile.code = "+249"

                if profile.pay == "Togo":
                    profile.code = "+228"

                if profile.pay == "Tunisia":
                    profile.code = "+216"

                if profile.pay == "Uganda":
                    profile.code = "+256"

                if profile.pay == "Zambia":
                    profile.code = "+260"

                if profile.pay == "Zimbabwe":
                    profile.code = "+263"

                dd = Profile.objects.filter(phonenumber= profile.phonenumber, code= profile.code)
                if dd:
                    messages.error(request, 'se numéro existe déja')
                    form = UserForm()
                    profile = ProfileForm()
                    compte = CompteUser()
                    return render(request, 'authentification/signin.html',
                                  {'form': form, 'profile': profile, 'codes': codes})

                compte = compte.save(commit=False)
                compte.montant = 000000.00
                compte.day = d
                user = User.objects.create_user(username=username, password=pwd, email=email)
                profile.user = user
                profile.save()
                compte.user=user
                compte.save()
                login(request, user)
                return redirect('camer_house:liste_category_un')
            else:
                messages.error(request,'creation de compte échoué' )

                return render(request,'authentification/signin.html', {'form':form, 'profile':profile, 'codes': codes})
        else:
            for field in form.errors:
                form[field].field.widget.attrs['class'] += ' is-invalid'
            for field in profile.errors:
                profile[field].field.widget.attrs['class'] += ' is-invalid'
            return render(request,'authentification/signin.html', {'form':form, 'profile':profile, 'codes': codes})
    else:
        form = UserForm()
        profile = ProfileForm()
        compte = CompteUser()
        return render(request, 'authentification/signin.html', {'form':form, 'profile':profile, 'codes': codes, 'compte': compte})

def logout_site(request):

    if request.method == "POST": # si la methode utiliser par le formulaire est post
       form = LoginForm(request.POST) # on recupere les donné du formulaire depuis la class loginform de  forms.py
       if form.is_valid(): # si les donnée sont valide
           username =form.cleaned_data['username'] # on recupère le nom
           pwd = form.cleaned_data['password1'] # on recupère le password
           user = authenticate(username=username, password=pwd) #on envoi les données reçus à la methode authenticate importé depuis django.contrib.auth (elle prend en paramettre un username et un password)
           if user is not None: # si le user exite, on le renvoi à sa page d'aceuil
               login(request, user) #apres connexion, la fonction login joue le role de SESSION
               return redirect('myhouse') # page dacceuil du client connecter
           else: #si non
               messages.error(request,"Authentification échouée") #on affiche un message derreur

               return render(request, 'authentification/login.html', {'form':form}) #on reste sur la page login
       else:
           for field in form.errors:
               form[field].field.widget.attrs['class'] += ' is-invalid'  # puis on rend les input rouge pour signaler lerreur
           return render(request,'authentification/login.html', {'form':form})  #si les donner ne sont pas entrer, on reste sur la page

    else:
        logout(request)
        form = LoginForm()
        return render(request,'authentification/login.html', {'form':form})