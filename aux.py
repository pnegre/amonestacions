# -*- coding: utf-8 -*-

import datetime

from django.db.models import Avg, Max, Min, Count

from amonestacions.models import *
from gestib.models import *


def periodeActual():
	now = datetime.datetime.now()
	for x in Periode.objects.all():
		dt1 = x.dt1
		dt2 = x.dt2
		if now > dt1 and now < dt2: return x
	
	return None



def resumeixAmonestacions(amonList):
	tmp = {}
	pts = Config.objects.all()[0].maxPoints
	for a in amonList:
		al = unicode(a.alumne)
		if al in tmp.keys():
			tmp[al]['pts'] += a.gravetat.punts
		else:
			tmp[al] = {'pts': pts + a.gravetat.punts, 'al': a.alumne}
	return tmp


def puntsAlumnePeriode(alumne,periode):
	amonList = Amonestacio.objects.filter(alumne=alumne).filter(dataHora__gt=periode.dt1).filter(dataHora__lt=periode.dt2)
	if amonList == None: return
	
	pts = Config.objects.all()[0].maxPoints
	for a in amonList:
		pts += a.gravetat.punts
	
	return pts


def dataDarreraAmon(alumne):
	dte = Amonestacio.objects.filter(alumne=alumne).aggregate(Max('dataHora'))
	return dte['dataHora__max'].strftime('%d - %m - %Y') 