# -*- coding: utf-8 -*-

from django.contrib.auth.decorators import login_required, permission_required

from django.http import HttpResponse
from django.utils import simplejson
from amonestacions.models import *
from gestib.models import *



@permission_required('amonestacions.posar_amonestacions')
def llistaAlumnes(request):
	als = Alumne.objects.filter(llinatge1__istartswith=request.GET.get('l1',''))
	res = [
			a.llinatge1 + ' ' + a.llinatge2 + ', ' + a.nom + ' [' + a.expedient + ']'
	for a in als ]

	return HttpResponse(simplejson.dumps({ 'results': res }), mimetype='application/json')
