from django.shortcuts import render
from django.core.urlresolvers import reverse, reverse_lazy
from django.http import HttpResponse, HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.forms import ModelForm
from django.views.generic import CreateView, UpdateView, DeleteView
from django.views.generic.base import TemplateView
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin


from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from crispy_forms.bootstrap import FormActions

from django.utils.translation import ugettext as _, ugettext_lazy as __

from ..models.groups import Group
from ..util import paginate 

#Views for Groups

class GroupsView(TemplateView):

	template_name = 'students/groups_list.html'

	def get_context_data(self, **kwargs):

		context = super(GroupsView, self).get_context_data(**kwargs)

		groups = Group.objects.all()

		context = paginate(groups, 5, self.request, context, var_name='groups')

		return context


class GroupCreateForm(ModelForm):
	"""docstring for GroupCreateModel"""
	class Meta:
		model = Group
		fields = '__all__'

	def __init__(self, *args, **kwargs):
		super(GroupCreateForm, self).__init__(*args, **kwargs)
		self.helper = FormHelper(self)

		# set form attributes
		self.helper.form_action = reverse('groups_add')
		self.helper.method = 'POST'
		self.helper.form_class = 'form-horizontal'

		# set field properties
		self.helper.help_text_inline = True
		self.helper.html5_required = False
		self.helper.label_class = 'col-sm-2 control-label'
		self.helper.field_class = 'col-sm-10'

		# add buttons
		self.helper.layout.append( FormActions(
		    Submit('add_button', _(u'Save'), css_class="btn btn-primary"),
			Submit('cancel_button', _(u'Cancel'), css_class="btn btn-link"),
		) )

		#self.fields['leader'].widget.attrs = {'disabled': 'True'}
		#self.fields['leader'].queryset = self.fields['leader'].queryset.none()

class GroupCreateView(SuccessMessageMixin, CreateView):
	"""docstring for GroupCreateView"""
	model = Group
	template_name = 'students/groups_add.html'
	form_class = GroupCreateForm
	success_url = reverse_lazy("groups")
	success_message = __(u'Group "%(title)s" was successfully added!')

	def get_context_data(self, **kwargs):
		context = super(GroupCreateView, self).get_context_data(**kwargs)
		context['page_title'] = _(u'Add group')
		return context

	def post(self, request, *args, **kwargs):
		if request.POST.get('cancel_button') is not None:
			messages.info(request, _(u'Group adding canceled!'))
			return HttpResponseRedirect(self.success_url)
		else:
			return super(GroupCreateView, self).post(request, *args, **kwargs)

class GroupUpdateForm(GroupCreateForm):
	"""docstring for  GroupUpdateForm"""
	def __init__(self, *args, **kwargs):
		super(GroupUpdateForm, self).__init__(*args, **kwargs)

		self.helper.form_action = reverse('groups_edit', kwargs={'pk': kwargs['instance'].id })

		self.fields['leader'].queryset = self.instance.student_set.order_by('last_name')

class GroupUpdateView(SuccessMessageMixin, UpdateView):
	"""docstring for GroupUpdateView"""
	model = Group
	template_name = 'students/groups_add.html'
	form_class = GroupUpdateForm
	success_url = reverse_lazy("groups")
	success_message = __(u'Group "%(title)s" was successfully updated!')

	def get_context_data(self, **kwargs):
		context = super(GroupUpdateView, self).get_context_data(**kwargs)
		context['page_title'] = _(u'Update group')
		return context

	def post(self, request, *args, **kwargs):
		if request.POST.get('cancel_button'):
			messages.info(request, _(u'Updating canceled!'))
			return HttpResponseRedirect(self.success_url)
		else:
			return super(GroupUpdateView, self).post(request, *args, **kwargs)


class GroupDeleteView(DeleteView):
	"""docstring for GroupDeleteView"""
	model = Group
	template_name = 'students/groups_confirm_delete.html'

	def get_success_url(self, message=_(u'Group successfully deleted!')):
		messages.success(self.request, message)
		return reverse('groups')

	def post(self, request, *args, **kwargs):
		if 'cancel_button' in request.POST:
			return HttpResponseRedirect(self.get_success_url(_(u'Deleting canceled!')))
		else:
			return super(GroupDeleteView, self).post(request, *args, **kwargs)
