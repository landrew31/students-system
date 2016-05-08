# -*- coding: utf-8 -*-

from django.shortcuts import render
from django import forms
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib import messages
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.views.generic.edit import FormView

from django.utils.translation import ugettext as _, ugettext_lazy as __

import logging

from studentsdb.settings import ADMIN_EMAIL

class ContactForm(forms.Form):
	"""docstring for ContactForm"""

	def __init__(self, *args, **kwargs):
		# call oroginal initializator
		super(ContactForm, self).__init__(*args, **kwargs)

		# this helper object allows us to customize form
		self.helper = FormHelper()

		# form tag attributes
		self.helper.form_class = 'form-horizontal'
		self.helper.form_method = 'post'
		self.helper.form_action = reverse('contact_admin')

		# twitter bootstrap styles
		self.helper.help_text_inline = True
		self.helper.html5_required = True
		self.helper.label_class = 'col-sm-2 control-label'
		self.helper.field_class = 'col-sm-10'

		# form buttons
		self.helper.add_input(Submit('send_button', _(u'Send')))
		

	from_email = forms.EmailField(
		label=_(u'Your Email')
	)

	subject = forms.CharField(
		label=_(u'Letter header'),
		max_length=128
	)

	message = forms.CharField(
		label=_(u'Message text'),
		max_length=2560,
		widget=forms.Textarea
	)

	recipient_list = [ADMIN_EMAIL]

	def send_email(self):
		subject = self.cleaned_data['subject']
		message = self.cleaned_data['message']
		from_email = self.cleaned_data['from_email']
		print(subject, message, from_email, [ADMIN_EMAIL])
		try:
			sent = send_mail(subject, message, from_email, [ADMIN_EMAIL])
		except Exception:
			message = _(u'Unknown mistake appeared during sending. Try to use the form later.')
			logger = logging.getLogger(__name__)
			logger.exception(message)
		else:
			message = _(u'Message successfully sent!')
		return sent


class ContactView(FormView):
	template_name = 'contact_admin/form.html'
	form_class = ContactForm

	def get_success_url(self):
		return reverse('contact_admin')

	def form_valid(self, form):

		try:
			form.send_email()
		except Exception:
			messages.error(self.request, _(u'Unknown mistake appeared during sending. Try to use the form later.'))
		else:
			messages.success(self.request, _(u'Message successfully sent!')
)

		return super(ContactView, self).form_valid(form)

