# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse

#Views for Students

def students_list(request):
	students = (
		{'id':1,
		 'first_name': u'Андрій',
		 'last_name': u'Лупа',
		 'ticket': 9,
		 'image': 'img/me.jpg'},
		{'id':1,
		 'first_name': u'Юрій',
		 'last_name': u'Чепига',
		 'ticket': 18,
		 'image': 'img/chep.jpg'},
		{'id':1,
		 'first_name': u'Ілля',
		 'last_name': u'Курін',
		 'ticket': 7,
		 'image': 'img/kur.jpg'},
		)
	return render(request, 'students/students_list.html', {'students': students})

def students_add(request):
	return HttpResponse('<h1>Student Add Form</h1>')

def students_edit(request, sid):
	return HttpResponse('<h1>Edit Student %s</h1>' %sid)

def students_delete(request, sid):
	return HttpResponse('<h1>Delete Student %s</h1>' %sid)

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

def groups_delete(request, sid):
	return HttpResponse('<h1>Delete Group %s</h1>' %gid)