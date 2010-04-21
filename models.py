# -*- coding: utf-8 -*-
from django.db import models

import gestib.models


class Area(models.Model):
	nom = models.CharField(max_length=200)
	
	def __unicode__(self):
		return self.nom



class Gravetat(models.Model):
	nom = models.CharField(max_length=200)
	punts = models.IntegerField()
	
	def __unicode__(self):
		return self.nom


class TipusAmonestacio(models.Model):
	nom = models.CharField(max_length=200)
	
	def __unicode__(self):
		return self.nom



class Amonestacio(models.Model):
	descripcio = models.TextField()
	dataHora = models.DateTimeField(auto_now_add=True)
	
	alumne = models.ForeignKey(gestib.models.Alumne)
	area = models.ForeignKey(Area)
	tipusAmon = models.ForeignKey(TipusAmonestacio)
	gravetat = models.ForeignKey(Gravetat)
	
	
	def __unicode__(self):
		return self.alumne.nom + ' ' + self.gravetat.nom
	


class Activitat(models.Model):
	pass

class TipusActivitat(models.Model):
	pass




