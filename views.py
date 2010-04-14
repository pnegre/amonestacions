# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.http import HttpResponse
from django.utils import simplejson

from xml.dom.minidom import parse, parseString

from amonestacions.forms import *
from amonestacions.models import *






def novaAmon(request):
	if request.method == 'POST':
		form = NovaAmonestacioForm(request.POST)
		if form.is_valid():
			form.save()
		
		return render_to_response(
			'amonestacions/novaAmon.html', {
				'ok': True
		} )
	
	form = NovaAmonestacioForm()
	return render_to_response(
			'amonestacions/novaAmon.html', {
				'form': form
	} )

def consultaAmon(request):
	return render_to_response(
			'amonestacions/base.html', {
	} )


def importData(request):
	if request.method == 'POST':
		f = request.FILES['file']
		dom = parse(f)
		
		professors = dom.getElementsByTagName('PROFESSOR')
		for prof in professors:
			p = Professor(
				nom = prof.getAttribute('nom'),
				llinatge1 = prof.getAttribute('ap1'),
				llinatge2 = prof.getAttribute('ap2'),
			)
			p.save()
		
		cursos = dom.getElementsByTagName('CURS')
		for curs in cursos:
			c = Curs(nom=curs.getAttribute('descripcio'))
			c.save()
			
			#grups = curs.getElementsByTagName('GRUP')
			#for grup in grups:
				#g = Grup(
					#nom=grup.getAttribute('descripcio'),
					#curs = c
				#)
				#g.save()
		
		
		#alumnes = dom.getElementsByTagName('ALUMNE')
		#for alumne in alumnes:
			#nom = alumne.getAttribute('nom')
			#l1 = alumne.getAttribute('ap1')
			#l2 = alumne.getAttribute('ap2')
			#exp = alumne.getAttribute('expedient')
			
			#a = Alumne(nom=nom,llinatge1=l1,llinatge2=l2,expedient=exp)
			#a.save()
	
	return render_to_response(
			'amonestacions/import.html', {
	} )


