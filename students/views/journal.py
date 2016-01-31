# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse

#Views for Students

def students_list(request):
	m = range(0,31)
	students = (
		{'id':1,
		 'name': u'Лупа Андрій',
		 'month':  'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa' },
		{'id':2,
		 'name': u'Чепига Юрій',
		 'month': 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa' },
		{'id':3,
		 'name': u'Курін Ілля',
		 'month': 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa' },
		)
	return render(request, 'students/journal.html', {'students': students})