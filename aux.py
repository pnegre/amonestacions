# -*- coding: utf-8 -*-

import datetime

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