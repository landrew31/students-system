# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse

#Views for Groups

def groups_list(request):
	groups = (
		{'id': 1,
		 'name': 'KA-31',
		 'leader': u'Лупа Андрій'},
		{'id': 2,
		 'name': 'KA-32',
		 'leader': u'Круть Валерія'},
		{'id': 3,
		 'name': 'KA-33',
		 'leader': u'Войтенко Анна'},
		)
	return render(request, 'students/groups_list.html', {'groups':groups})

def groups_add(request):
	return HttpResponse('<h1>Group Add Form</h1>')

def groups_edit(request, gid):
	return HttpResponse('<h1>Edit Group %s</h1>' %gid)

def groups_delete(request, gid):
	return HttpResponse('<h1>Delete Group %s</h1>' %gid)