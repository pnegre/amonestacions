# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.http import HttpResponse
from django.utils import simplejson

from amonestacions.forms import *

from xml.dom.minidom import parse, parseString

from amonestacions.models import *


def inici(request):
	form = NovaAmonestacioForm()
	return render_to_response(
			'amonestacions/index.html', {
				'form': form
	} )

def importData(request):
	dom = parse('/home/pnegre/Downloads/exportacioDadesCentre.xml')
	alumnes = dom.getElementsByTagName('ALUMNE')
	for alumne in alumnes:
		nom = alumne.getAttribute('nom')
		l1 = alumne.getAttribute('ap1')
		l2 = alumne.getAttribute('ap2')
		a = Alumne(nom=nom,llinatge1=l1,llinatge2=l2)
		a.save()
	
	return render_to_response(
			'amonestacions/import.html', {
	} )


def ajaxAlumne(request):
	res = []
	als = Alumne.objects.filter(llinatge1__startswith=request.GET.get('l1',''))
	for a in als:
		data = { 'id': a.id, 'value': a.llinatge1 + ' ' + a.llinatge2 + ', ' + a.nom, 'info': '' }
		res.append(data)
		
	r = { 'results': res }
	return HttpResponse(simplejson.dumps(r), mimetype='application/javascript')