# -*- coding: utf-8 -*-

from django import forms
from amonestacions.models import *
from gestib.models import *

import re, datetime

import aux



class NovaAmonestacioForm(forms.Form):
	alumne = forms.CharField(widget=forms.TextInput(attrs={'size':'40'}))
	gravetat = forms.ChoiceField()
	profe = forms.ChoiceField()
	descripcio = forms.CharField(widget=forms.Textarea(attrs={'rows': 10, 'cols': 60}))
	
	def __init__(self,*args,**kwrds):
		super(NovaAmonestacioForm,self).__init__(*args,**kwrds)
		self.fields['gravetat'].choices = [[x.id,x.nom] for x in Gravetat.objects.all()]
		self.fields['profe'].choices = [[x.codi,x] for x in Professor.objects.all()]
	
	def save(self):
		data = self.cleaned_data
		
		s = re.search('\[(\d+)\]',data['alumne'])
		exp = s.group(1)
		
		gra = Gravetat.objects.filter(id=data['gravetat'])[0]
		alu = Alumne.objects.filter(expedient=exp)[0]
		prof = Professor.objects.filter(codi=data['profe'])[0]
		amonestacio = Amonestacio(
			descripcio = data['descripcio'],
			alumne = alu,
			gravetat = gra,
			professor = prof,
		)
		amonestacio.save()
		self.amonestacio = amonestacio



class ConsultaAmonForm(forms.Form):
	periode = forms.ChoiceField()
	grup = forms.ChoiceField()
	
	def __init__(self,*args,**kwrds):
		super(ConsultaAmonForm,self).__init__(*args,**kwrds)
		self.fields['grup'].choices = [[x.id,unicode(x)] for x in Grup.objects.all()]
		self.fields['grup'].choices.insert(0,[-1,'TOTS'])
		self.fields['periode'].choices = [[x.id,unicode(x)] for x in Periode.objects.all()]
		x = aux.periodeActual()
		if x is not None:
			self.fields['periode'].initial = x.id



class ConsultaAmonAlumneForm(forms.Form):
	alumne = forms.CharField(widget=forms.TextInput(attrs={'size':'40'}))
	periode = forms.ChoiceField()
	
	def __init__(self,*args,**kwrds):
		super(ConsultaAmonAlumneForm,self).__init__(*args,**kwrds)
		self.fields['periode'].choices = [[x.id,unicode(x)] for x in Periode.objects.all()]
		x = aux.periodeActual()
		if x is not None:
			self.fields['periode'].initial = x.id



