from django import forms
from .models import *

class Enregistrement(forms.ModelForm):
    region = forms.CharField(widget=forms.TextInput(attrs = {'class': 'form-control', 'placeholder': 'ville, province ou région de localisation(ex: douala'}))
    arrondissement = forms.CharField(widget=forms.TextInput(attrs = {'class': 'form-control', 'placeholder': 'arrondissement d l\'emplacement'}))
    description = forms.CharField(widget=forms.Textarea(attrs = {'class': 'form-control', 'placeholder': 'entrer tout les détails possible pouvant encouragé la location'}))
    sommes = forms.CharField(widget=forms.NumberInput(attrs = {'class': 'form-control', 'placeholder': 'montant de la location', 'min': '1000'}))
    nbchambre = forms.CharField(widget=forms.NumberInput(attrs = {'class': 'form-control', 'placeholder': 'nombre de chambre', 'min': '0'}))
    nbcuisine = forms.CharField(widget=forms.NumberInput(attrs = {'class': 'form-control', 'placeholder': 'nombre de cuisine', 'min': '0'}))
    nbsalon = forms.CharField(widget=forms.NumberInput(attrs = {'class': 'form-control', 'placeholder': 'nombre de salon', 'min': '0'}))
    nbdouche = forms.CharField(widget=forms.NumberInput(attrs = {'class': 'form-control', 'placeholder': 'nombre de douche', 'min': '0'}))
    nbinfrastructure = forms.CharField(widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'nombre d\'infrastructure','title': '(exemple: pui, parking, piscine ect... ) entrez un nombre correspondant au nombre d\'infrastructure', 'min': '0'}))
    class Meta:
        model = House
        fields = ('category','type', 'region', 'arrondissement', 'nbchambre', 'nbsalon', 'nbcuisine', 'nbdouche', 'description', 'image', 'sommes', 'nbinfrastructure', 'etat', 'date', 'lat', 'lng', 'pay',)
        widgets = {
            'category': forms.HiddenInput(attrs = {'value': '1'}),
            'etat': forms.HiddenInput(attrs={'value': '0'}),
            'pay': forms.HiddenInput(attrs={'value': '0'}),
            'date': forms.HiddenInput(attrs={'value': '0'}),
            'lat': forms.HiddenInput(attrs={'value': '0'}),
            'lng': forms.HiddenInput(attrs={'value': '0'}),
            'type': forms.Select(attrs = {'class': 'form-control'}),
        }

class Enregistrement_Hotel(forms.ModelForm):
    region = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'ville, province ou région de localisation(ex: douala'}))
    arrondissement = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    nom = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'enter le nom'}))
    description = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control','placeholder': 'entrer tout les détails possible pouvant encouragé la location'}))
    nbchambre = forms.CharField(widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'nombre de chambre', 'min': '0'}))
    nbinfrastructure = forms.CharField(widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'nombre d\'infrastructure', 'min': '0'}))
    class Meta:
        model = House
        fields = ('category','region', 'arrondissement', 'type','nbchambre', 'nbinfrastructure', 'description', 'image', 'nom', 'etat','pay',)
        widgets = {
            'category': forms.HiddenInput(attrs = {'value': '2'}),
            'type': forms.Select(attrs = {'class': 'form-control'}),
            'etat': forms.HiddenInput(attrs={'value': '0'}),
            'pay': forms.HiddenInput(attrs={'value': '0'}),
        }

class Montant_Chambre(forms.ModelForm):
    montants = forms.CharField(widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'montant de la location', 'min': '1000'}))
    class Meta:
        model = Composition
        fields = ('montants', )

class CompteUser(forms.ModelForm):
    montant = forms.FloatField(widget=forms.NumberInput(attrs = { 'min': '1', 'class': 'form-control', 'placeholder': 'charger votre compte'} ))
    class Meta:
        model = Compte
        fields = ('montant', 'day')
        widgets = {
            'day': forms.HiddenInput(attrs={'value': '1'}),
        }

