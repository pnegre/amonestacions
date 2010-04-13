# -*- coding: utf-8 -*-

from django.http import HttpResponse
from django.utils import simplejson
from amonestacions.models import *



def llistaAlumnes(request):
	res = []
	als = Alumne.objects.filter(llinatge1__startswith=request.GET.get('l1',''))
	for a in als:
		data = { 'id': a.id, 'value': a.llinatge1 + ' ' + a.llinatge2 + ', ' + a.nom + ' [' + a.expedient + ']', 'info': '' }
		res.append(data)
		
	r = { 'results': res }
	return HttpResponse(simplejson.dumps(r), mimetype='application/javascript')