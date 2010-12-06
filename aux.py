# -*- coding: utf-8 -*-

import datetime

from reportlab.pdfgen import canvas
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import *
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, LETTER, landscape, portrait

from django.db.models import Avg, Max, Min, Count
from django.http import HttpResponse, HttpResponseRedirect

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
	return dte['dataHora__max'].strftime('%d/%m/%Y')




############### Per treure PDFS

# Necessita id de període i id de grup
# Si id de grup és "-1", agafa tots els grups
def informesPdf(periode,grup):
	response = HttpResponse(mimetype='application/pdf')
	response['Content-Disposition'] = 'attachment; filename=informe.pdf'
	
	# Our container for 'Flowable' objects
	elements = []
	
	# A large collection of style sheets pre-made for us
	styles = getSampleStyleSheet()
	
	# A basic document for us to write to 'rl_hello_platypus.pdf'
	doc = SimpleDocTemplate(response, leftMargin=25, rightMargin=25, topMargin=25, bottomMargin=25)
	doc.pagesize = portrait(A4)
	
	styles['Normal'].fontsize=8
	today = datetime.date.today()
	strdate = str(today.day) + "/" + str(today.month) + "/" + str(today.year)
	
	periode = Periode.objects.get(id=periode)
	amonList = Amonestacio.objects.filter(dataHora__gt=periode.dt1).filter(dataHora__lt=periode.dt2)
	if grup != "-1":
		grup = Grup.objects.get(id=grup)
		amonList = amonList.filter(alumne__grup=grup)
	
	alumnes = set( [ a.alumne for a in amonList ] )
	
	for al in sorted(alumnes, key = lambda a: unicode(a)):
		par = Paragraph("<b>Es Liceu</b>. Carrer Cabana, 31. 07141, Pont d'Inca, Marratxí<br/>Telèfon: 971 60 09 86. E-MAIL: escola@esliceu.com<br/><br/>",
			styles['Normal'])
		elements.append(par)
		elements.append(Paragraph(unicode(periode.descripcio), styles['Normal']))
		
		elements.append(Paragraph(unicode(al), styles['Heading1']))
		
		elements.append(Paragraph("Data: " + strdate, styles['Normal']))
		elements.append(Paragraph("Curs: " + unicode(al.grup), styles['Normal']))
		elements.append(Paragraph("Tutor/a: " + unicode(al.grup.tutor) + "<br/>", styles['Normal']))
		
		elements.append(Paragraph(u"Informe d'incidències", styles['Heading2']))
		
		amons = Amonestacio.objects.filter(dataHora__gt=periode.dt1).filter(dataHora__lt=periode.dt2).filter(alumne=al).order_by('dataHora')
		for a in amons:
			elements.append(Paragraph(u"<b>Data:</b> " + a.dataHora.strftime('%d/%m/%Y') + u'<br/>', styles['Normal']))
			elements.append(Paragraph(u"<b>Professor:</b> " + unicode(a.professor) + u'<br/>', styles['Normal']))
			elements.append(Paragraph(u"<b>Tipus d'incidència:</b> " + unicode(a.gravetat) + u'<br/>', styles['Normal']))
			elements.append(Paragraph(u"<b>Descripció:</b> " + a.descripcio + u'<br/><br/>', styles['Normal']))
		
		totalpunts = puntsAlumnePeriode(al,periode)
		
		elements.append(Paragraph(u"Total punts restants: " + unicode(totalpunts) + u'<br/><br/>', styles['Heading3']))
		
		elements.append(PageBreak()) 
	
	doc.build(elements)
	return response


