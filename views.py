# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.http import HttpResponse
from django.utils import simplejson

from amonestacions.forms import *

#import datetime
#import re

from amonestacions.models import *


def inici(request):
	form = NovaAmonestacioForm()
	return render_to_response(
			'amonestacions/index.html', {
				'form': form
	} )