# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.http import HttpResponse
from django.utils import simplejson

from xml.dom.minidom import parse, parseString

from amonestacions.forms import *
from amonestacions.models import *






def inici(request):
	if request.method == 'POST':
		form = NovaAmonestacioForm(request.POST)
		if form.is_valid():
			form.save()
		
		return render_to_response(
			'amonestacions/index.html', {
				'ok': True
		} )
	
	form = NovaAmonestacioForm()
	return render_to_response(
			'amonestacions/index.html', {
				'form': form
	} )



def importData(request):
	if request.method == 'POST':
		f = request.FILES['file']
		dom = parse(f)
		alumnes = dom.getElementsByTagName('ALUMNE')
		for alumne in alumnes:
			nom = alumne.getAttribute('nom')
			l1 = alumne.getAttribute('ap1')
			l2 = alumne.getAttribute('ap2')
			exp = alumne.getAttribute('expedient')
			
			a = Alumne(nom=nom,llinatge1=l1,llinatge2=l2,expedient=exp)
			a.save()
	
	return render_to_response(
			'amonestacions/import.html', {
	} )


