# -*- coding: utf-8 -*-

from datetime import datetime

from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.utils import simplejson
from django.core.mail import send_mail
from django.template import RequestContext

from django.contrib.auth.decorators import login_required, permission_required

from amonestacions.forms import *
from amonestacions.models import *
from gestib.models import *

import aux


def renderResponse(request,tmpl,dic):
	return render_to_response(tmpl,dic, context_instance=RequestContext(request))



@permission_required('amonestacions.posar_amonestacions')
def novaAmon(request):
	ok = False
	if request.method == 'POST':
		form = NovaAmonestacioForm(request.POST)
		if form.is_valid():
			form.save(request.user)
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
	else:
		form = NovaAmonestacioForm(initial={'dta': datetime.datetime.now().strftime('%d/%m/%Y'), })
	
	return renderResponse(
		request,
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
	return renderResponse(
		request,
		'amonestacions/alumne.html', {
			'alumne': alumne,
			'amonList': amonList,
			'punts': pts
	} )




@permission_required('amonestacions.posar_amonestacions')
def consultaAmon(request):
	form = ConsultaAmonForm()
	return renderResponse(
			request,
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
			if   int(x.pts) <= 0: x.critic = "0"
			elif int(x.pts) == 1: x.critic = "1"
			elif int(x.pts) == 2: x.critic = "2"
			elif int(x.pts) == 3: x.critic = "3"
			elif int(x.pts) == 4: x.critic = "4"
			elif int(x.pts) == 5: x.critic = "5"
			else:                 x.critic = "6"
			x.last = aux.dataDarreraAmon(x.alumne)
			amons.append(x)
		
		amons = sorted(amons, key = lambda a: a.pts)
		
		return renderResponse(
				request,
				'amonestacions/consultaPost.html', {
				'amons': amons,
				'perid': periode.id,
		} )



@permission_required('amonestacions.posar_amonestacions')
def consultaAlumne(request):
	if request.method == 'POST':
		form = ConsultaAmonAlumneForm(request.POST)
		if form.is_valid():
			s = re.search('\[(\d+)\]',request.POST['alumne'])
			exp = s.group(1)
			
			alumne = Alumne.objects.get(expedient=exp)
			periode = Periode.objects.get(id=request.POST['periode'])
			
			return HttpResponseRedirect('/amonestacions/veureAlumne/' + str(periode.id) + '/' + str(alumne.expedient))
	else:
		form = ConsultaAmonAlumneForm()
	
	return renderResponse(
			request,
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
		
	return renderResponse(
			request,
			'amonestacions/stats.html', {
				'sts': sts,
	} )


@permission_required('amonestacions.informes')
def informes(request):
	if request.method == 'POST':
		form = ConsultaInformesForm(request.POST)
		if form.is_valid():
			periode = form.cleaned_data['periode']
			grup = form.cleaned_data['grup']
			return aux.informesPdf(periode,grup)
		
	form = ConsultaInformesForm()
	return renderResponse(
			request,
			'amonestacions/informes.html', {
				'form': form,
	} )

