# -*- coding: utf-8 -*-

from django.conf.urls.defaults import *

urlpatterns = patterns('',

	(r'^$', 'amonestacions.views.novaAmon'),
	
	(r'^consultagrup/$', 'amonestacions.views.consultaAmon'),
	(r'^consultaAlumne/$', 'amonestacions.views.consultaAlumne'),
	(r'^stats/$', 'amonestacions.views.stats'),
	
	
	(r'^llistaAlumnes/$', 'amonestacions.ajax.llistaAlumnes'),
	
	(r'^veureAlumne/(?P<perid>\d+)/(?P<alumne_exp>\d+)$', 'amonestacions.views.veureAlumne', {}, "veure-alumne"),
)