class ReservePuol(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ('proprietaire',)
        widgets = {
            'proprietaire': forms.HiddenInput(attrs={'value': '1'}),
        }

class ReserveChambre(forms.ModelForm):
    class Meta:
        model = ReservationUniv
        fields = ('proprietaire',)
        widgets = {
            'proprietaire': forms.HiddenInput(attrs={'value': '1'}),
        }

class RetorerPuol(forms.ModelForm):
    class Meta:
        model = Occupation
        fields = ('proprietaire',)
        widgets = {
            'proprietaire': forms.HiddenInput(attrs={'value': '1'}),
        }

class RetorerChambre(forms.ModelForm):
    class Meta:
        model = OccupationUniv
        fields = ('proprietaire',)
        widgets = {
            'proprietaire': forms.HiddenInput(attrs={'value': '1'}),
        }

class Enregistrement_Boutique(forms.ModelForm):
    region = forms.CharField(widget=forms.TextInput(attrs = {'class': 'form-control', 'placeholder': 'ville, province ou région de localisation(ex: douala'}))
    arrondissement = forms.CharField(widget=forms.TextInput(attrs = {'class': 'form-control', 'placeholder': 'arrondissement d l\'emplacement'}))
    description = forms.CharField(widget=forms.Textarea(attrs = {'class': 'form-control', 'placeholder': 'entrer tout les détails possible pouvant encouragé la location'}))
    sommes = forms.CharField(widget=forms.NumberInput(attrs = {'class': 'form-control', 'placeholder': 'montant de la location', 'min': '1000'}))
    class Meta:
        model = House
        fields = ('category', 'type', 'region', 'arrondissement',  'sommes', 'image', 'description', 'etat', 'pay',)
        widgets = {
            'category': forms.HiddenInput(attrs={'value': '9'}),
            'etat': forms.HiddenInput(attrs={'value': '0'}),
            'pay': forms.HiddenInput(attrs={'value': '0'}),
            'type': forms.Select(attrs={'class': 'form-control'}),
        }

class Enregistrement_citee_universtaire(forms.ModelForm):
    class Meta:
        model = House
        fields = ('category', 'type', 'region', 'arrondissement',  'sommes', 'nbdouche', 'sommes')

class Enregistrement2_chambre(forms.ModelForm):
    statut = forms.CharField(widget=forms.HiddenInput(attrs = {'value': 'non occupé'}))
    longeur = forms.FloatField(widget=forms.NumberInput(attrs = { 'min': '1', 'class': 'form-control'} ))
    largeur = forms.FloatField(widget=forms.NumberInput(attrs = { 'min': '1', 'class': 'form-control'} ))
    hauteur = forms.FloatField(widget=forms.NumberInput(attrs = { 'min': '1', 'class': 'form-control'} ))
    description = forms.CharField(widget=forms.Textarea(attrs = {'class': 'form-control', 'placeholder': 'entrer tout les détails présents pouvant encouragé la location'}))
    numbre = forms.CharField(widget=forms.NumberInput(attrs = {'min': '1', 'class': 'form-control', 'placeholder': 'entrer le numbre similaire à celle ci', 'title': 'combien sont similaire à celle ci pour un enregistrement rapide'}))
    class Meta:
        model = Composition
        fields = ('statut', 'longeur', 'largeur', 'hauteur', 'description', 'image', 'insigne', 'numbre', 'imageUn', 'imageDeux')
        widgets= {
            'insigne': forms.Select(attrs={'class': 'form-control'}),

        }

class Enregistrement2_boutique(forms.ModelForm):
    statut = forms.CharField(widget=forms.HiddenInput(attrs = {'value': 'non occupé'}))
    longeur = forms.FloatField(widget=forms.NumberInput(attrs = { 'min': '1', 'class': 'form-control'} ))
    largeur = forms.FloatField(widget=forms.NumberInput(attrs = { 'min': '1', 'class': 'form-control'} ))
    hauteur = forms.FloatField(widget=forms.NumberInput(attrs = { 'min': '1', 'class': 'form-control'} ))
    description = forms.CharField(widget=forms.Textarea(attrs = {'class': 'form-control', 'placeholder': 'entrer tout les détails présents pouvant encouragé la location'}))
    class Meta:
        model = Composition
        fields = ('statut', 'longeur', 'largeur', 'hauteur', 'description', 'image', 'imageUn', 'imageDeux')

class Enregistrement_infrastruture(forms.ModelForm):
    description = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'entrer tout les détails présents pouvant encouragé la location exemple: parking 25 m / 10 m ou terrasse 2m /5m ou piscine .....'}))
    class Meta:
        model = Infrastructure
        fields = {'description', 'image', 'imageUn','imageDeux'}

