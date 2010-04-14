# -*- coding: utf-8 -*-

from django.conf.urls.defaults import *

urlpatterns = patterns('',

	(r'^$', 'amonestacions.views.novaAmon'),
	(r'^import/$', 'amonestacions.views.importData'),
	(r'^consulta/$', 'amonestacions.views.consultaAmon'),
	
	(r'^llistaAlumnes/$', 'amonestacions.ajax.llistaAlumnes'),

)
