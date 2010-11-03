# -*- coding: utf-8 -*-
from django.db import models

import gestib.models



class Gravetat(models.Model):
	nom = models.CharField(max_length=200)
	punts = models.IntegerField()
	
	def __unicode__(self):
		return self.nom



class Amonestacio(models.Model):
	descripcio = models.TextField()
	dataHora = models.DateTimeField(auto_now_add=True)
	
	alumne = models.ForeignKey(gestib.models.Alumne)
	professor = models.ForeignKey(gestib.models.Professor)
	gravetat = models.ForeignKey(Gravetat)
	
	def __unicode__(self):
		return self.alumne.nom + ' ' + self.gravetat.nom
	
	class Meta:
		permissions = (
			("posar_amonestacions","Pot posar amonestacions"),
		)



class Periode(models.Model):
	descripcio = models.TextField()
	dt1 = models.DateTimeField()
	dt2 = models.DateTimeField()
	
	def __unicode__(self):
		return self.descripcio


class Config(models.Model):
	maxPoints = models.IntegerField()


class InfoGrup(models.Model):
	grup = models.ForeignKey(gestib.models.Grup)
	emailTutor = models.CharField(max_length=200)
	
	def __unicode__(self):
		return unicode(self.grup) + " | " + self.emailTutor