class Update_house1(forms.ModelForm):
    region = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'ville, province ou région de localisation(ex: douala'}))
    arrondissement = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'arrondissement d l\'emplacement'}))
    description = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'entrer tout les détails possible pouvant encouragé la location'}))
    sommes = forms.CharField(widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'montant de la location', 'min': '1000'}))
    nbchambre = forms.CharField(widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'nombre de chambre', 'min': '0'}))
    nbcuisine = forms.CharField(widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'nombre de cuisine', 'min': '0'}))
    nbsalon = forms.CharField(widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'nombre de salon', 'min': '0'}))
    nbdouche = forms.CharField(widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'nombre de douche', 'min': '0'}))
    nbinfrastructure = forms.CharField(widget=forms.NumberInput( attrs={'class': 'form-control', 'placeholder': 'nombre d\'infrastructure','title': '(exemple: pui, parking, piscine ect... ) entrez un nombre correspondant au nombre d\'infrastructure', 'min': '0'}))

    class Meta:
        model = House
        fields = ( 'region', 'arrondissement', 'nbchambre', 'nbsalon', 'nbcuisine', 'nbdouche', 'description', 'sommes', 'nbinfrastructure')

class Update_house3(forms.ModelForm):
    region = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'ville, province ou région de localisation(ex: douala'}))
    arrondissement = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'arrondissement d l\'emplacement'}))
    nom = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'dite comment seras appeller votre structure'}))
    description = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control','placeholder': 'entrer tout les détails possible pouvant encouragé la location'}))
    sommes = forms.CharField(widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'montant de la location', 'min': '1000'}))
    nbchambre = forms.CharField(widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'nombre de chambre', 'min': '0'}))
    nbinfrastructure = forms.CharField(widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'nombre d\'infrastructure', 'min': '0'}))
    class Meta:
        model = House
        fields = ('region', 'arrondissement','nbchambre', 'nbinfrastructure', 'sommes', 'description', 'nom')

class Update_house4(forms.ModelForm):
    longeur = forms.FloatField(widget=forms.NumberInput(attrs={'min': '1', 'class': 'form-control'}))
    largeur = forms.FloatField(widget=forms.NumberInput(attrs={'min': '1', 'class': 'form-control'}))
    hauteur = forms.FloatField(widget=forms.NumberInput(attrs={'min': '1', 'class': 'form-control'}))
    description = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'entrer tout les détails présents pouvant encouragé la location'}))

    class Meta:
        model = Composition
        fields = ('longeur', 'largeur', 'hauteur', 'description', )

class Update_house2(forms.ModelForm):
    region = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'ville, province ou région de localisation(ex: douala'}))
    arrondissement = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'arrondissement d l\'emplacement'}))
    description = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'entrer tout les détails possible pouvant encouragé la location'}))
    sommes = forms.CharField(widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'montant de la location', 'min': '1000'}))

    class Meta:
        model = House
        fields = ('region', 'arrondissement', 'sommes', 'description')
