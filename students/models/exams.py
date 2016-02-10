# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


class Exam(models.Model):
	"""Examination model"""
	
	class Meta(object):
		verbose_name = u"Іспит"
		verbose_name_plural = u"Іспити"

	subject = models.CharField(
		max_length=256,
		blank=False,
		verbose_name=u"Назва предмету")

	time = models.DateTimeField(
		verbose_name=u"Дата і час",
		blank=False,
		null=True)

	teacher = models.CharField(
		max_length=256,
		blank=False,
		verbose_name=u"Викладач")

	for_group = models.ForeignKey('Group',
		verbose_name=u"Група",
		blank=False)

	def __unicode__(self):
		return u"%s - %s (%s)" % (self.subject, self.for_group.title, self.teacher)
