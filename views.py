# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.http import HttpResponse
from django.utils import simplejson

from amonestacions.forms import *
from amonestacions.models import *
from gestib.models import *






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



