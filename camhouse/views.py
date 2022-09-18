
from django.shortcuts import render, redirect, get_object_or_404 #404 pour gerer les donnees entrante qi n'existe pas
from rest_framework.views import APIView
from django.http import HttpResponse, JsonResponse
from services.cdb import mycdb
from .models import *
from .forms import *
from django.db.models import Q
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.core.exceptions import PermissionDenied #pour gerer les pages non utilise( les permition)
from django.db import connection # connection est use pr ecrire les requetes sql
from rest_framework import viewsets
from rest_framework.decorators import api_view
from .serializers import *
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.views.decorators.csrf import csrf_exempt
import time

d = time.time()
lien0 = " "
c=1
def dupliquer_cam(request, id):
    test = get_object_or_404(House, pk = id) #gere les erreurs 404
    d = time.time()
    has_perm = False
    if not request.user.is_authenticated:
        return redirect('login')
    if not request.user.has_perm("camhouse.add_house") and not request.user.has_perm("camhouse.delete_house") and not request.user.has_perm("camhouse.view_house") and not request.user.has_perm("camhouse.change_house"): #pour savoir s'il est autoriser a ajouter une house
        raise PermissionDenied #on renvoi ver la page 403
    else:
        has_perm = True
    #on duplique dabord la Maison
    maison = House.objects.filter(id=id) # je recupere la maison
    if maison:
        for ids in maison:
            id = ids.id  # je recupère l'id de la maison à enregistrer par cet utilisateur
            region = ids.region
            pay = ids.pay
            arrondissement = ids.arrondissement
            nbchambre  =ids.nbchambre
            nbsalon = ids.nbsalon
            nbcuisine = ids.nbcuisine
            nbdouche = ids.nbdouche
            description = ids.description
            image = ids.image
            sommes = ids.sommes
            nbinfrastructure = ids.nbinfrastructure
            category_id = ids.category_id
            cat = ids.category
            type_id = ids.type_id
            user_id = ids.user.id
            nom = ids.nom
            etat = 1
            lat = ids.lat
            lng =ids.lng
            date = d
        if request.user.id == user_id: #si c'est la maison du user actuel
            house = House(user_id=user_id, lat=lat, lng=lng, date=d, pay=pay, category_id=category_id, type_id=type_id, region=region, arrondissement=arrondissement, nbchambre=nbchambre, nbcuisine=nbcuisine, nbsalon=nbsalon, nbdouche=nbdouche, description=description, image=image, sommes=sommes, etat=etat, nom=nom, nbinfrastructure=nbinfrastructure)
            house.save()

            #ensuite on duplique ses compositions
            id_all = House.objects.filter(user=request.user)
            for dernier_id in id_all:
                d_id = dernier_id.id  # je recupère l'id de la derniere maison enregistrer par cet utilisateur
            compositions = Composition.objects.filter(house_id=id)
            for composition in compositions:
                Composition(house_id=d_id, image=composition.image, imageUn=composition.imageUn, imageDeux=composition.imageDeux, insigne_id=composition.insigne_id, longeur=composition.longeur, largeur=composition.largeur, hauteur=composition.hauteur, statut=composition.statut, numbre=composition.numbre, description=composition.description, type_id=composition.type_id).save()

            #maintenant on duplique ses infrastructure
            infrastructures = Infrastructure.objects.filter(house_id=id)
            for infrastructure in infrastructures:
                Infrastructure(house_id=d_id, image=infrastructure.image, imageUn=infrastructure.imageUn, imageDeux=infrastructure.imageDeux, description=infrastructure.description).save()
            messages.success(request, f"dupplication réussi. votre {cat} à ete creer")
            r = 1

        else:
            raise PermissionDenied #on renvoi la page 403

    else:
        raise PermissionDenied #on renvoi la page 403
    return redirect('camer_house:proprieter_ch')

def supprimer_cam(request, id):
    test = get_object_or_404(House, pk = id) #gere les erreurs 404
    has_perm = False
    if not request.user.is_authenticated:
        return redirect('login')
    if not request.user.has_perm("camhouse.add_house") and not request.user.has_perm(
            "camhouse.delete_house") and not request.user.has_perm("camhouse.view_house") and not request.user.has_perm(
            "camhouse.change_house"):  # pour savoir s'il est autoriser a ajouter une house
        raise PermissionDenied  # on renvoi ver la page 403
    else:
        has_perm = True
    # on supprime dabord la Maison
        maison = House.objects.filter(id=id)  # je recupere la maison
    if maison:
        for ids in maison:
            id = ids.id  # je recupère l'id de la maison à enregistrer par cet utilisateur
            user_id = ids.user.id
        if request.user.id == user_id:  # si c'est la maison du user actuel

            # on supprime ses compositions
            id_all = House.objects.filter(user=request.user)
            for dernier_id in id_all:
                d_id = dernier_id.id  # je recupère l'id de la derniere maison enregistrer par cet utilisateur
            compositions = Composition.objects.filter(house_id=id)
            for composition in compositions:
                composition.delete()

             #maintenant on suprime ses infrastructure
            infrastructures = Infrastructure.objects.filter(house_id=id)
            for infrastructure in infrastructures:
                infrastructure.delete()

            house = House.objects.get(id=id)
            house.delete()


        else:
            raise PermissionDenied #on renvoi la page 403
    else:
        raise PermissionDenied #on renvoi la page 403

    return redirect('camer_house:proprieter_ch')

def supprimer_Reserv_cam(request, id):
    test = get_object_or_404(House, pk = id) #gere les erreurs 404

    has_perm = False
    if not request.user.is_authenticated:
        return redirect('login')
    if not request.user.has_perm("camhouse.add_house") and not request.user.has_perm(
            "camhouse.delete_house") and not request.user.has_perm("camhouse.view_house") and not request.user.has_perm(
            "camhouse.change_house"):  # pour savoir s'il est autoriser a ajouter une house
        raise PermissionDenied  # on renvoi ver la page 403
    else:
        has_perm = True
    # on modifi dabord l'état de la Maison
        maison = House.objects.filter(id=id)  # je recupere la maison
    if maison:
        for ids in maison:
            id = ids.id  # je recupère l'id de la maison à supprimr par cet utilisateur
            user_id = ids.user_id
        test = Reservation.objects.filter(house_id=id)

        if request.user.id == user_id and test:  # si c'est la maison du user actuel
            maison.update(etat=1)
            reservation = Reservation.objects.get(house_id=id)
            reservation.delete()

        else:
            raise PermissionDenied #on renvoi la page 403
    else:
        raise PermissionDenied #on renvoi la page 403

    return redirect('camer_house:proprieter_ch')

def supprimer_Reserv_univ(request, id):
    test = get_object_or_404(ChambreUniv, pk = id) #gere les erreurs 404

    has_perm = False
    if not request.user.is_authenticated:
        return redirect('login')
    if not request.user.has_perm("camhouse.add_house") and not request.user.has_perm(
            "camhouse.delete_house") and not request.user.has_perm("camhouse.view_house") and not request.user.has_perm(
            "camhouse.change_house"):  # pour savoir s'il est autoriser a ajouter une house
        raise PermissionDenied  # on renvoi ver la page 403
    else:
        has_perm = True
    # on modifi dabord l'état de la Maison
        maison = ChambreUniv.objects.filter(id=id)  # je recupere la maison
    if maison:
        for ids in maison:
            id = ids.id  # je recupère l'id de la maison à supprimr par cet utilisateur
            user_id = ids.composition_id
        hous_id = Composition.objects.filter(id=user_id)
        for Houss_id in hous_id:
            idddh = Houss_id.house_id
        use = House.objects.filter(id=idddh)
        for me in use:
            usermoi = me.user_id
        test = ReservationUniv.objects.filter(chambre_id=id)

        if request.user.id == usermoi and test:  # si c'est la maison du user actuel
            maison.update(etat=1)
            reservation = ReservationUniv.objects.get(chambre_id=id)
            reservation.delete()

        else:
            raise PermissionDenied #on renvoi la page 403
    else:
        raise PermissionDenied #on renvoi la page 403

    return redirect('camer_house:proprieter_ch')

def confirmer_Reserv_cam(request, id):
    test = get_object_or_404(House, pk = id) #gere les erreurs 404

    has_perm = False
    d = time.time()
    if not request.user.is_authenticated:
        return redirect('login')
    if not request.user.has_perm("camhouse.add_house") and not request.user.has_perm(
            "camhouse.delete_house") and not request.user.has_perm("camhouse.view_house") and not request.user.has_perm(
            "camhouse.change_house"):  # pour savoir s'il est autoriser a ajouter une house
        raise PermissionDenied  # on renvoi ver la page 403
    else:
        has_perm = True
    # on modifi dabord l'état de la Maison
        maison = House.objects.filter(id=id)  # je recupere la maison
    if maison:
        for ids in maison:
            id = ids.id  # je recupère l'id de la maison à enregistrer par cet utilisateur
            user_id = ids.user_id
        if request.user.id == user_id:  # si c'est la maison du user actuel
            maison.update(etat=3)
            lolo = Reservation.objects.filter(house_id=id)
            for new in lolo:
                proprio = new.user_id
                user_id = new.proprietaire
                puol = new.house_id
            date = d
            test = Occupation.objects.filter(house_id=id)
            if test:
                raise PermissionDenied  # on renvoi la page 403
            else:
                form = Occupation(proprietaire=proprio, date=date, user_id=user_id, house_id=puol)
                form.save()
                reservation = Reservation.objects.get(house_id=id)
                reservation.delete()
                return redirect('camer_house:proprieter_ch')

        else:
            raise PermissionDenied #on renvoi la page 403
    else:
        raise PermissionDenied #on renvoi la page 403

    return redirect('camer_house:proprieter_ch')

def confirmer_Reserv_univ(request, id):
    test = get_object_or_404(ChambreUniv, pk = id) #gere les erreurs 404

    has_perm = False
    d = time.time()
    if not request.user.is_authenticated:
        return redirect('login')
    if not request.user.has_perm("camhouse.add_house") and not request.user.has_perm(
            "camhouse.delete_house") and not request.user.has_perm("camhouse.view_house") and not request.user.has_perm(
            "camhouse.change_house"):  # pour savoir s'il est autoriser a ajouter une house
        raise PermissionDenied  # on renvoi ver la page 403
    else:
        has_perm = True
    # on modifi dabord l'état de la Maison
        maisons = ChambreUniv.objects.filter(id=id)  # je recupere la maison
    if maisons:
        for univ in maisons:
            id = univ.id  # je recupère l'id de la maison à enregistrer par cet utilisateur
            user_id = univ.composition_id
        hous_id = Composition.objects.filter(id = user_id)
        for Houss_id in hous_id:
            idddh = Houss_id.house_id
        use = House.objects.filter(id = idddh)
        for me in use:
            usermoi = me.user_id
        if request.user.id == usermoi:  # si c'est la maison du user actuel
            maisons.update(etat=3)
            lolo = ReservationUniv.objects.filter(chambre_id=id)
            for new in lolo:
                proprio = new.user_id
                user_id = new.proprietaire
                puol = new.chambre_id
            date = d
            test = OccupationUniv.objects.filter(chambre_id=id)
            if test:
                raise PermissionDenied  # on renvoi la page 403
            else:
                form = OccupationUniv(proprietaire=proprio, date=date, user_id=user_id, chambre_id=puol)
                form.save()
                reservation = ReservationUniv.objects.get(chambre_id=id)
                reservation.delete()
                return redirect('camer_house:proprieter_ch')

        else:
            raise PermissionDenied #on renvoi la page 403
    else:
        raise PermissionDenied #on renvoi la page 403

    return redirect('camer_house:proprieter_ch')

def supprimer_com(request, id):
    test = get_object_or_404(Composition, pk = id) #gere les erreurs 404
    has_perm = False
    if not request.user.is_authenticated:
        return redirect('login')
    if not request.user.has_perm("camhouse.add_house") and not request.user.has_perm(
            "camhouse.delete_house") and not request.user.has_perm("camhouse.view_house") and not request.user.has_perm(
            "camhouse.change_house"):  # pour savoir s'il est autoriser a ajouter une house
        raise PermissionDenied  # on renvoi ver la page 403
    else:
        # on supprime dabord la Maison
        chambre = Composition.objects.filter(id = id)  # je recupere la chambre
        print(chambre)
        for ch in chambre:
            ids = ch.house_id
            print(ids)
        chambre.delete()
        House.objects.filter(id = ids).update(etat = 0)
    return redirect('camer_house:proprieter_ch')
#**

def globaltchat(request):

    has_perm = False
    category = Category.objects.order_by('id').all()
    if not request.user.is_authenticated:
        return redirect('login')

    if request.user.has_perm("camhouse.add_house") and request.user.has_perm("camhouse.delete_house") and request.user.has_perm("camhouse.view_house") and request.user.has_perm("camhouse.change_house"): #si l'utilisateur a la permition d'ajouter une house, on l'autorise
        has_perm = True

    ancien = Compte.objects.filter(user_id=request.user)
    for montants in ancien:
        montant = montants.montant

    context = {

        'has_perm': has_perm,
        'sategory': category,
        'montant': montant,
        'formCompte': CompteUser()
    }

    return render(request, 'globaltchat.html', context=context)

