# -*- coding: utf-8 -*-

from datetime import datetime

from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.http import HttpResponse
from django.utils import simplejson

from django.contrib.auth.decorators import login_required, permission_required

from amonestacions.forms import *
from amonestacions.models import *
from gestib.models import *



@permission_required('amonestacions.posar_amonestacions')
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



@permission_required('amonestacions.posar_amonestacions')
def veureAlumne(request,alumne_exp):
	alumne = Alumne.objects.get(expedient=alumne_exp)
	amonList = Amonestacio.objects.filter(alumne=alumne)
	pts = 100
	for a in amonList:
		pts += a.gravetat.punts
	return render_to_response(
		'amonestacions/alumne.html', {
			'alumne': alumne,
			'amonList': amonList,
			'punts': pts
	} )



@permission_required('amonestacions.posar_amonestacions')
def consultaAmon(request):
	if request.method == 'POST':
		post = request.POST
		periode = Periode.objects.get(id=post['periode'])
		if post['grup'] != '-1':
			grup = Grup.objects.get(id=post['grup'])
			amonList = Amonestacio.objects.filter(alumne__grup=grup)
		else:
			amonList = Amonestacio.objects.all()
		
		amonList = amonList.filter(dataHora__gt=periode.dt1).filter(dataHora__lt=periode.dt2)
		return render_to_response(
				'amonestacions/consulta.html', {
				'amonList': amonList,
		} )	
	
	form = ConsultaAmonForm()
	return render_to_response(
			'amonestacions/consulta.html', {
			'form': form,
	} )



