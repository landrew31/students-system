from __future__ import unicode_literals

from django.db import models
from django.utils.translation import ugettext_lazy as _

class Exam(models.Model):
	"""Examination model"""
	
	class Meta(object):
		verbose_name = _(u"Exam")
		verbose_name_plural = _(u"Exams")

	subject = models.CharField(
		max_length=256,
		blank=False,
		verbose_name=_(u"Subject title")
	)

	time = models.DateTimeField(
		verbose_name=_(u"Date and time"),
		blank=False,
		null=True
	)

	teacher = models.CharField(
		max_length=256,
		blank=False,
		verbose_name=_(u"Teacher")
	)

	for_group = models.ForeignKey('Group',
		verbose_name=_(u"Group"),
		blank=False
	)

	def __unicode__(self):
		return u"%s - %s (%s)" % (self.subject, self.for_group.title, self.teacher)
