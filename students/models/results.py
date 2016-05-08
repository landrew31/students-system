from __future__ import unicode_literals

from django.db import models

from django.utils.translation import ugettext_lazy as _


class Result(models.Model):
	"""Examination model"""
	
	class Meta(object):
		verbose_name = _(u"Exam result")
		verbose_name_plural = _(u"Exams results")

	student = models.ForeignKey('Student',
		verbose_name=_(u"Student"),
		blank=False,
		null=True
	)

	exam = models.ForeignKey('Exam',
		verbose_name=_(u"Subject title"),
		blank=False,
		null=True
	)

	mark = models.IntegerField(
		verbose_name=_(u"Mark"),
		blank=False,
		null=True
	)

	def __unicode__(self):
		return u"%s %s, %s - %d" % (self.student.last_name, self.student.first_name, self.exam.subject, self.mark)
