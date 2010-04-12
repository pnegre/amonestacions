# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.http import HttpResponse
from django.utils import simplejson

#import datetime
#import re

from amonestacions.models import *


def inici(request):
	return render_to_response(
			'amonestacions/index.html', { 
	} )