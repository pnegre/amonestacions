# -*- coding: utf-8 -*-
from django.db import models




class Curs(models.Model):
	nom = models.CharField(max_length=200)
	codi = models.CharField(max_length=200)
	
	def __unicode__(self):
		return self.nom





class Professor(models.Model):
	nom = models.CharField(max_length=200)
	llinatge1 = models.CharField(max_length=200)
	llinatge2 = models.CharField(max_length=200)
	codi = models.CharField(max_length=200)
	
	def __unicode__(self):
		return  self.llinatge1 + ' ' + self.llinatge2 + ', ' + self.nom


class Grup(models.Model):
	nom = models.CharField(max_length=200)
	codi = models.CharField(max_length=200)
	
	tutor = models.ForeignKey(Professor)
	curs = models.ForeignKey(Curs)
	
	def __unicode__(self):
		return self.curs.nom + " " + self.nom


class Alumne(models.Model):
	nom = models.CharField(max_length=200)
	llinatge1 = models.CharField(max_length=200)
	llinatge2 = models.CharField(max_length=200)
	expedient = models.CharField(max_length=200)
	
	grup = models.ForeignKey(Grup)
	
	def __unicode__(self):
		return self.llinatge1 + ' ' + self.llinatge2 + ', ' + self.nom




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
	
	alumne = models.ForeignKey(Alumne)
	area = models.ForeignKey(Area)
	tipusAmon = models.ForeignKey(TipusAmonestacio)
	gravetat = models.ForeignKey(Gravetat)
	
	
	def __unicode__(self):
		return self.alumne.nom + ' ' + self.gravetat.nom
	


class Activitat(models.Model):
	pass

class TipusActivitat(models.Model):
	pass




