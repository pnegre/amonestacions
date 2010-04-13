# -*- coding: utf-8 -*-

from django.conf.urls.defaults import *

urlpatterns = patterns('',

	(r'^$', 'amonestacions.views.inici'),
	(r'^import$', 'amonestacions.views.importData'),
	
	(r'^llistaAlumnes/$', 'amonestacions.ajax.llistaAlumnes'),

)
