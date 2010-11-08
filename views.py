# -*- coding: utf-8 -*-

from datetime import datetime

from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.utils import simplejson
from django.core.mail import send_mail

from django.contrib.auth.decorators import login_required, permission_required

from amonestacions.forms import *
from amonestacions.models import *
from gestib.models import *

import aux



@permission_required('amonestacions.posar_amonestacions')
def novaAmon(request):
	ok = False
	if request.method == 'POST':
		form = NovaAmonestacioForm(request.POST)
		if form.is_valid():
			form.save()
			ok = True
			
			try:
				al = form.amonestacio.alumne
				periode = aux.periodeActual()
				pts = aux.puntsAlumnePeriode(al,periode)
				
				emailTutor = InfoGrup.objects.get(grup=form.amonestacio.alumne.grup).emailTutor
				txt = unicode("Això és un missatge automàtic, enviat pel programa d'amonestacions. No cal que responeu.", 'utf-8') + "\n\n"
				txt += unicode("L'alumne ",'utf-8') + unicode(form.amonestacio.alumne) + unicode(" Ha estat sancionat mitjançant el programa d'amonestacions ",'utf-8')
				txt += unicode("amb una falta de tipus ",'utf-8') + unicode(form.amonestacio.gravetat.nom) + ". "
				txt += unicode("Això comporta actualitzar el seu saldo en ",'utf-8') + unicode(form.amonestacio.gravetat.punts) + unicode(" punts.") + "\n\n"
				txt += unicode("Professor que ha introduit la falta: ",'utf-8') + unicode(form.amonestacio.professor) + "\n\n"
				txt += unicode("Motiu/explicació: ",'utf-8') + unicode(form.amonestacio.descripcio) + "\n\n"
				txt += unicode("Saldo de punts en el període actiu: ",'utf-8') + unicode(pts) + "\n\n"
				send_mail(unicode('[Nova amonestació] alumne ','utf-8') + unicode(form.amonestacio.alumne),
					txt,
					'amonestacions@esliceu.com',
					[emailTutor], fail_silently=False)
			
			except:
				pass
		
	
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




@permission_required('amonestacions.posar_amonestacions')
def consultaAmon(request):
	form = ConsultaAmonForm()
	return render_to_response(
			'amonestacions/consulta.html', {
			'form': form,
	} )


@permission_required('amonestacions.posar_amonestacions')
def consultaAmonPost(request):
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
		temp = aux.resumeixAmonestacions(amonList)
		for a in temp.keys():
			x = AmObj()
			x.pts = temp[a]['pts']
			x.alumne = temp[a]['al']
			amons.append(x)
		
		amons = sorted(amons, key = lambda a: a.pts)
		
		return render_to_response(
				'amonestacions/consultaPost.html', {
				'amons': amons,
				'perid': periode.id,
		} )



@permission_required('amonestacions.posar_amonestacions')
def consultaAlumne(request):
	if request.method == 'POST':
		s = re.search('\[(\d+)\]',request.POST['alumne'])
		exp = s.group(1)
		
		alumne = Alumne.objects.get(expedient=exp)
		periode = Periode.objects.get(id=request.POST['periode'])
		
		return HttpResponseRedirect('/amonestacions/veureAlumne/' + str(periode.id) + '/' + str(alumne.expedient))
	
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


