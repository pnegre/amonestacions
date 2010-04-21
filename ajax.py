# -*- coding: utf-8 -*-

from django.http import HttpResponse
from django.utils import simplejson
from amonestacions.models import *
from gestib.models import *



def llistaAlumnes(request):
	als = Alumne.objects.filter(llinatge1__startswith=request.GET.get('l1',''))
	res = [ { 
			'id': a.id, 
			'value': a.llinatge1 + ' ' + a.llinatge2 + ', ' + a.nom + ' [' + a.expedient + ']', 
			'info': '' 
	} for a in als ]
	
	return HttpResponse(simplejson.dumps({ 'results': res }), mimetype='application/javascript')