# -*- coding: utf-8 -*-

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
	alumne = Alumne.objects.filter(expedient=alumne_exp)[0]
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
		amonList = Amonestacio.objects.all()
		return render_to_response(
				'amonestacions/consulta.html', {
				'amonList': amonList,
		} )
	
	
	form = ConsultaAmonForm()
	return render_to_response(
			'amonestacions/consulta.html', {
			'form': form,
	} )



