# -*- coding: utf-8 -*-

from django.conf.urls import patterns

urlpatterns = patterns('',

	(r'^$', 'amonestacions.views.novaAmon'),

	(r'^consultagrup/$', 'amonestacions.views.consultaAmon'),
	(r'^consultagruppost/$', 'amonestacions.views.consultaAmonPost'),
	(r'^consultaAlumne/$', 'amonestacions.views.consultaAlumne'),
	(r'^stats/$', 'amonestacions.views.stats'),
	(r'^informes/$', 'amonestacions.views.informes'),
	(r'^amonsalumne/$', 'amonestacions.views.amonestacionsAlumne'),
	(r'^emailstutors/$', 'amonestacions.views.emailstutors'),

	(r'^llistaAlumnes/$', 'amonestacions.ajax.llistaAlumnes'),
	(r'^anys/$', 'amonestacions.ajax.anys'),
	(r'^avaluacions/$', 'amonestacions.ajax.avaluacions'),
	(r'^grupsany/$', 'amonestacions.ajax.grupsAny'),
	(r'^tutorgrup/$', 'amonestacions.ajax.tutorGrup'),

	(r'^veureAlumne/(?P<alumne_exp>\d+)$', 'amonestacions.views.veureAlumne', {}, "veure-alumne"),
)
