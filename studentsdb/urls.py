"""studentsdb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import patterns, include, url
from django.contrib import admin

from students.views.contact_admin import ContactView
from students.views.students import StudentCreateView, StudentUpdateView, StudentDeleteView
from students.views.groups import GroupCreateView, GroupUpdateView, GroupDeleteView

urlpatterns = [
	#Students urls
	url(r'^$', 'students.views.students.students_list', name='home'),
	url(r'^students/add/$', StudentCreateView.as_view(), name='students_add'),
	url(r'^students/(?P<pk>\d+)/edit/$', StudentUpdateView.as_view(), name='students_edit'),
	url(r'^students/(?P<pk>\d+)/delete/$', StudentDeleteView.as_view(), name='students_delete'),

	#Groups urls
	url(r'^groups/$', 'students.views.groups.groups_list', name='groups'),
	url(r'^groups/add/$', GroupCreateView.as_view() , name='groups_add'),
	url(r'^groups/(?P<pk>\d+)/edit/$', GroupUpdateView.as_view() , name='groups_edit'),
	url(r'^groups/(?P<pk>\d+)/delete/$', GroupDeleteView.as_view(), name='groups_delete'),

	#Journal urls
	url(r'^journal/$', 'students.views.journal.students_list', name='journal'),

	#Exams urls
	url(r'^exams/$', 'students.views.exams.exams_list', name='exams'),
	url(r'^exams/add/$', 'students.views.exams.exams_add', name='exams_add'),
	url(r'^exams/(?P<sid>\d+)/edit/$', 'students.views.exams.exams_edit', name='exams_edit'),
	url(r'^exams/(?P<sid>\d+)/delete/$', 'students.views.exams.exams_delete', name='exams_delete'),

	#Exams Results urls
	url(r'^results/$', 'students.views.results.results_list', name='results'),
	url(r'^results/add/$', 'students.views.results.results_add', name='results_add'),
	url(r'^results/(?P<sid>\d+)/edit/$', 'students.views.results.results_edit', name='results_edit'),
	url(r'^results/(?P<sid>\d+)/delete/$', 'students.views.results.results_delete', name='results_delete'),

	# Contact admin form
	url(r'^contact_admin/$', ContactView.as_view(), name='contact_admin'),
	# 'students.views.contact_admin.contact_admin'

    url(r'^admin/', include(admin.site.urls)),
]

from .settings import MEDIA_ROOT, DEBUG

if DEBUG:
	#serve files from media folder
	urlpatterns += patterns('',
		url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': MEDIA_ROOT}))
