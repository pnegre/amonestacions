# -*- coding: utf-8 -*-

from django.conf.urls.defaults import *

urlpatterns = patterns('',

	(r'^$', 'amonestacions.views.novaAmon'),
	(r'^consultagrup/$', 'amonestacions.views.consultaAmon'),
	
	(r'^llistaAlumnes/$', 'amonestacions.ajax.llistaAlumnes'),
	
	(r'^veureAlumne/(?P<alumne_exp>\d+)$', 'amonestacions.views.veureAlumne', {}, "veure-alumne"),
)
