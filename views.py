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
def veureAlumne(request,perid,alumne_exp):
	alumne = Alumne.objects.get(expedient=alumne_exp)
	periode = Periode.objects.get(id=perid)
	amonList = Amonestacio.objects.filter(alumne=alumne).filter(dataHora__gt=periode.dt1).filter(dataHora__lt=periode.dt2)
	pts = Config.objects.all()[0].maxPoints
	for a in amonList:
		pts += a.gravetat.punts
	return render_to_response(
		'amonestacions/alumne.html', {
			'alumne': alumne,
			'amonList': amonList,
			'punts': pts
	} )


def resumeixAmonestacions(amonList):
	aux = {}
	pts = Config.objects.all()[0].maxPoints
	for a in amonList:
		al = unicode(a.alumne)
		if al in aux.keys():
			aux[al]['pts'] += a.gravetat.punts
		else:
			aux[al] = {'pts': pts + a.gravetat.punts, 'al': a.alumne}
	return aux


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
		
		class AmObj: pass
		amons = []
		aux = resumeixAmonestacions(amonList)
		for a in aux.keys():
			x = AmObj()
			x.pts = aux[a]['pts']
			x.alumne = aux[a]['al']
			amons.append(x)
		
		amons = sorted(amons, key = lambda a: a.pts)
		
		return render_to_response(
				'amonestacions/consulta.html', {
				'amons': amons,
				'perid': periode.id,
		} )
	
	form = ConsultaAmonForm()
	return render_to_response(
			'amonestacions/consulta.html', {
			'form': form,
	} )



@permission_required('amonestacions.posar_amonestacions')
def consultaAlumne(request):
	if request.method == 'POST':
		s = re.search('\[(\d+)\]',request.POST['alumne'])
		exp = s.group(1)
		
		amonList = Amonestacio.objects.filter(alumne__expedient=exp)
		return render_to_response(
				'amonestacions/consultaAlumne.html', {
				'amonList': amonList,
		} )	
	
	form = ConsultaAmonAlumneForm()
	return render_to_response(
			'amonestacions/consultaAlumne.html', {
			'form': form,
	} )

@permission_required('amonestacions.posar_amonestacions')
def stats(request):
	class EstObj: 
		pass
	
	sts = []
	grups = Grup.objects.all()
	
	for g in grups:
		e = EstObj()
		e.nomGrup = unicode(g)
		amons = Amonestacio.objects.filter(alumne__grup=g)
		e.faltes = len(amons)
		sts.append(e)
		
	return render_to_response(
			'amonestacions/stats.html', {
				'sts': sts,
	} )


