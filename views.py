# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.http import HttpResponse
from django.utils import simplejson

from xml.dom.minidom import parse, parseString

from amonestacions.forms import *
from amonestacions.models import *






def novaAmon(request):
	ok = False
	if request.method == 'POST':
		form = NovaAmonestacioForm(request.POST)
		if form.is_valid():
			form.save()
			ok = True
		
	
	form = NovaAmonestacioForm()
	return render_to_response(
		'amonestacions/novaAmon.html', {
			'ok': ok,
			'form': form,
	} )





def consultaAmon(request):
	if request.method == 'POST':
		pass
	
	amonList = Amonestacio.objects.all()	
	
	return render_to_response(
			'amonestacions/consulta.html', {
			'amonList': amonList
	} )




def importData(request):
	if request.method == 'POST':
		f = request.FILES['file']
		dom = parse(f)
		
		professors = dom.getElementsByTagName('PROFESSOR')
		for prof in professors:
			p = Professor(
				codi = prof.getAttribute('codi'),
				nom = prof.getAttribute('nom'),
				llinatge1 = prof.getAttribute('ap1'),
				llinatge2 = prof.getAttribute('ap2'),
			)
			p.save()
		
		cursos = dom.getElementsByTagName('CURS')
		for curs in cursos:
			c = Curs(nom=curs.getAttribute('descripcio'),codi=curs.getAttribute('codi'))
			c.save()
			
			grups = curs.getElementsByTagName('GRUP')
			for grup in grups:
				prof = Professor.objects.filter(codi=grup.getAttribute('tutor'))
				if prof == None: continue
				if len(prof) == 0: continue
				
				g = Grup(
					nom = grup.getAttribute('nom'),
					curs = c,
					tutor = prof[0],
					codi = grup.getAttribute('codi'),
				)
				g.save()
		
		
		alumnes = dom.getElementsByTagName('ALUMNE')
		for alumne in alumnes:
			nom = alumne.getAttribute('nom')
			l1 = alumne.getAttribute('ap1')
			l2 = alumne.getAttribute('ap2')
			exp = alumne.getAttribute('expedient')
			gp = Grup.objects.filter(codi=alumne.getAttribute('grup'))
			if gp == None: continue
			if len(gp) == 0: continue
			
			a = Alumne(nom=nom,llinatge1=l1,llinatge2=l2,expedient=exp,grup=gp[0])
			a.save()
	
	return render_to_response(
			'amonestacions/import.html', {
	} )


