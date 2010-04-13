# -*- coding: utf-8 -*-

from django import forms
from amonestacions.models import *


class NovaAmonestacioForm(forms.Form):
	alumne = forms.CharField()
	area = forms.ChoiceField()
	tipusAmon = forms.ChoiceField()
	gravetat = forms.ChoiceField()
	descripcio = forms.CharField(widget=forms.Textarea(attrs={'rows': 10, 'cols': 60}))
	
	def __init__(self,*args,**kwrds):
		super(NovaAmonestacioForm,self).__init__(*args,**kwrds)
		self.fields['tipusAmon'].choices = [[x.id,x.nom] for x in TipusAmonestacio.objects.all()]
		self.fields['gravetat'].choices = [[x.id,x.nom] for x in Gravetat.objects.all()]
		self.fields['area'].choices = [[x.id,x.nom] for x in Area.objects.all()]