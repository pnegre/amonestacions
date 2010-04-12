# -*- coding: utf-8 -*-
from django.db import models


class Area(models.Model):
	nom = models.CharField(max_length=200)



class Gravetat(models.Model):
	nom = models.CharField(max_length=200)


class TipusAmonestacio(models.Model):
	nom = models.CharField(max_length=200)


class Alumne(models.Model):
	nom = models.CharField(max_length=200)
	llinatge1 = models.CharField(max_length=200)
	llinatge2 = models.CharField(max_length=200)
	

class Amonestacio(models.Model):
	descripcio = models.TextField()
	
	alumne = models.ForeignKey(Alumne)
	area = models.ForeignKey(Area)
	tipusAmon = models.ForeignKey(TipusAmonestacio)
	gravetat = models.ForeignKey(Gravetat)
	


class Activitat(models.Model):
	pass

class TipusActivitat(models.Model):
	pass


