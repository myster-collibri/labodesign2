from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.
SEXE=(
	("feminin", "FEMININ"),
	("masculin", "MASCULIN"))

class Vetements(models.Model):
	date=models.DateTimeField(default=timezone.now)
	nom=models.CharField(max_length=500)
	description=models.TextField()
	auteur=models.ForeignKey(User, on_delete=models.CASCADE)
	sexe=models.CharField(max_length=300, choices=SEXE)

	def __str__(self):
		return "{} : {}".format(self.nom, self.sexe)

class VetementsImage(models.Model):
	date=models.DateTimeField(default=timezone.now)
	image=models.ImageField(upload_to="images")
	vetement=models.ForeignKey(Vetements, on_delete=models.CASCADE)

	def __str__(self):
		return self.vetement.nom

class Composants(models.Model):
	date=models.DateTimeField(default=timezone.now)
	nom=models.CharField(max_length=500)
	auteur=models.ForeignKey(User, on_delete=models.CASCADE)
	vetement=models.ForeignKey(Vetements, on_delete=models.CASCADE)
	details=models.CharField(max_length=500)

	def __str__(self):
		return self.nom

class ComposantDesign(models.Model):
	date=models.DateTimeField(default=timezone.now)
	composant=models.ForeignKey(Composants, on_delete=models.CASCADE)
	details=models.TextField()

	def __str__(self):
		return self.composant.nom

class ComposantDesignImage(models.Model):
	date=models.DateTimeField(default=timezone.now)
	image=models.ImageField(upload_to='images')
	composant_design=models.ForeignKey(ComposantDesign, on_delete=models.CASCADE)

	def __str__(self):
		return self.composant_design.details

class CaoModelImage(models.Model):
	image=models.ImageField(upload_to='images')

class Cao(models.Model):
	vetement=models.CharField(max_length=300)
	sexe=models.CharField(max_length=300)
	auteur=models.CharField(max_length=300)
	top_model=models.CharField(max_length=500)

	def __str__(self):
		return self.vetement


class CaoComposant(models.Model):
	cao=models.ForeignKey(Cao, on_delete=models.CASCADE)
	nom=models.CharField(max_length=300)

class CaoImageComposant(models.Model):
	caocomposant=models.ForeignKey(CaoComposant, on_delete=models.CASCADE)
	image_url=models.CharField(max_length=500)