def home_ch(request):
    has_perm = False
    category = Category.objects.order_by('id').all()
    d = time.time()
    if not request.user.is_authenticated:
        return redirect('login')

    #je suprime la consultation si 2jour(48heures) sont passée
    consult = Consultation.objects.filter(user_id=request.user.id)
    reserve = Reservation.objects.filter(user_id=request.user.id, proprietaire=request.user.id)

    if consult.exists():
        for const in consult:
            dte = const.day
        valeur = (d - dte)/3600
        if valeur >= 48:
            consult.delete()
    # je suprime la reservation si 7jour(168heures) sont passée
    if reserve.exists():
        for const in reserve:
            dte = const.date
            idh  = const.house_id
        valeur = (d - dte)/3600
        if valeur >= 168:
            reserve.delete()
            House.objects.filter(id = idh).update(etat=1)



    if request.user.has_perm("camhouse.add_house") and request.user.has_perm("camhouse.delete_house") and request.user.has_perm("camhouse.view_house") and request.user.has_perm("camhouse.change_house"): #si l'utilisateur a la permition d'ajouter une house, on l'autorise
        has_perm = True
    if request.method == "POST":

        form = CompteUser(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.day = d
            form.user = request.user
            if form.montant > 0:
                ancien = Compte.objects.filter(user_id= request.user)
            else:
                ancien = Compte.objects.filter(user_id=request.user)
                for montants in ancien:
                    montant = montants.montant

                context = {
                    'has_perm': has_perm,
                    'sategory': category,
                    'montant': montant,
                    'formCompte': CompteUser()
                }
                return render(request, 'home_ch.html', context=context)

            for montants in ancien:
                montant = montants.montant
            form.montant += montant
            Compte.objects.filter(user_id=request.user).update(montant=form.montant)
            context = {
                'has_perm': has_perm,
                'sategory': category,
                'montant': form.montant,
                'formCompte': CompteUser()
            }
            return render(request,'home_ch.html', context=context)
    else:

        ancien = Compte.objects.filter(user_id=request.user)
        for montants in ancien:
            montant = montants.montant

        context = {

            'has_perm': has_perm,
            'sategory': category,
            'montant': montant,
            'formCompte': CompteUser()
        }
        return render(request, 'home_ch.html', context=context)


    ancien = Compte.objects.filter(user_id=request.user)
    for montants in ancien:
        montant = montants.montant

    context = {
        'has_perm': has_perm,
        'sategory': category,
        'montant': montant,
        'formCompte': CompteUser()
    }
    return render(request, 'home_ch.html', context=context)
#**
def proprieter(request):
    r = 0
    has_perm = False
    formCompte = CompteUser()
    formRestorer = RetorerPuol()
    lien0= "active"
    if not request.user.is_authenticated:
        return redirect('login')

    ancien = Compte.objects.filter(user_id=request.user)
    for montants in ancien:
        montant = montants.montant
        idC = montants.id


    if not request.user.has_perm("camhouse.add_house") and not request.user.has_perm("camhouse.delete_house") and not request.user.has_perm("camhouse.view_house") and not request.user.has_perm("camhouse.change_house"): #pour savoir s'il est autoriser a ajouter une house
        raise PermissionDenied #on renvoi ver la page 403
    else:
        has_perm = True
    if request.method == 'POST':
        if request.POST['montant'] =="":
            print("operation anulée")
        elif float(request.POST['montant']) <= 0:
            print("opération anulée")

        elif float(request.POST['montant']) > 0:
            montant = montant + float(request.POST['montant'])
            Compte.objects.filter(user_id=request.user).update(montant=montant)
            return redirect("camer_house:proprieter_ch")
        else:
            print("operation impossible")


        if request.POST['proprietaire'] == "" or request.POST['puol'] == "" or request.POST['montant'] == 0:
            print("restoration annulé")

        elif int(request.POST['proprietaire']) <= 0 or int(request.POST['puol']) <= 0 or request.POST['montant'] == 0:
            print("donné erone")

        elif int(request.POST['proprietaire']) > 0 and int(request.POST['puol']) > 0 and montant >= 1000:
            id = request.POST['puol']
            house = House.objects.filter(id=id)
            for use in house:
                donnee = use.user_id
                etat = use.etat
            if request.user.id == donnee and etat == 3:
                House.objects.filter(id=id).update(etat=1)
                reservation = Occupation.objects.get(house_id=id)
                reservation.delete()
                dos = montant - 1000
                Compte.objects.filter(id=idC).update(montant=dos)
                return redirect("camer_house:proprieter_ch")
            else:
                raise PermissionDenied  # on renvoi la page 403
        else:
            print(f"reservation impossible car {request.POST['proprietaire']} : {request.POST['puol']}")

        if(request.POST['id'] is not None):
            house = House.objects.filter(id= request.POST['id'])
            for h in house:
                id_cat = h.category
                id_cate = h.category_id
                id_us = h.user_id
                ch = h.nbchambre
                cu = h.nbcuisine
                sa = h.nbsalon
                do = h.nbdouche
                infra = h.nbinfrastructure

            if (id_us == request.user.id):
                if id_cate == 1 or id_cate == 4 or id_cate == 5 or id_cate == 6 or id_cate == 7:
                    if (int(request.POST['sommes']) >= 1000 and request.POST['description'] != ' ' and request.POST['region'] != ' ' and request.POST['arrondissement'] != ' ' and int(request.POST['nbchambre']) >= 0 and int(request.POST['nbsalon']) >= 0 and int(request.POST['nbcuisine']) >= 0 and int(request.POST['nbdouche']) >= 0 and int(request.POST['nbinfrastructure']) >= 0):
                        if int(request.POST['nbchambre']) < ch or int(request.POST['nbsalon']) < sa or int(request.POST['nbcuisine']) < cu or int(request.POST['nbdouche']) < do or int(request.POST['nbinfrastructure']) < infra:
                            messages.error(request, f" echec de modification . votre {id_cat} n'a pas ete Mise à jour. vérifier vos information. une ou plusieurs données sont inférieur à celle déja enregistrer")
                            r = 2
                        elif int(request.POST['nbchambre']) > ch or int(request.POST['nbsalon']) > sa or int(request.POST['nbcuisine']) > cu or int(request.POST['nbdouche']) > do or int(request.POST['nbinfrastructure']) > infra:
                            House.objects.filter(id=request.POST['id']).update(sommes=request.POST['sommes'],description=mycdb(request.POST['description']),region=mycdb(request.POST['region']),arrondissement=mycdb(
                                                                                       request.POST['arrondissement']),
                                                                                   nbchambre=request.POST['nbchambre'],
                                                                                   nbsalon=request.POST['nbsalon'],
                                                                                   nbcuisine=request.POST['nbcuisine'],
                                                                                   nbdouche=request.POST['nbdouche'],
                                                                                   nbinfrastructure=request.POST[
                                                                                       'nbinfrastructure'], etat=0)
                            messages.success(request,
                                                 f"modification réussi. veuiller finaliser votre {id_cat}")
                            r = 1

                        elif int(request.POST['nbchambre']) == ch and int(request.POST['nbsalon']) == sa and int(
                                    request.POST['nbcuisine']) == cu and int(request.POST['nbdouche']) == do and int(
                                    request.POST['nbinfrastructure']) == infra:
                                House.objects.filter(id=request.POST['id']).update(sommes=request.POST['sommes'],
                                                                                   description=mycdb(
                                                                                       request.POST['description']),
                                                                                   region=mycdb(request.POST['region']),
                                                                                   arrondissement=mycdb(
                                                                                       request.POST['arrondissement']),
                                                                                   nbchambre=request.POST['nbchambre'],
                                                                                   nbsalon=request.POST['nbsalon'],
                                                                                   nbcuisine=request.POST['nbcuisine'],
                                                                                   nbdouche=request.POST['nbdouche'],
                                                                                   nbinfrastructure=request.POST[
                                                                                       'nbinfrastructure'])
                                messages.success(request,
                                                 f"modification réussi. votre {id_cat} à ete Mise à jour")
                                r = 1
                    else:
                        messages.error(request, f"echec de modification . votre {id_cat} n'a pas ete Mise à jour. vérifier vos information")
                        r = 2

                elif id_cate == 2 or id_cate == 3 :
                    if (int(request.POST['sommes']) >= 1000 and request.POST['description'] != ' ' and request.POST['region'] != ' ' and request.POST['arrondissement'] != ' ' and int(request.POST['nbchambre']) >= 0 and int(request.POST['nbinfrastructure']) >= 0):

                        if int(request.POST['nbchambre']) < ch or int(request.POST['nbinfrastructure']) < infra:
                            messages.error(request, f" echec de modification . votre {id_cat} n'a pas ete Mise à jour. vérifier vos information. une ou plusieurs données sont inférieur à celle déja enregistrer")
                            r = 2

                        elif int(request.POST['nbchambre']) > ch or int(request.POST['nbinfrastructure']) > infra:
                            House.objects.filter(id = request.POST['id']).update(sommes = request.POST['sommes'], description = mycdb(request.POST['description']), region = mycdb(request.POST['region']), arrondissement = mycdb(request.POST['arrondissement']),  nbchambre = request.POST['nbchambre'],nbinfrastructure = request.POST['nbinfrastructure'], etat = 0)
                            messages.success(request,f"modification réussi. veuiller finaliser votre {id_cat}")
                            r = 1

                        elif int(request.POST['nbchambre']) == ch and int(request.POST['nbsalon']) == sa and int(request.POST['nbcuisine']) == cu and int(request.POST['nbdouche']) == do and int(request.POST['nbinfrastructure']) == infra:
                            House.objects.filter(id = request.POST['id']).update(sommes = request.POST['sommes'], description = mycdb(request.POST['description']), region = mycdb(request.POST['region']), arrondissement = mycdb(request.POST['arrondissement']),  nbchambre = request.POST['nbchambre'], nbinfrastructure = request.POST['nbinfrastructure'])
                            messages.success(request, f"modification réussi. votre {id_cat} à ete Mise à jour")
                            r = 1


                    else:
                        messages.error(request, f"echec de modification . votre {id_cat} n'a pas été Mise à jour. vérifier vos information")
                        r = 2

                elif id_cate == 9:
                    if (int(request.POST['sommes']) >= 1000 and request.POST['description'] != ' ' and request.POST['region'] != ' ' and request.POST['arrondissement'] != ' '):
                        House.objects.filter(id = request.POST['id']).update(sommes = request.POST['sommes'], description = mycdb(request.POST['description']), region = mycdb(request.POST['region']), arrondissement = mycdb(request.POST['arrondissement']))
                        messages.success(request,f"modification réussi. votre {id_cat} à ete Mise à jour")
                        r = 1
                    else:
                        messages.error(request, f"echec de modification . votre {id_cat} n'a pas ete Mise à jour. vérifier vos information")
                        r = 2

                else:
                    print("fou")
                    #il reste  les citées universitaire

    form1 = Update_house1()
    form2 = Update_house2()
    form3 = Update_house3()
    liste_maison = House.objects.filter(user=request.user)
    liste_maison_number = liste_maison.count()
    sategory = Category.objects.order_by('id').all()
    contex = {
        'formCompte':CompteUser(),
        'formRestorer':formRestorer,
        'lien0': lien0,
        'form1': form1,
        'form2': form2,
        'form3': form3,
        'has_perm': has_perm,
        'liste_maison_number': liste_maison_number,
        'liste_maisons': liste_maison,
        'sategory': sategory,
        'montant': montant,
        'r':r,
    }
    return render(request,'proprieter.html', context=contex)

@csrf_exempt
def sugestion(request):
    result = ""
    if not request.user.is_authenticated:
        return redirect('login')

    if request.method == "POST":
        pay = Profile.objects.filter(user_id= request.user.id)
        for me in pay:
            pay_de_moi = me.pay
        deido = mycdb(request.POST['keyword'].upper())
        liste = House.objects.complex_filter( Q(pay=pay_de_moi, arrondissement__icontains = deido, category_id = 8 ))
        for mo in liste:
            result = mo.arrondissement
        zero ="<div id='deidosu' value = '"+result+"'>"+result+"</div>" \
                                                               "<script>" \
                                                               "$('#deidosu').click(function(){ $('#id_arrondissement').val('"+result+"'); $('#suggesstion-box').hide();});" \
                                                               "</script>"
        return JsonResponse({'donnee': zero})

@csrf_exempt
def don(request):
    if not request.user.is_authenticated:
        return redirect('login')

    if request.method == "POST":
        id = request.POST['id']
        house = House.objects.filter(id=id)
        for use in house:
            donnee = use.user_id
        information = Profile.objects.filter(user_id=donnee).values()
        deido = list(information)
        return JsonResponse({'donnee': deido})
    else:
        sategory = Category.objects.order_by('id').all()
        ancien = Compte.objects.filter(user_id=request.user)
        for montants in ancien:
            montant = montants.montant

        context = {
            'sategory': sategory,
            'montant': montant
        }
        return render(request, 'liste_category.html', context=context)

@csrf_exempt
def consultation(request):
    if not request.user.is_authenticated:
        return redirect('login')

    if request.method == "POST":
        test = Consultation.objects.filter(user_id=request.user.id)
        if test.exists():
            return JsonResponse({'resultat': "cette opération à déja été éffectuer. veuillez actualiser votre page", })
        else:
            d = time.time()
            ancien = Compte.objects.filter(user_id=request.user)
            for montants in ancien:
                montant = montants.montant

            montant = montant - 500

            Compte.objects.filter(user_id=request.user).update(montant=montant)

            Consultation(day=d, user_id=request.user.id).save()

            return JsonResponse({'resultat': "yes",})

@csrf_exempt
def CAD(request):
    if not request.user.is_authenticated:
        return redirect('login')

    if request.method == "POST":
        user = User.objects.get(pk = request.user.id)
        if  request.user.has_perm("camhouse.add_house") and request.user.has_perm( "camhouse.delete_house") and request.user.has_perm("camhouse.view_house") and request.user.has_perm("camhouse.change_house"):  # pour savoir s'il est autoriser a ajouter une house
            return JsonResponse({'resultat': "cette opération à déja été éffectuer. veuillez actualiser votre page", })
        else:
            user.user_permissions.add(41, 42, 43, 44)
            return JsonResponse({'resultat': "yes", })

@csrf_exempt
def notification(request):
    r = 0
    if not request.user.is_authenticated:
        return redirect('login')

    if request.method == "POST":
        user = User.objects.filter(pk = request.user.id)
        if user.exists():
            if int(request.POST['db']) > 0 and int(request.POST['moi']) == 0 and request.POST['puol'] == "0":
                db = Notification.objects.filter(user_id=request.user.id, house_id=request.POST['db'])
                me = House.objects.filter(pk = request.POST['db'])
                for mee in me:
                    idme = mee.user_id
                if db.exists():
                    db.update(date=time.time())
                    return JsonResponse({'resultat': r })
                else:
                    profil = Profile.objects.filter(user_id=request.user.id)
                    for moi in profil:
                        proprieter = moi.phonenumber
                    deido = request.user.username
                    if idme != request.user.id:
                        Notification.objects.create(user_id= request.user.id, house_id= request.POST['db'], date=time.time(), phonenumber=proprieter, proprietaire= deido)
                    return JsonResponse({'resultat': r})

            elif int(request.POST['moi']) > 0 and int(request.POST['puol']) > 0 and int(request.POST['db']) == 0 :
                db = Notification.objects.filter(house_id=request.POST['puol'])
                if db.exists():
                    r = db.count()
                    return JsonResponse({'resultat': r})
                else:
                    r = 0
                    return JsonResponse({'resultat': r })

            elif int(request.POST['moi']) == 0 and int(request.POST['puol']) > 0 and int(request.POST['db']) == 0:
                db = Notification.objects.filter(house_id=request.POST['puol']).order_by("-date")
                print(request.user.id)
                if db.exists():
                    info = list(db.values())
                else:
                    info = ""
                return JsonResponse({'resultat': info })
        else:
            return JsonResponse({'resultat': r })
    else:
        return JsonResponse({'resultat': r })

@csrf_exempt
def locataire(request):
    if not request.user.is_authenticated:
        return redirect('login')

    if request.method == "POST":
        id = request.POST['id']
        house = House.objects.filter(id=id)
        for use in house:
            donnee = use.user_id
            etat = use.etat
        if donnee == request.user.id and etat == 3:
            Locataire = Occupation.objects.filter(house_id=id)
            for userL in Locataire:
                consommateur = userL.proprietaire
                date = userL.date
            information = Profile.objects.filter(user_id=consommateur)
            for infor in information:
                pay = infor.pay
                phonenumber = infor.phonenumber
                code = infor.code

            valeur = [
                        {'phonenumber': phonenumber,
                         'day': date,
                         'pay': pay,
                         'code': code
                         }
                    ]

            deido = list(valeur)
            return JsonResponse({'donnee': deido})
    else:
        sategory = Category.objects.order_by('id').all()
        ancien = Compte.objects.filter(user_id=request.user)
        for montants in ancien:
            montant = montants.montant

        context = {
            'sategory': sategory,
            'montant': montant
        }
        return render(request, 'liste_category.html', context=context)

@csrf_exempt
def locataireUniv(request):
    if not request.user.is_authenticated:
        return redirect('login')

    if request.method == "POST":
        id = request.POST['id']
        house = ChambreUniv.objects.filter(id=id)
        for use in house:
            user_id = use.composition_id
            etat = use.etat
        hous_id = Composition.objects.filter(id=user_id)
        for Houss_id in hous_id:
            idddh = Houss_id.house_id
        use = House.objects.filter(id=idddh)
        for me in use:
            donnee = me.user_id
        if donnee == request.user.id and etat == 3:
            Locataire = OccupationUniv.objects.filter(chambre_id=id)
            for userL in Locataire:
                consommateur = userL.proprietaire
                date = userL.date
            information = Profile.objects.filter(user_id=consommateur)
            for infor in information:
                pay = infor.pay
                phonenumber = infor.phonenumber
                code = infor.code

            valeur = [
                        {'phonenumber': phonenumber,
                         'day': date,
                         'pay': pay,
                         'code': code
                         }
                    ]

            deido = list(valeur)
            return JsonResponse({'donnee': deido})
    else:
        sategory = Category.objects.order_by('id').all()
        ancien = Compte.objects.filter(user_id=request.user)
        for montants in ancien:
            montant = montants.montant

        context = {
            'sategory': sategory,
            'montant': montant
        }
        return render(request, 'liste_category.html', context=context)

def liste_category(request, category):
    test = get_object_or_404(Category, pk=category)# renvoi ereur 404 si category n'existe pas
    if not request.user.is_authenticated:
        return redirect('login')

    d = time.time()
    dac = 0
    autorisation = Consultation.objects.filter(user_id=request.user.id)
    if autorisation.exists():
        dac= 1
    else:
        dac = 0
    formReserve = ReservePuol()
    formCompte = CompteUser()
    has_perm = False
    if request.method == 'POST':
        ancien = Compte.objects.filter(user_id=request.user)
        for montants in ancien:
            montant = montants.montant
            idC = montants.id
        if request.POST['montant'] == "":
            print("operation anulée")
        elif float(request.POST['montant']) <= 0:
            print("opération anulée m")

        elif float(request.POST['montant']) > 0:
            montant = montant + float(request.POST['montant'])
            Compte.objects.filter(user_id=request.user).update(montant=montant)

        else:
            print("operation impossible")

        if request.POST['proprietaire'] == "" or request.POST['puol'] == "" or request.POST['montant'] == 0:
            print("reservation annulé")

        elif int(request.POST['proprietaire']) <= 0 or int(request.POST['puol']) <= 0 or request.POST['montant'] == 0:
            print("donné erone")

        elif int(request.POST['proprietaire']) > 0 and int(request.POST['puol']) > 0 and montant >= 1000:
            id = request.POST['puol']
            house = House.objects.filter(id=id)
            if house.exists():
                for use in house:
                    proprio = use.user_id
                    puol = use.id
                moi = request.user.id
                date = d
            else:
                print("off")
            test = Reservation.objects.filter(house_id=id)
            if test.exists():
                print("yes")
            else:
                form = Reservation(proprietaire=proprio, date=date, user_id=request.user.id, house_id=puol)
                form.save()
                dos = montant - 1000
                Compte.objects.filter(id=idC).update(montant=dos)
                House.objects.filter(id=puol).update(etat=2)
        else:
            print(f"reservation impossible car {request.POST['proprietaire']} : {request.POST['puol']}")

    if request.user.has_perm("camhouse.add_house") and request.user.has_perm("camhouse.delete_house") and request.user.has_perm("camhouse.view_house") and request.user.has_perm("camhouse.change_house"): #si l'utilisateur a la permition d'ajouter une house, on l'autorise
        has_perm = True
    if category == 1:
        lien1 = 'un'
    elif category == 2:
        lien1 = 'deux'
    elif category == 3:
        lien1 = 'trois'
    elif category == 4:
        lien1 = 'quatre'
    elif category == 5:
        lien1 = 'cinq'
    elif category == 6:
        lien1 = 'six'
    elif category == 7:
        lien1 = 'sept'
    elif category == 8:
        lien1 = 'huit'
    elif category == 9:
        lien1 = 'neuf'
    me = Profile.objects.filter(user_id= request.user.id)
    for moi in me:
        pay_moi =moi.pay
    listes = House.objects.filter(category_id=category, pay=pay_moi)
    paginator = Paginator(listes, 8)
    page_number = request.GET.get('page')
    page_object = paginator.get_page(page_number)
    sategory = Category.objects.order_by('id').all()
    ancien = Compte.objects.filter(user_id=request.user)
    for montants in ancien:
        montant = montants.montant


    context= {
        'autorisation':dac,
        'formReserve':formReserve,
        'formCompte':formCompte,
        'lien1': lien1,
        'has_perm': has_perm,
        'listes': page_object,
        'sategory': sategory,
        'montant': montant
    }
    return render(request, 'liste_category.html', context=context)

def liste_category_un(request):
    category = 1
    test = get_object_or_404(Category, pk=category)# renvoi ereur 404 si category n'existe pas
    if not request.user.is_authenticated:
        return redirect('login')

    d = time.time()
    # je suprime la consultation si 2jour(48heures) sont passée
    consult = Consultation.objects.filter(user_id=request.user.id)
    reserve = Reservation.objects.filter(user_id=request.user.id, proprietaire=request.user.id)

    if consult.exists():
        for const in consult:
            dte = const.day
        valeur = (d - dte) / 3600
        if valeur >= 48:
            consult.delete()
    # je suprime la reservation si 7jour(168heures) sont passée
    if reserve.exists():
        for const in reserve:
            dte = const.date
            idh = const.house_id
        valeur = (d - dte) / 3600
        if valeur >= 168:
            reserve.delete()
            House.objects.filter(id=idh).update(etat=1)

    dac = 0
    autorisation = Consultation.objects.filter(user_id=request.user.id)
    if autorisation.exists():
        dac= 1
    else:
        dac = 0
    formReserve = ReservePuol()
    formCompte = CompteUser()
    has_perm = False
    if request.method == 'POST':
        ancien = Compte.objects.filter(user_id=request.user)
        for montants in ancien:
            montant = montants.montant
            idC = montants.id
        if request.POST['montant'] == "":
            print("operation anulée")
        elif float(request.POST['montant']) <= 0:
            print("opération anulée m")

        elif float(request.POST['montant']) > 0:
            montant = montant + float(request.POST['montant'])
            Compte.objects.filter(user_id=request.user).update(montant=montant)

        else:
            print("operation impossible")

        if request.POST['proprietaire'] == "" or request.POST['puol'] == "" or request.POST['montant'] == 0:
            print("reservation annulé")

        elif int(request.POST['proprietaire']) <= 0 or int(request.POST['puol']) <= 0 or request.POST['montant'] == 0:
            print("donné erone")

        elif int(request.POST['proprietaire']) > 0 and int(request.POST['puol']) > 0 and montant >= 1000:
            id = request.POST['puol']
            house = House.objects.filter(id=id)
            if house.exists():
                for use in house:
                    proprio = use.user_id
                    puol = use.id
                moi = request.user.id
                date = d
            else:
                print("off")
            test = Reservation.objects.filter(house_id=id)
            if test.exists():
                print("yes")
            else:
                form = Reservation(proprietaire=proprio, date=date, user_id=request.user.id, house_id=puol)
                form.save()
                dos = montant - 1000
                Compte.objects.filter(id=idC).update(montant=dos)
                House.objects.filter(id=puol).update(etat=2)
        else:
            print(f"reservation impossible car {request.POST['proprietaire']} : {request.POST['puol']}")

    if request.user.has_perm("camhouse.add_house") and request.user.has_perm("camhouse.delete_house") and request.user.has_perm("camhouse.view_house") and request.user.has_perm("camhouse.change_house"): #si l'utilisateur a la permition d'ajouter une house, on l'autorise
        has_perm = True
    if category == 1:
        lien1 = 'un'
    elif category == 2:
        lien1 = 'deux'
    elif category == 3:
        lien1 = 'trois'
    elif category == 4:
        lien1 = 'quatre'
    elif category == 5:
        lien1 = 'cinq'
    elif category == 6:
        lien1 = 'six'
    elif category == 7:
        lien1 = 'sept'
    elif category == 8:
        lien1 = 'huit'
    elif category == 9:
        lien1 = 'neuf'
    me = Profile.objects.filter(user_id= request.user.id)
    for moi in me:
        pay_moi =moi.pay
    listes = House.objects.filter(category_id=category, pay=pay_moi)
    paginator = Paginator(listes, 8)
    page_number = request.GET.get('page')
    page_object = paginator.get_page(page_number)
    sategory = Category.objects.order_by('id').all()
    ancien = Compte.objects.filter(user_id=request.user)
    for montants in ancien:
        montant = montants.montant


    context= {
        'autorisation':dac,
        'formReserve':formReserve,
        'formCompte':formCompte,
        'lien1': lien1,
        'has_perm': has_perm,
        'listes': page_object,
        'sategory': sategory,
        'montant': montant
    }
    return render(request, 'liste_category.html', context=context)
#**
def detail_category(request, id):
    hpuol = id
    chambre_univ = []
    if not request.user.is_authenticated:
        return redirect('login')

    has_perm = False
    test = get_object_or_404(House, pk=id)# renvoi ereur 404 si id n'existe pas
    d = time.time()
    category = Category.objects.order_by('id').all()
    d = time.time()
    if request.user.has_perm("camhouse.add_house") and request.user.has_perm(
            "camhouse.delete_house") and request.user.has_perm("camhouse.view_house") and request.user.has_perm(
            "camhouse.change_house"):  # si l'utilisateur a la permition d'ajouter une house, on l'autorise
        has_perm = True
    formReserve = ReservePuol()
    formCompte = CompteUser()
    ancien = Compte.objects.filter(user_id=request.user)
    for montants in ancien:
        montant = montants.montant
        idC = montants.id

    if request.method == 'POST':
        if request.POST['montant'] == "":
            print("operation anulée1")
        elif float(request.POST['montant']) <= 0:
            print("opération anulée2")

        elif float(request.POST['montant']) > 0:
            montant = montant + float(request.POST['montant'])
            Compte.objects.filter(user_id=request.user).update(montant=montant)
        else:
            print("operation impossible")

        if request.POST['proprietaire'] == "" or request.POST['puol'] == "" or request.POST['montant'] == 0:
            print("reservation annulé3")

        elif int(request.POST['proprietaire']) <= 0 or int(request.POST['puol']) <= 0 or request.POST['montant'] == 0:
            print("donné erone")

        elif int(request.POST['proprietaire']) > 0 and int(request.POST['puol']) > 0 and montant >= 1000:
            id = request.POST['puol']
            house = House.objects.filter(id=id)
            if house:
                for use in house:
                    proprio = use.user_id
                    puol = use.id
                moi = request.user.id
                date = d
            else:
                print("off")
            test = Reservation.objects.filter(house_id=id)
            if test:
                print("yes")
            else:
                if(request.POST['type'] == "puol"):
                    for montants in ancien:
                        montant = montants.montant
                    form = Reservation(proprietaire=proprio, date=date, user_id=request.user.id, house_id=puol)
                    form.save()
                    dos = montant - 1000
                    Compte.objects.filter(id=idC).update(montant=dos)
                    House.objects.filter(id=puol).update(etat=2)
                    ancien = Compte.objects.filter(user_id=request.user)

                    context = {
                        'has_perm': has_perm,
                        'sategory': category,
                        'montant': montant,
                        'formCompte': CompteUser()
                    }
                    return render(request, 'home_ch.html', context=context)
                if(request.POST['type'] == "univ"):
                    for montants in ancien:
                        montant = montants.montant
                    house = ChambreUniv.objects.filter(id=id)
                    for use in house:
                        proprio = use.composition.house.user_id
                        puol = use.id
                    form = ReservationUniv(proprietaire=proprio, date=d, user_id=request.user.id, chambre_id=puol)
                    form.save()
                    dos = montant - 1000
                    Compte.objects.filter(id=idC).update(montant=dos)
                    ChambreUniv.objects.filter(id=puol).update(etat=2)
                    ancien = Compte.objects.filter(user_id=request.user)

                    context = {
                        'has_perm': has_perm,
                        'sategory': category,
                        'montant': montant,
                        'formCompte': CompteUser()
                    }
                    return render(request, 'home_ch.html', context=context)

        else:
            print(f"reservation impossible car {request.POST['proprietaire']} : {request.POST['puol']}")


    purch_number = 0
    purd_number = 0
    purcu_number = 0
    purs_number = 0
    sategory = Category.objects.order_by('id').all()

    detail = House.objects.filter(id = id)
    compose = Composition.objects.filter(house_id=id)
    for comp in compose:
        idCompo = comp.id

    if detail : # si l'id existe j'effectu le traitement

        for infra in detail:
            etat = infra.etat
            catego = infra.category_id
            nbinfra = infra.nbinfrastructure #je recupère le numbre d'infrastructure a enregistrer
            nbchTotal = infra.nbchambre  #je recupère le numbre de chambre a enregistrer
            nbcuTotal = infra.nbcuisine  #je recupère le numbre de cuisine a enregistrer
            nbdoTotal = infra.nbdouche  #je recupère le numbre de douche a enregistrer
            nbsaTotal = infra.nbsalon  #je recupère le numbre de salon a enregistrer

        if nbinfra is None:
            nbinfra = 0
        infrastructures = Infrastructure.objects.filter(house_id = id)
        if nbsaTotal is None:
            nbsaTotal = 0
        if nbchTotal is None:
            if catego == 9:
                nbchTotal = 1
            else:
                nbchTotal = 0
        if nbcuTotal is None:
            nbcuTotal = 0
        if nbdoTotal is None:
            nbdoTotal = 0
        purin_number = infrastructures.count() #je recupère le numbre d'infrastructure enredistrer
        chambres = Composition.objects.filter(house_id = id, type_id=1)#je recupère le numbre de chambre enredistrer
        for nbch in chambres:
            if catego == 9:
                nbch.numbre =1
            purch_number += nbch.numbre
        douches = Composition.objects.filter(house_id = id, type_id=4)#je recupère le numbre de douche enredistrer
        for nbd in douches:
            purd_number += nbd.numbre
        cuisines = Composition.objects.filter(house_id = id, type_id=3)#je recupère le numbre de cuisine enredistrer
        for nbcu in cuisines:
            purcu_number += nbcu.numbre
        salons = Composition.objects.filter(house_id = id, type_id=2)#je recupère le numbre de salon enredistrer
        for nbs in salons:
            purs_number += nbs.numbre
        for activech in chambres: #je recupère le dernier id pour utiliser l\'atribu active dans carrousel au niveau du template
            purch = activech.id
        for activecu in cuisines:
            purcu = activecu.id
        for actived in douches:
            purd = actived.id
        for actives in salons:
            purs = actives.id
        for infrastructur in infrastructures:
            purin = infrastructur.id

        if nbchTotal == 0 or nbchTotal is None:

            purch = 0

        if nbsaTotal == 0 or nbsaTotal is None:
            purs = 0

        if nbdoTotal == 0 or nbdoTotal is None:
            purd = 0

        if nbcuTotal == 0 or nbcuTotal is None:
            purcu = 0
        if purin_number == 0 or purin_number is None:
            purin = 0

        if catego == 8:
            chambre_univ = ChambreUniv.objects.filter(composition__house=id)#je recupère les ou la ChambreUniv ou l'id de la maison qui est dans composition == a id

        if purch_number != nbchTotal or purcu_number != nbcuTotal or purd_number != nbdoTotal or purs_number != nbsaTotal or purin_number != nbinfra :
            return redirect('camer_house:liste_category_un') # si la piol n'est pas totalement enregistrer on repart a l'acceuil

        ancien = Compte.objects.filter(user_id=request.user)
        for montants in ancien:
            montant = montants.montant

        context = {
            'chambre_univ':chambre_univ,
            'id':hpuol,
            'formReserve':ReservePuol(),
            'formReserveC':ReserveChambre(),
            'formCompte': CompteUser(),
            'has_perm': has_perm,
            'infrastructures': infrastructures,
            'purin': purin,
            'purinn': purin_number,
            'catego': catego,
            'actives': purs,
            'actived': purd,
            'activecu': purcu,
            'activech': purch,
            'details': detail,
            'catego': catego,
            'sategory': sategory,
            'chambres': chambres,
            'cuisines': cuisines,
            'douches': douches,
            'salons': salons,
            'montant':montant,
            'etat':etat
        }
        #je dois rediriger vers liste category
        return render(request, 'detail_category.html', context=context)
    else:
        return redirect('camer_house:liste_category_un')
#**
def search(request):
    if not request.user.is_authenticated:
        return redirect('login')

    has_perm = False
    dac = 0
    autorisation = Consultation.objects.filter(user_id=request.user.id)
    if autorisation.exists():
        dac = 1
    else:
        dac = 0

    category = Category.objects.order_by('id').all()
    d = time.time()
    formReserve = ReservePuol()
    formCompte = CompteUser()
    if request.user.has_perm("camhouse.add_house") and request.user.has_perm("camhouse.delete_house") and request.user.has_perm("camhouse.view_house") and request.user.has_perm("camhouse.change_house"): #si l'utilisateur a la permition d'ajouter une house, on l'autorise
        has_perm = True
    me = Profile.objects.filter(user_id= request.user.id)
    for moi in me:
        pay_moi =moi.pay

    if request.GET.get('category') == '8':
        ss = request.GET.get('search').upper()
    else:
        ss = request.GET.get('search')
    search_value = mycdb(ss)
    search_category = request.GET.get('category')
    listes = House.objects.filter(Q(category_id = search_category, sommes__icontains = search_value) |
                                  Q(category_id = search_category, region__icontains = search_value) |
                                  Q(category_id = search_category, arrondissement__icontains = search_value) |
                                  Q(category_id = search_category, description__icontains = search_value), etat = 1, pay= pay_moi)
    paginator = Paginator(listes, 8)
    page_number = request.GET.get('page')
    page_object = paginator.get_page(page_number)
    sategory = Category.objects.order_by('id').all()
    ancien = Compte.objects.filter(user_id=request.user)
    for montants in ancien:
        montant = montants.montant
        idC = montants.id

    if request.method == 'POST':
        if request.POST['montant'] == "":
            print("operation anulée")
        elif float(request.POST['montant']) <= 0:
            print("opération anulée")

        elif float(request.POST['montant']) > 0:
            montant = montant + float(request.POST['montant'])
            Compte.objects.filter(user_id=request.user).update(montant=montant)
        else:
            print("operation impossible")

        if request.POST['proprietaire'] == "" or request.POST['puol'] == "" or request.POST['montant'] == 0:
            print("reservation annulé")

        elif int(request.POST['proprietaire']) <= 0 or int(request.POST['puol']) <= 0 or request.POST['montant'] == 0:
            print("donné erone")

        elif int(request.POST['proprietaire']) > 0 and int(request.POST['puol']) > 0 and montant >= 1000:
            id = request.POST['puol']
            house = House.objects.filter(id=id)
            if house:
                for use in house:
                    proprio = use.user_id
                    puol = use.id
                moi = request.user.id
                date = d
            else:
                print("off")
            test = Reservation.objects.filter(house_id=id)
            if test:
                print("yes")
            else:
                form = Reservation(proprietaire=proprio, date=date, user_id=request.user.id, house_id=puol)
                form.save()
                dos = montant - 1000
                Compte.objects.filter(id=idC).update(montant=dos)
                House.objects.filter(id=puol).update(etat=2)
                ancien = Compte.objects.filter(user_id=request.user)
                for montants in ancien:
                    montant = montants.montant
                context = {
                    'has_perm': has_perm,
                    'sategory': category,
                    'montant': montant,
                    'formCompte': CompteUser()
                }
                return render(request, 'home_ch.html', context=context)

        else:
            print(f"reservation impossible car {request.POST['proprietaire']} : {request.POST['puol']}")


    trouve = listes.count()
    context = {
                'autorisation':dac,
        'formReserve': formReserve,
        'formCompte': formCompte,
        'has_perm': has_perm,
        'trouver': trouve,
        'listes': page_object,
        'search_value': search_value,
        'search_category': search_category,
        'sategory': sategory,
        'montant': montant

    }
    return render(request, 'search.html', context=context)
#**
def rapid_search(request):
    if not request.user.is_authenticated:
        return redirect('login')

    has_perm = False
    dac = 0
    autorisation = Consultation.objects.filter(user_id=request.user.id)
    if autorisation.exists():
        dac = 1
    else:
        dac = 0
    category = Category.objects.order_by('id').all()
    d = time.time()
    dac = 0
    autorisation = Consultation.objects.filter(user_id=request.user.id)
    if autorisation.exists():
        dac = 1
    else:
        dac = 0

    formReserve = ReservePuol()
    formCompte = CompteUser()
    if request.user.has_perm("camhouse.add_house") and request.user.has_perm("camhouse.delete_house") and request.user.has_perm("camhouse.view_house") and request.user.has_perm("camhouse.change_house"): #si l'utilisateur a la permition d'ajouter une house, on l'autorise
        has_perm = True
    me = Profile.objects.filter(user_id= request.user.id)
    for moi in me:
        pay_moi =moi.pay
    search_region = mycdb(request.GET.get('region'))
    search_arrondissement = mycdb(request.GET.get('arrondissement'))
    search_chambre = request.GET.get('chambre')
    search_cuisine = request.GET.get('cuisine')
    search_douche = request.GET.get('douche')
    search_salon = request.GET.get('salon')
    search_somme = request.GET.get('somme')
    search_category = request.GET.get('category')
    listes = House.objects.filter(Q(region__icontains = mycdb(search_region) , arrondissement__icontains = mycdb(search_arrondissement), nbchambre__icontains = search_chambre,
                                    nbsalon__icontains = search_salon, nbcuisine__icontains = search_cuisine, nbdouche__icontains = search_douche,
                                    category_id = search_category, sommes__icontains = search_somme), etat = 1, pay=pay_moi )
    paginator = Paginator(listes, 8)
    page_number = request.GET.get('page')
    page_object = paginator.get_page(page_number)
    sategory = Category.objects.order_by('id').all()
    ancien = Compte.objects.filter(user_id=request.user)
    for montants in ancien:
        montant = montants.montant
        idC = montants.id

    if request.method == 'POST':
        if request.POST['montant'] == "":
            print("operation anulée")
        elif float(request.POST['montant']) <= 0:
            print("opération anulée")

        elif float(request.POST['montant']) > 0:
            montant = montant + float(request.POST['montant'])
            Compte.objects.filter(user_id=request.user).update(montant=montant)
        else:
            print("operation impossible")

        if request.POST['proprietaire'] == "" or request.POST['puol'] == "" or request.POST['montant'] == 0:
            print("reservation annulé")

        elif int(request.POST['proprietaire']) <= 0 or int(request.POST['puol']) <= 0 or request.POST['montant'] == 0:
            print("donné erone")

        elif int(request.POST['proprietaire']) > 0 and int(request.POST['puol']) > 0 and montant >= 1000:
            id = request.POST['puol']
            house = House.objects.filter(id=id)
            if house:
                for use in house:
                    proprio = use.user_id
                    puol = use.id
                moi = request.user.id
                date = d
            else:
                print("off")
            test = Reservation.objects.filter(house_id=id)
            if test:
                print("yes")
            else:
                form = Reservation(proprietaire=proprio, date=date, user_id=request.user.id, house_id=puol)
                form.save()
                dos = montant - 1000
                Compte.objects.filter(id=idC).update(montant=dos)
                House.objects.filter(id=puol).update(etat=2)
                ancien = Compte.objects.filter(user_id=request.user)
                for montants in ancien:
                    montant = montants.montant
                context = {
                    'has_perm': has_perm,
                    'sategory': category,
                    'montant': montant,
                    'formCompte': CompteUser()
                }
                return render(request, 'home_ch.html', context=context)

        else:
            print(f"reservation impossible car {request.POST['proprietaire']} : {request.POST['puol']}")


    trouve = listes.count()

    context = {
        'autorisation': dac,
        'formReserve': formReserve,
        'formCompte':formCompte,
        'montant': montant,
        'has_perm': has_perm,
        'trouver': trouve,
        'search_region': search_region,
        'search_arrondissement': search_arrondissement,
        'search_chambre': search_chambre,
        'search_cuisine': search_cuisine,
        'search_douche': search_douche,
        'search_salon': search_salon,
        'search_somme': search_somme,
        'search_category': search_category,
        'listes': page_object,
        'sategory': sategory,
    }
    return render(request, 'rapid_search.html', context = context)

def enregistrement(request): # il reste l'enregistrement des citée universitaire
    has_perm = False
    if not request.user.is_authenticated:
        return redirect('login')

    formCompte = CompteUser()
    category = request.GET.get('category')
    profile = Profile.objects.filter(user_id=request.user.id)
    for info in profile:
        pay = info.pay
    ancien = Compte.objects.filter(user_id=request.user)
    for montants in ancien:
        montant = montants.montant
    if request.method == 'POST':
        ancien = Compte.objects.filter(user_id=request.user)
        for montants in ancien:
            montant = montants.montant
        if request.POST['montant'] == "":
            print("operation anulée")
        elif float(request.POST['montant']) <= 0:
            print("opération anulée")

        elif float(request.POST['montant']) > 0:
            montant = montant + float(request.POST['montant'])
            Compte.objects.filter(user_id=request.user).update(montant=montant)
        else:
            print("zero montant")
    sategory = Category.objects.order_by('id').all()
    if not request.user.has_perm("camhouse.add_house") and not request.user.has_perm("camhouse.delete_house") and not request.user.has_perm("camhouse.view_house") and not request.user.has_perm("camhouse.change_house"): #pour savoir s'il est autoriser a ajouter une house
        raise PermissionDenied #on renvoi ver la page 403
    else:
        has_perm = True

    if category == '2' or category == '3' or category == '8':
        if request.method == 'POST':
            form = Enregistrement_Hotel(request.POST, request.FILES)
            if form.is_valid():
                form = form.save(commit=False)
                form.user = request.user
                form.image.name = f'{d}'
                form.lat = 000.00
                form.lng = 000.00
                form.date = d
                form.pay = pay
                pascal = f'{form.category.id}'
                if category == '3' or category == '8':
                    pascal = category
                    form.category_id = category
                taille = form.image.size/1048576
                if(category == pascal and form.nbinfrastructure >= 0 and form.type.id > 0 and form.type.id < 5 and form.description != ' ' and form.region != ' ' and form.arrondissement != ' ' and form.nom !=' '):
                    if(taille <= 1.5):
                        form.region = mycdb(form.region)
                        if category == '8':
                            form.arrondissement = form.arrondissement.upper()
                        form.arrondissement = mycdb(form.arrondissement)
                        form.description = mycdb(form.description)
                        form.nom =mycdb(form.nom)
                        form.save()
                        return redirect('camer_house:enregistrement2_ch')
                    else:
                        messages.error(request, f"la taille de l'image est suppérieur à 2Mo. taille actuèlle : {form.image.size/1048576}Mo")
                        form = Enregistrement_Hotel()
                        context = {
                            'has_perm': has_perm,
                            'form': form,
                            'formCompte': formCompte,
                            'category': category,
                            'sategory': sategory,
                            'montant': montant,
                        }
                        return render(request, 'enregistrement.html', context=context)
                else:
                    print(pascal)
                    messages.error(request, "formulaire non approuvé")
                    form = Enregistrement_Hotel()
                    context = {
                        'form': form,
                        'formCompte': formCompte,
                        'category': category,
                        'sategory': sategory,
                        'montant': montant,
                    }
                    return render(request, 'enregistrement.html', context=context)
                #return HttpResponse(form.category)
            else:
 #               for field in form.errors:
  #                  form[field].field.widget.attrs['class'] += ' is-invalid'  # je rend les input invalide en rouge pour signaler lerreur
                messages.error(request, "formulaire non approuvé")
                context = {
                    'has_perm': has_perm,
                    'form': form,
                    'formCompte': formCompte,
                    'category': category,
                    'sategory': sategory,
                    'montant': montant,
                }
                return render(request, 'enregistrement.html', context=context)
        else:
            form = Enregistrement_Hotel()
            context = {
                'has_perm': has_perm,
                'form': form,
                'formCompte': formCompte,
                'category': category,
                'sategory': sategory,
                'montant': montant,
            }
            return render(request, 'enregistrement.html', context=context)
    #elif category == '8' :
        #form = Enregistrement_citee_universtaire()
    elif category == '9':
        if request.method == 'POST':
            form = Enregistrement_Boutique(request.POST, request.FILES)
            if form.is_valid():
                form = form.save(commit=False)  # on affecte les valeur actuel du formulaire a la variable form
                form.user = request.user  # comme le user ne fait pas parti des donnée de form, on l'ajoute
                form.image.name = f'{d}'  # je n'ai pas mis une extention mais sa marche
                form.lat = 000.00
                form.lng = 000.00
                form.date = d
                form.pay = pay

                pascal = f'{form.category.id}'
                taille = form.image.size/1048576
                if(category == pascal and  form.sommes >= 1000 and form.type.id > 0 and form.type.id < 5 and form.description != ' ' and form.region != ' ' and form.arrondissement != ' ') :
                    if (taille <= 1.5):
                        form.region = mycdb(form.region)
                        form.arrondissement = mycdb(form.arrondissement)
                        form.description = mycdb(form.description)
                        form.save()  # puis on sauvegarde
                        return redirect('camer_house:enregistrement2_ch')
                    else:
                        messages.error(request,f"la taille de l'image est suppérieur à 1.5Mo. taille actuèlle : {form.image.size/1048576}Mo")
                        form = Enregistrement()
                        context = {
                            'has_perm': has_perm,
                            'form': form,
                            'formCompte': formCompte,
                            'category': category,
                            'sategory': sategory,
                            'montant': montant,
                        }
                        return render(request, 'enregistrement.html', context=context)
                else:
                    messages.error(request, "formulaire non approuvé")
                    context = {
                        'has_perm': has_perm,
                        'formCompte': formCompte,
                        'form': form,
                        'category': category,
                        'sategory': sategory,
                        'montant': montant,
                    }
                    return render(request, 'enregistrement.html', context=context)
                # return HttpResponse(form.category)
            else: #si le formulaire n'est pas valide
   #             for field in form.errors:
    #                form[field].field.widget.attrs['class'] += ' is-invalid'  # je rend les input invalide en rouge pour signaler lerreur
                messages.error(request, "formulaire non approuvé")
                context = {
                    'has_perm': has_perm,
                    'form': form,
                    'formCompte': formCompte,
                    'category': category,
                    'sategory': sategory,
                    'montant': montant,
                }
                return render(request, 'enregistrement.html', context=context)
            # return HttpResponse(form.category)
        else:
            form = Enregistrement_Boutique()
            context = {
                'has_perm': has_perm,
                'form': form,
                'formCompte': formCompte,
                'category': category,
                'sategory': sategory,
                'montant': montant,
            }
            return render(request, 'enregistrement.html', context=context)
    elif category == '1' or category == '4' or category == '5' or category == '6' or category == '7' :
        if request.method == 'POST':
            form = Enregistrement(request.POST, request.FILES)
            if form.is_valid():# si le formulaire est valide
                form = form.save(commit=False) #on affecte les valeur actuel du formulaire a la variable form
                form.user = request.user # comme le user ne fait pas parti des donnée de form, on l'ajoute
                form.image.name = f'{d}' #je n'ai pas mis une extention mais sa marche
                form.lat = 000.00
                form.lng = 000.00
                form.date = d
                form.pay = pay

                form.etat = 0
                # rapelon ici que nous pouvons avoir acces a tout les donnée du formulaire. exemple: a ce niveau, le type = à form.type
                pascal = f'{form.category.id}'
                taille = form.image.size/1048576
                if category == '4' or category == '5' or category == '6' or category == '7':
                    pascal = category
                    form.category_id = category
                if(category == pascal and form.nbinfrastructure >= 0 and form.nbchambre >= 0 and form.nbdouche >= 0 and form.nbcuisine >= 0 and form.nbsalon >= 0 and form.sommes >= 1000 and form.type.id > 0 and form.type.id < 5 and form.description != ' ' and form.region != ' ' and form.arrondissement != ' '):
                    if(taille  <= 1.5):
                        form.region = mycdb(form.region)
                        form.arrondissement = mycdb(form.arrondissement)
                        form.description = mycdb(form.description)
                        form.save() # puis on sauvegarde
                        return redirect('camer_house:enregistrement2_ch')
                    else :
                        messages.error(request,f"la taille de l'image est suppérieur à 1.5Mo. taille actuèlle : {form.image.size/1048576}Mo")
                        form = Enregistrement()
                        context = {
                            'formCompte': formCompte,
                            'has_perm': has_perm,
                            'form': form,
                            'category': category,
                            'sategory': sategory,
                            'montant': montant,
                        }
                        return render(request, 'enregistrement.html', context=context)
                else:
                    messages.error(request, "formulaire non approuvé 1")
                    form = Enregistrement()
                    context = {
                        'has_perm': has_perm,
                        'formCompte': formCompte,
                        'form': form,
                        'category': category,
                        'sategory': sategory,
                        'montant': montant,
                    }
                    return render(request, 'enregistrement.html', context =context )
            else: #si le formulaire n'est pas valide
 #               for field in form.errors:
  #                  form[field].field.widget.attrs['class'] += ' is-invalid'  # je rend les input invalide en rouge pour signaler lerreur
                messages.error(request, "formulaire non envoyé")
                context = {
                    'has_perm': has_perm,
                    'form': form,
                    'formCompte': formCompte,
                    'category': category,
                    'sategory': sategory,
                    'montant': montant,
                }
                return render(request, 'enregistrement.html', context=context)

        else:
            form = Enregistrement()
            context = {
                'has_perm': has_perm,
                'formCompte': formCompte,
                'form': form,
                'category': category,
                'sategory': sategory,
                'montant': montant,
            }
            return render(request, 'enregistrement.html', context=context)
    else:
        liste_maison = House.objects.filter(user=request.user)
        liste_maison_number = liste_maison.count()
        sategory = Category.objects.order_by('id').all()
        context = {
            'has_perm': has_perm,
            'liste_maison_number': liste_maison_number,
            'formCompte': formCompte,
            'liste_maisons': liste_maison,
            'sategory': sategory,
            'montant': montant,
        }
        return render(request, 'proprieter.html', context=context)
    context = {
        'has_perm': has_perm,
        'formCompte': formCompte,
        'form' : form,
        'category': category,
        'sategory': sategory,
        'montant': montant,
    }
    return render(request, 'enregistrement.html', context=context)

def enregistrement2(request):
    d = time.time()
    has_perm = False
    if not request.user.is_authenticated:
        return redirect('login')

    formCompte = CompteUser()
    ancien = Compte.objects.filter(user_id=request.user)
    for montants in ancien:
        montant = montants.montant
    sategory = Category.objects.order_by('id').all()
    if request.user.is_authenticated:
        print(request.user)
        idh = House.objects.filter(user=request.user) # je recupère tous les maisons enregistrer par cet utilisateur
        if request.method == 'POST':
            if request.POST['montant'] == "":
                print("operation anulée")
            elif float(request.POST['montant']) <= 0:
                print("opération anulée")

            elif float(request.POST['montant']) > 0:
                montant = montant + float(request.POST['montant'])
                Compte.objects.filter(user_id=request.user).update(montant=montant)
    else:
        raise  PermissionDenied
    if not request.user.has_perm("camhouse.add_house") and not request.user.has_perm("camhouse.delete_house") and not request.user.has_perm("camhouse.view_house") and not request.user.has_perm("camhouse.change_house"): #pour savoir s'il est autoriser a ajouter une house
        raise PermissionDenied #on renvoi ver la page 403
    else:
        has_perm = True

    for ids in idh:
        id = ids.id #je recupère l'id de la derniere maison enregistrer par cet utilisateur
        catego = ids.category_id

    maisons = House.objects.filter(id=id) # je recupèr tous ls info sur la maison
 #   chambre_a_duppliques = Composition.objects.filter(house=id)
    for maison in maisons: # je recupère les détail de la maison
        nbchambre = maison.nbchambre # je recupère le nombre de chambre
        nbcuisine = maison.nbcuisine # je recupère le nombre de cuisine
        nbsalon = maison.nbsalon # je recupère le nombre de salon
        nbdouche = maison.nbdouche # je recupère le nombre de douche
        nbinfrastructure = maison.nbinfrastructure # je recupère le nombre d'infrstructure
        etat = maison.etat #je recupère l'"tat de la maison
    chambres = Composition.objects.filter(house_id=id, type=1) # je recupère tous les chambres deja ajoutées
    chambre_nb = 0

    cuisines = Composition.objects.filter(house_id=id, type=3) # je recupère tous les cuisines deja ajoutées
    cuisine_nb = 0

    salons = Composition.objects.filter(house_id=id, type=2) # je recupère tous les salons deja ajoutées
    salon_nb = 0

    douches = Composition.objects.filter(house_id=id, type=4) # je recupère tous les douches deja ajoutées
    douche_nb = 0

    infrastructures = Infrastructure.objects.filter(house_id=id) # je recupère tous les infrastructure deja ajoutées
    infrastructure_nb = infrastructures.count() #nombre d'infrastructure deja renregistrer

    if catego == 9:
        boutik = Composition.objects.filter(house_id=id) # je verifi si la boutique est deja enregistrer
        pp = boutik.count()
    else:
        pp = 1

    if nbchambre is None:
        chambre_nb = 0
        chambre_en = 0
    else:
        for chambre in chambres:
            chambre_nb += chambre.numbre # j'obtient le numbre de chambre deja enregistrer
        purch_number = chambre_nb
        chambre_en = nbchambre - purch_number # je calcul le numbre de chambre qui reste à enregistrer

    if nbcuisine is None:
        cuisine_nb = 0
        cuisine_en = 0
    else:
        for cuisine in cuisines:
            cuisine_nb += cuisine.numbre # j'obtient le numbre de cuisine deja enregistrer
        purcui_number = cuisine_nb
        cuisine_en = nbcuisine - purcui_number # je calcul le numbre de cuisine qui reste à enregistrer

    if nbsalon is None:
        salon_nb = 0
        salon_en = 0
    else:
        for salon in salons:
            salon_nb += salon.numbre # j'obtient le numbre de salon deja enregistrer
        pursa_number = salon_nb
        salon_en = nbsalon - pursa_number # je calcul le numbre de salon qui reste à enregistrer

    if nbdouche is None:
        douche_nb = 0
        douche_en = 0
    else:
        for douche in douches:
            douche_nb += douche.numbre # j'obtient le numbre de douche deja enregistrer
        purdo_number = douche_nb
        douche_en = nbdouche - purdo_number # je calcul le numbre de douche qui reste à enregistrer

    if nbinfrastructure is None:
        infrastructure_nb= 0
        infrastructure_en = 0
    else:
        infrastructure_en = nbinfrastructure - infrastructure_nb # je calcul le numbre de douche qui reste à enregistrer



    if request.method == 'POST' and chambre_en == 0 and cuisine_en == 0 and douche_en == 0 and salon_en == 0 and pp == 0:
        form = Enregistrement2_boutique(request.POST, request.FILES)
        if form.is_valid():
            form = form.save(commit=False)
            fom = form
            fom.statut = 'non occupé'
            fom.house_id = id
            fom.type_id = 1
            form.numbre = 0
            form.insigne_id = 16
            taille = form.image.size/1048576
            tailleUn = form.imageUn.size / 1048576
            tailleDeux = form.imageDeux.size / 1048576
            if taille <= 1.5 or tailleUn <= 1.5 or tailleDeux <= 1.5:
                form.image.name = f'img{d}'
                form.imageUn.name = f'imgUn{d}'
                form.imageDeux.name = f'imgDeux{d}'
                form.statut = mycdb(form.statut)
                form.description = mycdb(form.description)
                fom.save()
                return redirect('camer_house:enregistrement2_ch')
            else:
                messages.error(request, f"la taille de l'image est suppérieur à 1.5Mo. taille actuèlle : {form.image.size/1048576}Mo")
        else:
            messages.error(request,'formulaire non valide') #au cas echeant

    elif request.method == 'POST' and chambre_en > 0:
        form = Enregistrement2_chambre(request.POST, request.FILES)
        if form.is_valid():
            form = form.save(commit=False)
            if form.numbre >= 1 and form.numbre <= chambre_en :
                fom = form
                fom.statut = fom.statut
                fom.house_id = id
                fom.type_id = 1
                taille = form.image.size / 1048576
                tailleUn = form.imageUn.size / 1048576
                tailleDeux = form.imageDeux.size / 1048576
                if taille <= 1.5 or tailleUn <= 1.5 or tailleDeux <= 1.5:
                    if catego != 2 and catego != 3 and catego != 8:
                        form.image.name = f'img{d}'
                        form.imageUn.name = f'imgUn{d}'
                        form.imageDeux.name = f'imgDeux{d}'
                        form.statut = mycdb(form.statut)
                        form.description = mycdb(form.description)
                        fom.save()
                    else:
                        if int(request.POST['montants']) >= 1000:
                            form.statut = mycdb(form.statut)
                            form.description = mycdb(form.description)
                            form.image.name = f'img{d}'
                            form.imageUn.name = f'imgUn{d}'
                            form.imageDeux.name = f'imgDeux{d}'
                            fom.save()
                            compo = Composition.objects.filter(house_id=fom.house_id)
                            for id_c in compo:
                                idc = id_c.id
                                nb = id_c.numbre
                                insig = id_c.insigne.type
                            Composition.objects.filter(id = idc).update(montants = request.POST['montants'])
                            i=1
                            while i <= nb:
                                d = time.time()
                                ChambreUniv.objects.create(insigne=insig+str(i), date = d, composition_id=idc, etat= 1 )
                                i = i+1


                        else:
                            messages.error(request, f"le montant doit être supérieur à 1000")
                    return redirect('camer_house:enregistrement2_ch')
                else:
                    messages.error(request, f"la taille de l'image est suppérieur à 1.5Mo. taille actuèlle : {form.image.size/1048576}Mo")
            else:
                messages.error(request,f'le numbre de chambre doit être inférieur ou égale à {chambre_en}')
        else:
            messages.error(request, f'le formulaire est non valide')


    elif request.method == 'POST' and cuisine_en > 0:
        form = Enregistrement2_chambre(request.POST, request.FILES)
        if form.is_valid():
            form = form.save(commit=False)
            if form.numbre >= 1 and form.numbre <= cuisine_en:
                fom = form
                if fom.statut == 'non moderne':
                    fom.statut = 'traditionnel'
                fom.statut = fom.statut
                fom.house_id = id
                fom.type_id = 3
                taille = form.image.size / 1048576
                tailleUn = form.imageUn.size / 1048576
                tailleDeux = form.imageDeux.size / 1048576
                if taille <= 1.5 or tailleUn <= 1.5 or tailleDeux <= 1.5:
                    form.statut = mycdb(form.statut)
                    form.description = mycdb(form.description)
                    form.image.name = f'img{d}'
                    form.imageUn.name = f'imgUn{d}'
                    form.imageDeux.name = f'imgDeux{d}'
                    fom.save()
                    return redirect('camer_house:enregistrement2_ch')
                else:
                    messages.error(request, f"la taille de l'image est suppérieur à 1.5Mo. taille actuèlle : {form.image.size/1048576}Mo")
            else:
                messages.error(request, f"le numbre de cuisine doit être inférieur ou égal à {cuisine_en}")
        else:
            messages.error(request, "le formulaire est non valide")

    elif request.method == 'POST' and douche_en > 0:
        form = Enregistrement2_chambre(request.POST, request.FILES)
        if form.is_valid():
            form = form.save(commit=False)
            if form.numbre >= 1 and form.numbre <= douche_en:
                fom = form
                if fom.statut == 'non moderne':
                    fom.statut = 'traditionnel'
                fom.statut = fom.statut
                fom.house_id = id
                fom.type_id = 4
                taille = form.image.size / 1048576
                tailleUn = form.imageUn.size / 1048576
                tailleDeux = form.imageDeux.size / 1048576
                if taille <= 1.5 or tailleUn <= 1.5 or tailleDeux <= 1.5:
                    form.statut = mycdb(form.statut)
                    form.description = mycdb(form.description)
                    form.image.name = f'img{d}'
                    form.imageUn.name = f'imgUn{d}'
                    form.imageDeux.name = f'imgDeux{d}'
                    fom.save()
                    return redirect('camer_house:enregistrement2_ch')
                else:
                    messages.error(request, f"la taille de l'image est suppérieur à 1.5Mo. taille actuèlle : {form.image.size/1048576}Mo")
            else:
                messages.error(request, f'le numbre de douche doit être inférieur ou égale à {douche_en}')
        else:
            messages.error(request, f'le formulaire est non valide')
    elif request.method == 'POST' and salon_en > 0:
        form = Enregistrement2_chambre(request.POST, request.FILES)
        if form.is_valid():
            form = form.save(commit=False)
            if form.numbre >= 1 and form.numbre <= salon_en:
                fom = form
                fom.statut = ' '
                fom.house_id = id
                fom.type_id = 2
                taille = form.image.size / 1048576
                tailleUn = form.imageUn.size / 1048576
                tailleDeux = form.imageDeux.size / 1048576
                if taille <= 1.5 or tailleUn <= 1.5 or tailleDeux <= 1.5:
                    form.description = mycdb(form.description)
                    form.image.name = f'img{d}'
                    form.imageUn.name = f'imgUn{d}'
                    form.imageDeux.name = f'imgDeux{d}'
                    fom.save()
                    return redirect('camer_house:enregistrement2_ch')
                else:
                    messages.error(request,
                                   f"la taille de l'image est suppérieur à 1.5Mo. taille actuèlle : {form.image.size/1048576}Mo")
            else:
                messages.error(request, f'le numbre de salon doit être inférieur ou égale à {salon_en}')
        else:
            messages.error(request, f'le formulaire est non valide')
    elif request.method == 'POST' and infrastructure_en > 0:
        form = Enregistrement_infrastruture(request.POST, request.FILES)
        if form.is_valid():
            form = form.save(commit=False)
            form.house_id = id
            taille = form.image.size / 1048576
            tailleUn = form.imageUn.size / 1048576
            tailleDeux = form.imageDeux.size / 1048576
            if taille <= 1.5 or tailleUn <= 1.5 or tailleDeux <= 1.5:
                form.description = mycdb(form.description)
                form.image.name = f'img{d}'
                form.imageUn.name = f'imgUn{d}'
                form.imageDeux.name = f'imgDeux{d}'
                form.save()
                return redirect('camer_house:enregistrement2_ch')
            else:
                messages.error(request,f"la taille de l'image est suppérieur à 1.5Mo. taille actuèlle : {form.image.size/1048576}Mo")

        else:
            messages.error(request, f"le numbre d'infrastructure doit être inférieur ou égale à {infrastructure_en}")

    elif chambre_en == 0 and cuisine_en == 0 and douche_en == 0 and salon_en == 0 and infrastructure_en == 0 and etat == 0 and pp ==1: #si tout est enregisgter, on passe a la page de confirmation
        with connection.cursor() as cursor:
            cursor.execute("Update camhouse_house SET etat = 1 WHERE id = %s ", [int(id)])
            row = cursor.fetchone()
            return redirect('camer_house:proprieter_ch')


    if chambre_en > 0:
        form_m = Montant_Chambre()
        form = Enregistrement2_chambre()
    elif salon_en > 0:
        form = Enregistrement2_chambre()
        form_m = 0
    elif cuisine_en > 0:
        form = Enregistrement2_chambre()
        form_m = 0
    elif douche_en > 0:
        form = Enregistrement2_chambre()
        form_m = 0
    elif infrastructure_en > 0:
        form = Enregistrement_infrastruture()
        form_m = 0
    elif catego == 9 and pp == 0:
        form = Enregistrement2_chambre()
        form_m = 0
    else:
        return redirect('camer_house:liste_category_un')

    context = {
        'montant': montant,
        'has_perm': has_perm,
#        'chambre_a_duppliques':chambre_a_duppliques,
        'form': form,
        'formCompte': formCompte,
        'form_m': form_m,
        'infrastructure_en': infrastructure_en,
        'chambre_en': chambre_en,
        'cuisine_en': cuisine_en,
        'salon_en': salon_en,
        'douche_en': douche_en,
        'nbchambre': nbchambre,
        'nbcuisine': nbcuisine,
        'nbsalon': nbsalon,
        'nbdouche': nbdouche,
        'nbinfrastructure': nbinfrastructure,
        'sategory': sategory,
        'catego' : catego,
        'idh': id,
        'maisons':maisons,
    }

    return render(request,'enregistrement2.html', context=context)

def enregistrement22(request, id):
    chambre_univ = []
    test = get_object_or_404(House, pk=id)# renvoi ereur 404 si category n'existe pas
    nbRU = ChambreUniv.objects.filter(composition__house_id=id, etat= 2).count()
    nbLU = ChambreUniv.objects.filter(composition__house_id=id, etat= 1).count()
    nbOU = ChambreUniv.objects.filter(composition__house_id=id, etat= 3).count()
    has_perm = False
    formCompte = CompteUser()
    iopo = id
    d = time.time()
    sategory = Category.objects.order_by('id').all()
    ancien = Compte.objects.filter(user_id=request.user)
    for montants in ancien:
        montant = montants.montant
        idC = montants.id

    if request.method == 'POST':
        if request.POST['montant'] == "":
            print("operation anulée")
        elif float(request.POST['montant']) <= 0:
            print("opération anulée")

        elif float(request.POST['montant']) > 0:
            montant = montant + float(request.POST['montant'])
            Compte.objects.filter(user_id=request.user).update(montant=montant)
        else:
            print("operation impossible")

        if request.POST['proprietaire'] == "" or request.POST['puol'] == "" or request.POST['montant'] == 0:
            print("restoration annulé")

        elif int(request.POST['proprietaire']) <= 0 or int(request.POST['puol']) <= 0 or request.POST['montant'] == 0:
            print("donné erone")

        elif int(request.POST['proprietaire']) > 0 and int(request.POST['puol']) > 0 and montant >= 1000:
            id = request.POST['puol']
            maison = ChambreUniv.objects.filter(id=id)
            for ids in maison:
                id = ids.id  # je recupère l'id de la maison à supprimr par cet utilisateur
                user_id = ids.composition_id
                etat = ids.etat
            hous_id = Composition.objects.filter(id=user_id)
            for Houss_id in hous_id:
                idddh = Houss_id.house_id
            use = House.objects.filter(id=idddh)
            for me in use:
                usermoi = me.user_id
            if request.user.id == usermoi and etat == 3:
                ChambreUniv.objects.filter(id=id).update(etat=1)
                reservation = OccupationUniv.objects.get(chambre_id=id)
                reservation.delete()
                dos = montant - 1000
                Compte.objects.filter(id=idC).update(montant=dos)
                return redirect("camer_house:proprieter_ch")
            else:
                raise PermissionDenied  # on renvoi la page 403
        else:
            print(f"reservation impossible car {request.POST['proprietaire']} : {request.POST['puol']}")

    idh = House.objects.filter(id = iopo) # je recupère la maison à finalizer(dans se cas elle correspond a l'id reçue dans de lien)
    if not request.user.has_perm("camhouse.add_house") and not request.user.has_perm("camhouse.delete_house") and not request.user.has_perm("camhouse.view_house") and not request.user.has_perm("camhouse.change_house"): #pour savoir s'il est autoriser a ajouter une house
        raise PermissionDenied #on renvoi ver la page 403
    else:
        has_perm = True

    for ids in idh:
        id = ids.id #je recupère l'id de la maison à enregistrer par cet utilisateur
        id_user = ids.user_id
        catego = ids.category_id
    if catego == 8:
        chambre_univ = ChambreUniv.objects.filter(composition__house=id)  # je recupère les ou la ChambreUniv ou l'id de la maison qui est dan
    if id_user != request.user.id:
        raise PermissionDenied #on renvoi ver la page 403
    maisons = House.objects.filter(id=id) # je recupèr tous ls info sur la maison
 #   chambre_a_duppliques = Composition.objects.filter(house=id)
    for maison in maisons: # je recupère les détail de la maison
        nbchambre = maison.nbchambre # je recupère le nombre de chambre
        nbcuisine = maison.nbcuisine # je recupère le nombre de cuisine
        nbsalon = maison.nbsalon # je recupère le nombre de salon
        nbdouche = maison.nbdouche # je recupère le nombre de douche
        nbinfrastructure = maison.nbinfrastructure # je recupère le nombre d'infrstructure
        etat = maison.etat
    chambres = Composition.objects.filter(house_id=id, type=1) # je recupère tous les chambres deja ajoutées
    chambre_nb = 0

    cuisines = Composition.objects.filter(house_id=id, type=3) # je recupère tous les cuisines deja ajoutées
    cuisine_nb = 0

    salons = Composition.objects.filter(house_id=id, type=2) # je recupère tous les salons deja ajoutées
    salon_nb = 0

    douches = Composition.objects.filter(house_id=id, type=4) # je recupère tous les douches deja ajoutées
    douche_nb = 0

    infrastructures = Infrastructure.objects.filter(house_id=id) # je recupère tous les infrastructure deja ajoutées
    infrastructure_nb = infrastructures.count() #nombre d'infrastructure deja renregistrer

    if nbchambre is None:
        chambre_nb = 0
        chambre_en = 0
    else:
        for chambre in chambres:
            chambre_nb += chambre.numbre # j'obtient le numbre de chambre deja enregistrer
        purch_number = chambre_nb
        chambre_en = nbchambre - purch_number # je calcul le numbre de chambre qui reste à enregistrer

    if nbcuisine is None:
        cuisine_nb = 0
        cuisine_en = 0
    else:
        for cuisine in cuisines:
            cuisine_nb += cuisine.numbre # j'obtient le numbre de cuisine deja enregistrer
        purcui_number = cuisine_nb
        cuisine_en = nbcuisine - purcui_number # je calcul le numbre de cuisine qui reste à enregistrer

    if nbsalon is None:
        salon_nb = 0
        salon_en = 0
    else:
        for salon in salons:
            salon_nb += salon.numbre # j'obtient le numbre de salon deja enregistrer
        pursa_number = salon_nb
        salon_en = nbsalon - pursa_number # je calcul le numbre de salon qui reste à enregistrer

    if nbdouche is None:
        douche_nb = 0
        douche_en = 0
    else:
        for douche in douches:
            douche_nb += douche.numbre # j'obtient le numbre de douche deja enregistrer
        purdo_number = douche_nb
        douche_en = nbdouche - purdo_number # je calcul le numbre de douche qui reste à enregistrer

    if nbinfrastructure is None:
        infrastructure_nb= 0
        infrastructure_en = 0
    else:
        infrastructure_en = nbinfrastructure - infrastructure_nb # je calcul le numbre de douche qui reste à enregistrer

    if catego == 9:
        boutik = Composition.objects.filter(house_id=id) # je verifi si la boutique est deja enregistrer
        pp = boutik.count()
    else:
        pp = 1


    if request.method == 'POST' and chambre_en == 0 and cuisine_en == 0 and douche_en == 0 and salon_en == 0 and pp == 0:
        form = Enregistrement2_boutique(request.POST, request.FILES)
        if form.is_valid():
            form = form.save(commit=False)
            form = form
            form.statut = 'non occupé'
            form.house_id = id
            form.type_id = 1
            form.numbre = 0
            form.insigne_id = 16
            taille = form.image.size / 1048576
            tailleUn = form.imageUn.size / 1048576
            tailleDeux = form.imageDeux.size / 1048576
            if taille <= 1.5 or tailleUn <= 1.5 or tailleDeux <= 1.5:
                form.statut = mycdb(form.statut)
                form.description = mycdb(form.description)
                form.image.name = f'img{d}'
                form.imageUn.name = f'imgUn{d}'
                form.imageDeux.name = f'imgDeux{d}'
                form.save()
                return redirect('camer_house:enregistrement22_ch', id)
            else:
                messages.error(request, f"la taille de l'image est suppérieur à 1.5Mo. taille actuèlle : {fom.image.size/1048576}Mo")

        else:
            messages.error(request, f"formulaire non valide")
    elif request.method == 'POST' and chambre_en > 0:
        form = Enregistrement2_chambre(request.POST, request.FILES)
        if form.is_valid():
            form = form.save(commit=False)
            if form.numbre >= 1 and form.numbre <= chambre_en:
                fom = form
                fom.statut = fom.statut
                fom.house_id = id
                fom.type_id = 1
                taille = form.image.size / 1048576
                tailleUn = form.imageUn.size / 1048576
                tailleDeux = form.imageDeux.size / 1048576
                if taille <= 1.5 or tailleUn <= 1.5 or tailleDeux <= 1.5:
                    if catego != 2 and catego != 3 and catego != 8:
                        form.statut = mycdb(form.statut)
                        form.description = mycdb(form.description)
                        form.image.name = f'img{d}'
                        form.imageUn.name = f'imgUn{d}'
                        form.imageDeux.name = f'imgDeux{d}'
                        fom.save()
                    else:
                        if int(request.POST['montants']) >= 1000:
                            form.statut = mycdb(form.statut)
                            form.description = mycdb(form.description)
                            form.image.name = f'img{d}'
                            form.imageUn.name = f'imgUn{d}'
                            form.imageDeux.name = f'imgDeux{d}'
                            fom.save()
                            compo = Composition.objects.filter(house_id=fom.house_id)
                            for id_c in compo:
                                idc = id_c.id
                                nb = id_c.numbre
                                jojo = id_c.numbre
                                insig = id_c.insigne.type
                                insigid = id_c.insigne_id
                            Composition.objects.filter(id=idc).update(montants=request.POST['montants'])

                            testCompo = Composition.objects.filter(house_id=fom.house_id, insigne_id= insigid )
                            if testCompo:
                                i = 0
                                for db in testCompo:
                                    i += db.numbre
                                nb = i
                                i = nb - jojo + 1
                            else:
                                i= 1
                            while i <= nb:
                                d = time.time()
                                ChambreUniv.objects.create(insigne=insig + str(i), date=d, composition_id=idc, etat=1)
                                i = i + 1

                    return redirect('camer_house:enregistrement22_ch', id)
                else:
                    messages.error(request,f"la taille de l'image est suppérieur à 1.5Mo. taille actuèlle : {form.image.size/1048576}Mo")
            else:
                messages.error(request, f'le numbre de chambre doit être inférieur ou égale à {chambre_en}')
        else:
            messages.error(request, f'le formulaire est non valide')


    elif request.method == 'POST' and cuisine_en > 0:
        form = Enregistrement2_chambre(request.POST, request.FILES)
        if form.is_valid():
            form = form.save(commit=False)
            if form.numbre >= 1 and form.numbre <= cuisine_en:
                fom = form
                if fom.statut == 'non moderne':
                    fom.statut = 'traditionnel'
                fom.statut = fom.statut
                fom.house_id = id
                fom.type_id = 3
                taille = fom.image.size / 1048576
                tailleUn = form.imageUn.size / 1048576
                tailleDeux = form.imageDeux.size / 1048576
                if taille <= 1.5 or tailleUn <= 1.5 or tailleDeux <= 1.5:
                    form.statut = mycdb(form.statut)
                    form.description = mycdb(form.description)
                    form.image.name = f'img{d}'
                    form.imageUn.name = f'imgUn{d}'
                    form.imageDeux.name = f'imgDeux{d}'
                    fom.save()
                    return redirect('camer_house:enregistrement22_ch', id)
                else:
                    messages.error(request, f"la taille de l'image est suppérieur à 1.5Mo. taille actuèlle : {fom.image.size/1048576}Mo")
            else:
                messages.error(request, f"le numbre de cuisine doit être inférieur ou égal à {cuisine_en}")
        else:
            messages.error(request, "le formulaire est non valide")

    elif request.method == 'POST' and douche_en > 0:
        form = Enregistrement2_chambre(request.POST, request.FILES)
        if form.is_valid():
            form = form.save(commit=False)
            if form.numbre >= 1 and form.numbre <= douche_en:
                fom = form
                if fom.statut == 'non moderne':
                    fom.statut = 'traditionnel'
                fom.statut = fom.statut
                fom.house_id = id
                fom.type_id = 4
                taille = fom.image.size / 1048576
                tailleUn = form.imageUn.size / 1048576
                tailleDeux = form.imageDeux.size / 1048576
                if taille <= 1.5 or tailleUn <= 1.5 or tailleDeux <= 1.5:
                    form.statut = mycdb(form.statut)
                    form.description = mycdb(form.description)
                    form.image.name = f'img{d}'
                    form.imageUn.name = f'imgUn{d}'
                    form.imageDeux.name = f'imgDeux{d}'
                    fom.save()
                    return redirect('camer_house:enregistrement22_ch', id)
                else:
                    messages.error(request, f"la taille de l'image est suppérieur à 1.5Mo. taille actuèlle : {fom.image.size/1048576}Mo")
            else:
                messages.error(request, f'le numbre de douche doit être inférieur ou égale à {douche_en}')
        else:
            messages.error(request, 'formulaire non valide')
    elif request.method == 'POST' and salon_en > 0:
        form = Enregistrement2_chambre(request.POST, request.FILES)
        if form.is_valid():
            form = form.save(commit=False)
            if form.numbre >= 1 and form.numbre <= salon_en:
                fom = form
                fom.statut = ' '
                fom.house_id = id
                fom.type_id = 2
                taille = fom.image.size / 1048576
                tailleUn = form.imageUn.size / 1048576
                tailleDeux = form.imageDeux.size / 1048576
                if taille <= 1.5 or tailleUn <= 1.5 or tailleDeux <= 1.5:
                    form.description = mycdb(form.description)
                    form.image.name = f'img{d}'
                    form.imageUn.name = f'imgUn{d}'
                    form.imageDeux.name = f'imgDeux{d}'
                    fom.save()
                    return redirect('camer_house:enregistrement22_ch', id)
                else:
                    messages.error(request,f"la taille de l'image est suppérieur à 1.5Mo. taille actuèlle : {fom.image.size/1048576}Mo")
            else:
                messages.error(request, f'le numbre de salon doit être inférieur ou égale à {salon_en}')
        else:
            messages.error(request, 'formulaire non valide')
    elif request.method == 'POST' and infrastructure_en > 0:
        form = Enregistrement_infrastruture(request.POST, request.FILES)
        if form.is_valid():
            form = form.save(commit=False)
            form.house_id = id
            taille = form.image.size / 1048576
            tailleUn = form.imageUn.size / 1048576
            tailleDeux = form.imageDeux.size / 1048576
            if taille <= 1.5 or tailleUn <= 1.5 or tailleDeux <= 1.5:
                form.description = mycdb(form.description)
                form.image.name = f'img{d}'
                form.imageUn.name = f'imgUn{d}'
                form.imageDeux.name = f'imgDeux{d}'
                form.save()
                return redirect('camer_house:enregistrement22_ch', id)
            else:
                messages.error(request, f"la taille de l'image est suppérieur à 1.5Mo. taille actuèlle : {form.image.size/1048576}Mo")
        else:
            messages.error(request, f"le numbre d'infrastructure doit être inférieur ou égale à {infrastructure_en}")

    elif request.method == 'POST' and etat == 0: # methode reserver a la confirmation de la maison ( mêttre l'état a 1)
        etats = 1
        id = request.POST["id"]
        if int(id) == int(iopo):
            puol = House.objects.filter(id=id)
            for cam in puol:
                user = cam.user_id
        else:
            redirect('camer_house:liste_category_un') #ici cest pour erreur 404
        id = int(id)
        for category_puol in puol:
            number_category = category_puol.category_id
        if user == request.user.id:
            with connection.cursor() as cursor:
                cursor.execute("Update camhouse_house SET etat = 1 WHERE id = %s ", [int(id)])
                row = cursor.fetchone()
                return redirect('camer_house:proprieter_ch')
    elif chambre_en == 0 and cuisine_en == 0 and douche_en == 0 and salon_en == 0 and infrastructure_en == 0 and etat != 1:
        #si tout est enregisgter, on passe a la page de confirmation
        purch_number = 0
        purd_number = 0
        purcu_number = 0
        purs_number = 0
        sategory = Category.objects.order_by('id').all()
        detail = House.objects.filter(id=id)
        for infra in detail:
            nbinfra = infra.nbinfrastructure  # je recupère le numbre d'infrastructure à enregistrer
            nbchTotal = infra.nbchambre  # je recupère le numbre de chambre à enregistrer
            nbcuTotal = infra.nbcuisine  # je recupère le numbre de cuisine à enregistrer
            nbdoTotal = infra.nbdouche  # je recupère le numbre de douche à enregistrer
            nbsaTotal = infra.nbsalon  # je recupère le numbre de salon à enregistrer
        if nbinfra is None:
            nbinfra = 0
        infrastructures = Infrastructure.objects.filter(house_id=id)
        if nbsaTotal is None:
            nbsaTotal = 0
        if nbchTotal is None:
            nbchTotal = 0
        if nbcuTotal is None:
            nbcuTotal = 0
        if nbdoTotal is None:
            nbdoTotal = 0
        purin_number = infrastructures.count()  # je recupère le numbre d'infrastructure enredistrer
        chambres = Composition.objects.filter(house_id=id, type_id=1)  # je recupère le numbre de chambre enredistrer
        for nbch in chambres:
            purch_number += nbch.numbre
        douches = Composition.objects.filter(house_id=id, type_id=4)  # je recupère le numbre de douche enredistrer
        for nbd in douches:
            purd_number += nbd.numbre
        cuisines = Composition.objects.filter(house_id=id, type_id=3)  # je recupère le numbre de cuisine enredistrer
        for nbcu in cuisines:
            purcu_number += nbcu.numbre
        salons = Composition.objects.filter(house_id=id, type_id=2)  # je recupère le numbre de salon enredistrer
        for nbs in salons:
            purs_number += nbs.numbre
        for activech in chambres:  # je recupère le dernier id pour utiliser l\'atribu active dans carrousel au niveau du template
            purch = activech.id
        for activecu in cuisines:
            purcu = activecu.id
        for actived in douches:
            purd = actived.id
        for actives in salons:
            purs = actives.id
        for infrastructur in infrastructures:
            purin = infrastructur.id

        if nbchTotal == 0 or nbchTotal is None:
            purch = 0

        if nbsaTotal == 0 or nbsaTotal is None:
            purs = 0

        if nbdoTotal == 0 or nbdoTotal is None:
            purd = 0

        if nbcuTotal == 0 or nbcuTotal is None:
            purcu = 0
        if purin_number == 0 or purin_number is None:
            purin = 0

        context = {
            'nbRU':     nbRU,
            'nbLU':     nbLU,
            'nbOU':     nbOU,
            'formRestorer': RetorerChambre(),
            'chambre_univ': chambre_univ,
            'has_perm': has_perm,
            'infrastructures': infrastructures,
            'purin': purin,
            'purinn': purin_number,
            'formCompte': formCompte,
            'etat': etat,
            'idh': id,
            'actives': purs,
            'actived': purd,
            'activecu': purcu,
            'activech': purch,
            'details': detail,
            'sategory': sategory,
            'catego' : catego,
            'chambres': chambres,
            'cuisines': cuisines,
            'douches': douches,
            'salons': salons,
            'montant': montant,
        }
        return render(request,'enregistrement3.html', context = context)

    elif etat == 1: # je gere l'affichages des détail dans cette condition
        if request.method == 'POST':
            ch_ch = Composition.objects.filter(id = request.POST['id'])
            if float(request.POST['longeur']) > 0 and float(request.POST['largeur']) > 0 and float(request.POST['hauteur']) > 0 and request.POST['description'] != ' ' :
                ch_ch.update(longeur = request.POST['longeur'], largeur = request.POST['largeur'], hauteur = request.POST['hauteur'], description = mycdb(request.POST['description']))
                messages.success(request, f"modification réussi. ete Mise à jour effectuer avec success")
            else:
                messages.error(request, f"echec de modification . votre {id_cat} n'a pas ete Mise à jour. vérifier vos information")

        purch_number = 0
        purd_number = 0
        purcu_number = 0
        purs_number = 0
        sategory = Category.objects.order_by('id').all()
        detail = House.objects.filter(id=id)
        for infra in detail:
            nbinfra = infra.nbinfrastructure  # je recupère le numbre d'infrastructure à enregistrer
            nbchTotal = infra.nbchambre  # je recupère le numbre de chambre à enregistrer
            nbcuTotal = infra.nbcuisine  # je recupère le numbre de cuisine à enregistrer
            nbdoTotal = infra.nbdouche  # je recupère le numbre de douche à enregistrer
            nbsaTotal = infra.nbsalon  # je recupère le numbre de salon à enregistrer
        if nbinfra is None:
            nbinfra = 0
        infrastructures = Infrastructure.objects.filter(house_id=id)
        if nbsaTotal is None:
            nbsaTotal = 0
        if nbchTotal is None:
            if catego == 9:
                nbchTotal = 1
            else:
                nbchTotal = 0
        if nbcuTotal is None:
            nbcuTotal = 0
        if nbdoTotal is None:
            nbdoTotal = 0
        purin_number = infrastructures.count()  # je recupère le numbre d'infrastructure enredistrer
        chambres = Composition.objects.filter(house_id=id, type_id=1)  # je recupère le numbre de chambre enredistrer
        for nbch in chambres:
            purch_number += nbch.numbre
        douches = Composition.objects.filter(house_id=id, type_id=4)  # je recupère le numbre de douche enredistrer
        for nbd in douches:
            purd_number += nbd.numbre
        cuisines = Composition.objects.filter(house_id=id, type_id=3)  # je recupère le numbre de cuisine enredistrer
        for nbcu in cuisines:
            purcu_number += nbcu.numbre
        salons = Composition.objects.filter(house_id=id, type_id=2)  # je recupère le numbre de salon enredistrer
        for nbs in salons:
            purs_number += nbs.numbre
        for activech in chambres:  # je recupère le dernier id pour utiliser l\'atribu active dans carrousel au niveau du template
            purch = activech.id
        for activecu in cuisines:
            purcu = activecu.id
        for actived in douches:
            purd = actived.id
        for actives in salons:
            purs = actives.id
        for infrastructur in infrastructures:
            purin = infrastructur.id

        if nbchTotal == 0 or nbchTotal is None:
            purch = 0

        if nbsaTotal == 0 or nbsaTotal is None:
            purs = 0

        if nbdoTotal == 0 or nbdoTotal is None:
            purd = 0

        if nbcuTotal == 0 or nbcuTotal is None:
            purcu = 0
        if purin_number == 0 or purin_number is None:
            purin = 0

        form4 = Update_house4()


        context = {
            'nbRU':     nbRU,
            'nbLU':     nbLU,
            'nbOU':     nbOU,
            'formRestorer': RetorerChambre(),
            'chambre_univ': chambre_univ,
            'form4': form4,
            'formCompte': formCompte,
            'infrastructures': infrastructures,
            'purin': purin,
            'purinn': purin_number,
            'has_perm': has_perm,
            'etat': etat,
            'idh': id,
            'actives': purs,
            'actived': purd,
            'activecu': purcu,
            'activech': purch,
            'details': detail,
            'sategory': sategory,
            'montant': montant,
            'catego': catego,
            'chambres': chambres,
            'cuisines': cuisines,
            'douches': douches,
            'salons': salons,
        }
        return render(request, 'enregistrement3.html', context=context)

    if chambre_en > 0:
        form_m = Montant_Chambre()
        form = Enregistrement2_chambre()
    elif salon_en > 0:
        form = Enregistrement2_chambre()
        form_m = 0
    elif cuisine_en > 0:
        form = Enregistrement2_chambre()
        form_m = 0
    elif douche_en > 0:
        form = Enregistrement2_chambre()
        form_m = 0
    elif infrastructure_en > 0:
        form = Enregistrement_infrastruture()
        print(chambre_en)
        form_m = 0
    elif catego == 9 and pp == 0:
        form = Enregistrement2_chambre()
        form_m = 0
    else:
        return redirect('camer_house:liste_category_un')

    context = {
        'nbRU': nbRU,
        'nbLU': nbLU,
        'nbOU': nbOU,
        'chambre_univ': chambre_univ,
        'has_perm': has_perm,
        #        'chambre_a_duppliques':chambre_a_duppliques,
        'form': form,
        'formCompte': formCompte,
        'form_m': form_m,
        'infrastructure_en': infrastructure_en,
        'chambre_en': chambre_en,
        'cuisine_en': cuisine_en,
        'salon_en': salon_en,
        'douche_en': douche_en,
        'nbchambre': nbchambre,
        'nbcuisine': nbcuisine,
        'nbsalon': nbsalon,
        'nbdouche': nbdouche,
        'nbinfrastructure': nbinfrastructure,
        'sategory': sategory,
        'montant': montant,
        'catego': catego,
        'idh': id,
        'maisons': maisons,
    }

    return render(request, 'enregistrement22.html', context=context)

def enregistrement3(request):
    if not request.user.is_authenticated:
        return redirect('login')
    sategory = Category.objects.order_by('id').all()
    print("bbb")
    return  HttpResponse('salut')



# les API
class ListeMaisonViewSet(viewsets.ModelViewSet):
    queryset = House.objects.all()
    serializer_class = ListeMaison

class CompositionViewSet(viewsets.ModelViewSet):
    queryset = Composition.objects.all()
    serializer_class =composition

@api_view(['GET'])
def allCategori(request):
    permission_classes = (IsAuthenticated,)
    categoris = Category.objects.all()
    serialization = Catego(categoris, many=True)
    return Response(serialization.data)

#API AUTH
@api_view(['GET'])
def connexion(request, username, password):
    username = username # on recupère le nom
    pwd = password  # on recupère le password
    user = authenticate(username=username,password=pwd)  # on envoi les données reçus à la methode authenticate importé depuis django.contrib.auth (elle prend en paramettre un username et un password)
    if user is not None:  # si le user exite, on le renvoi à sa page d'aceuil
        login(request, user)  # apres connexion, la fonction login joue le role de SESSION
        return Response('ok')  # page dacceuil du client connecter
    else:
        return Response('false') # on affiche un message derreur

#API AUTH


@api_view(['GET'])
def ListeCategori(request, id):
    liste = House.objects.filter(category_id=id, etat=1)
    serializer = ListeMaison(liste, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def Maison(request, id):
    house = House.objects.filter(id=id)
    serializer = maison(house, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def DetailInfrastructure(request, id):
    detail = Infrastructure.objects.filter(house_id=id)
    serializer = infrastructure(detail, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def DetailHouseCh(request, id):
    detail = Composition.objects.filter(house_id=id, type_id = 1)
    serializer = composition(detail, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def DetailHouseCc(request, id):
    detail = Composition.objects.filter(house_id=id, type_id = 3)
    serializer = composition(detail, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def DetailHouseS(request, id):
    detail = Composition.objects.filter(house_id=id, type_id = 2)
    serializer = composition(detail, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def DetailHouseD(request, id):
    detail = Composition.objects.filter(house_id=id, type_id = 4)
    serializer = composition(detail, many=True)
    return Response(serializer.data)



#API AUTH
class RegiterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data)


    #permission_classes = (IsAuthenticated, ) #si il est permis on gere l'api