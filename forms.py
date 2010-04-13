# -*- coding: utf-8 -*-

from django import forms
from amonestacions.models import *

import re


class NovaAmonestacioForm(forms.Form):
	alumne = forms.CharField(widget=forms.TextInput(attrs={'size':'40'}))
	area = forms.ChoiceField()
	tipusAmon = forms.ChoiceField()
	gravetat = forms.ChoiceField()
	descripcio = forms.CharField(widget=forms.Textarea(attrs={'rows': 10, 'cols': 60}))
	
	def __init__(self,*args,**kwrds):
		super(NovaAmonestacioForm,self).__init__(*args,**kwrds)
		self.fields['tipusAmon'].choices = [[x.id,x.nom] for x in TipusAmonestacio.objects.all()]
		self.fields['gravetat'].choices = [[x.id,x.nom] for x in Gravetat.objects.all()]
		self.fields['area'].choices = [[x.id,x.nom] for x in Area.objects.all()]
	
	def save(self):
		data = self.cleaned_data
		
		s = re.search('\[(\d+)\]',data['alumne'])
		exp = s.group(1)
		
		are = Area.objects.filter(id=data['area'])[0]
		tip = TipusAmonestacio.objects.filter(id=data['tipusAmon'])[0]
		gra = Gravetat.objects.filter(id=data['gravetat'])[0]
		alu = Alumne.objects.filter(expedient=exp)[0]
		amonestacio = Amonestacio(
			descripcio = data['descripcio'],
			alumne = alu,
			area = are,
			tipusAmon = tip,
			gravetat = gra
		)
		amonestacio.save()