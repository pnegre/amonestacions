# -*- coding: utf-8 -*-

from django.contrib.auth.decorators import login_required, permission_required

from django.http import HttpResponse
from django.utils import simplejson
from amonestacions.models import *
from gestib.models import *

import aux



@permission_required('amonestacions.posar_amonestacions')
def llistaAlumnes(request):
	patt = request.GET.get('l1', '')
	als = Alumne.objects.filter(llinatge1__istartswith=patt)
	res = [
			a.llinatge1 + ' ' + a.llinatge2 + ', ' + a.nom + ' [' + a.expedient + ']'
	for a in als ]

	return HttpResponse(simplejson.dumps({ 'results': res }), mimetype='application/json')


@permission_required('amonestacions.posar_amonestacions')
def anys(request):
	annys = Any.objects.all()
	res = [ [a.id, str(a) ] for a in annys ]
	return HttpResponse(simplejson.dumps(res), mimetype='application/json')


@permission_required('amonestacions.posar_amonestacions')
def avaluacions(request):
	aid = request.GET.get('any')
	anny = Any.objects.get(id=aid)
	avs = Avaluacio.objects.filter(anny=anny)
	res = [ [a.id, str(a) ] for a in avs ]
	return HttpResponse(simplejson.dumps(res), mimetype='application/json')



# Donat un any, treure tots els grups dels cursos
@permission_required('amonestacions.posar_amonestacions')
def grupsAny(request):
	aid = request.GET.get('any')
	anny = Any.objects.get(id=aid)
	grups = Grup.objects.filter(curs__anny=anny)
	res = [ [g.id, str(g) ] for g in grups ]
	return HttpResponse(simplejson.dumps(res), mimetype='application/json')
