# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


class Result(models.Model):
	"""Examination model"""
	
	class Meta(object):
		verbose_name = u"Результат Іспиту"
		verbose_name_plural = u"Результати Іспитів"

	student = models.ForeignKey('Student',
		verbose_name=u"Студент",
		blank=False,
		null=True)

	exam = models.ForeignKey('Exam',
		verbose_name=u"Назва предмету",
		blank=False,
		null=True)

	mark = models.IntegerField(
		verbose_name=u"Оцінка",
		blank=False,
		null=True)

	def __unicode__(self):
		return u"%s %s, %s - %d" % (self.student.last_name, self.student.first_name, self.exam.subject, self.mark)
