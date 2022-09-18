from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='profile')
    phonenumber = models.IntegerField()
    day = models.FloatField()
    pay = models.CharField(max_length=50)
    code = models.CharField(max_length=10)

    def __str__(self):
        return self.user.username

class Category(models.Model):
    name=models.CharField(max_length=50)
    def __str__(self):
        return self.name

class Typepayement(models.Model):
    type=models.CharField(max_length=50)
    def __str__(self):
        return self.type

class Compte(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='compte')
    montant = models.FloatField()
    day = models.FloatField()
    def __str__(self):
        return self.user.username

class House(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    type = models.ForeignKey(Typepayement, on_delete=models.CASCADE)
    region = models.CharField(max_length=50)
    arrondissement = models.CharField(max_length=55)
    nbchambre = models.IntegerField(null = True)
    nbsalon = models.IntegerField(null = True)
    nbcuisine = models.IntegerField(null = True)
    nbdouche = models.IntegerField(null = True)
    description = models.TextField()
    image = models.ImageField(upload_to=f'camhouse/house/')
    sommes = models.IntegerField(null= True)
    etat = models.IntegerField(null= True)
    nom = models.CharField(max_length=50, null = True)
    nbinfrastructure = models.IntegerField(null = True) #null et blank sont des attributs permettant de spécifier que le champ peut etre vide dans la bd
    lat = models.FloatField(null=True)
    lng = models.FloatField(null=True)
    date = models.FloatField(null=True)
    pay = models.CharField(max_length=55, null=True)
    def __str__(self):
        return self.user.username

class Reservation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    proprietaire = models.IntegerField()
    house = models.ForeignKey(House, on_delete=models.CASCADE)
    date = models.FloatField()
    def __str__(self):
        return self.house



class Occupation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    proprietaire = models.IntegerField()
    house = models.ForeignKey(House, on_delete=models.CASCADE)
    date = models.FloatField()
    def __str__(self):
        return self.house

class Insigne(models.Model):
    type = models.CharField(max_length=5)
    def __str__(self):
        return self.type

class Infrastructure(models.Model):
    house = models.ForeignKey(House, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=f'camhouse/infrastucture/')
    imageUn = models.ImageField(upload_to=f'camhouse/infrastuctureUn/')
    imageDeux = models.ImageField(upload_to=f'camhouse/infrastuctureDeux/')
    description = models.TextField()
    def __str__(self):
        return self.description

class Typecomposition(models.Model):
    type=models.CharField(max_length=15)
    def __str__(self):
        return self.type

class Composition(models.Model):
    house = models.ForeignKey(House, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=f'camhouse/chambre/')
    imageUn = models.ImageField(upload_to=f'camhouse/chambreUn/', null=True) #en reinitialisant la DB il faut e,lever l'atribut nulll=true
    imageDeux = models.ImageField(upload_to=f'camhouse/chambreDeux/', null=True)
    insigne = models.ForeignKey(Insigne, on_delete=models.CASCADE)
    longeur = models.FloatField()
    largeur = models.FloatField()
    hauteur = models.FloatField()
    montants = models.IntegerField(null=True)
    statut = models.CharField(max_length=15)
    numbre = models.IntegerField()
    description = models.TextField()
    type = models.ForeignKey(Typecomposition, on_delete=models.CASCADE)
    def __str__(self):
        return self.description

class Consultation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='consultation')
    day = models.FloatField()

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    house = models.ForeignKey(House, on_delete=models.CASCADE)
    date = models.FloatField()
    proprietaire = models.CharField(max_length=20, null=True)
    phonenumber = models.IntegerField(null=True)
    def __str__(self):
        return self.house

class ChambreUniv(models.Model):
    composition = models.ForeignKey(Composition, on_delete=models.CASCADE)
    insigne = models.CharField(max_length= 10)
    date = models.FloatField()
    etat = models.IntegerField(null=True)
    def __str__(self):
        return self.composition

class ReservationUniv(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    proprietaire = models.IntegerField()
    chambre = models.ForeignKey(ChambreUniv, on_delete=models.CASCADE)
    date = models.FloatField()
    def __str__(self):
        return self.house

class OccupationUniv(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    proprietaire = models.IntegerField()
    chambre = models.ForeignKey(ChambreUniv, on_delete=models.CASCADE)
    date = models.FloatField()
    def __str__(self):
        return self.house

class Message(models.Model):
    send = models.IntegerField()
    receve = models.ForeignKey(User, on_delete=models.CASCADE)
    sms = models.TextField(null=True)
    date = models.FloatField()
    etat = models.IntegerField()
    house = models.ForeignKey(House, on_delete=models.CASCADE, null=True)
    def __str__(self):
        return self.send