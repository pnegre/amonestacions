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


def informesPdf(periode,grup):
	response = HttpResponse(mimetype='application/pdf')
	response['Content-Disposition'] = 'attachment; filename=informe.pdf'
	
	grup = Grup.objects.get(id=grup)
	periode = Periode.objects.get(id=periode)
	
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
	
	par = Paragraph("<b>Es Liceu</b>. Carrer Cabana, 31. 07141, Pont d'Inca, Marratxí<br/>Telèfon: 971 60 09 86. E-MAIL: escola@esliceu.com<br/><br/>",
		styles['Normal'])
	elements.append(par)
	
	
	amonList = Amonestacio.objects.filter(alumne__grup=grup).filter(dataHora__gt=periode.dt1).filter(dataHora__lt=periode.dt2)
	temp = resumeixAmonestacions(amonList)	
	
	
	doc.build(elements)
	return response
	
	
	
	
	
	
	
	
	
	#for al in alumnes:	
		#par = Paragraph("<b>Es Liceu</b>. Carrer Cabana, 31. 07141, Pont d'Inca, Marratxí<br/>Telèfon: 971 60 09 86. E-MAIL: escola@esliceu.com<br/><br/>",
			#styles['Normal'])
		#elements.append(par)
		#elements.append(Paragraph(unicode(periode.nom), styles['Normal']))
		
		#elements.append(Paragraph(unicode(al), styles['Heading1']))
		
		#elements.append(Paragraph("Data: " + strdate, styles['Normal']))
		#elements.append(Paragraph("Curs: " + unicode(grup), styles['Normal']))
		#elements.append(Paragraph("Tutor/a: " + unicode(grup.tutor) + "<br/><br/>", styles['Normal']))
		
		#dadesTaula = []
		#for a in assignatures:
			#notesFiltrades = Nota.objects.filter(assignatura=a,alumne=al,periode=periode)
			#if len(notesFiltrades) == 0: continue
			#nts = []
			#nts.append(a.nom)
			#for t in tipnotes:
				#try:
					#n = notesFiltrades.get(tipnota=t)
					#nts.append(n.nota.it)
				#except:
					#nts.append("")
			#dadesTaula.append(nts)

		
		#tits = [Paragraph(t.nom,styles['Normal']) for t in tipnotes ]
		#tits.insert(0,'')
				
		#data = []
		#data.append(tits)
		#for i in dadesTaula:
			#data.append(i)
	
		#ts = [
			##('ALIGN', (1,1), (-1,-1), 'CENTER'),
			#('GRID', (0,0), (-1,-1), 1, colors.black),
		#]
		
		## Create the table with the necessary style, and add it to the
		## elements list.
		#table = Table(data,style=ts)
		#elements.append(table)
		
		#coms = ""
		#comentaris = Comentari.objects.filter(alumne=al,periode=periode)
		#for c in comentaris:
			#coms += "<b>" + c.assignatura.nom + ":</b> " + c.text + "  "
		
		#elements.append(Paragraph("<br/><br/>", styles['Normal']))
		#elements.append(Paragraph(coms, styles['Normal']))
		
		#s = "<br/>__________________________________________________________________________________________________________________________________________________<br/>"
		#s += "Alumne/a: " + str(al) + ". Grup: " + str(grup) + "<br/>Signatura del Pare/mare:"
		#par2 = Paragraph(s, styles["Normal"])
		
		#elements.append(par2)
		#elements.append(PageBreak()) 
		
	## Build the pdf document
	#doc.build(elements)
	#return response