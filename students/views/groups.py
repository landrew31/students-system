# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.core.urlresolvers import reverse, reverse_lazy
from django.http import HttpResponse, HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.forms import ModelForm
from django.views.generic import CreateView, UpdateView, DeleteView
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin


from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from crispy_forms.bootstrap import FormActions

from ..models.groups import Group

#Views for Groups

def groups_list(request):
	groups = Group.objects.all()

	# try to order group list
	order_by = request.GET.get('order_by', '')
	if order_by in ('id', 'title', 'leader'):
		groups = groups.order_by(order_by)
		if request.GET.get('reverse', '') == '1':
			groups = groups.reverse()

	# paginate groups
	paginator = Paginator(groups, 3)
	page = request.GET.get('page')
	try:
		groups = paginator.page(page)
	except PageNotAnInteger:
		groups = paginator.page(1)
	except EmptyPage:
		groups = paginator.page(paginator.num_pages)

	return render(request, 'students/groups_list.html', {'groups':groups})

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
		    Submit('add_button', u'Зберегти', css_class="btn btn-primary"),
			Submit('cancel_button', u'Скасувати', css_class="btn btn-link"),
		) )

		#self.fields['leader'].widget.attrs = {'disabled': 'True'}
		#self.fields['leader'].queryset = self.fields['leader'].queryset.none()

class GroupCreateView(SuccessMessageMixin, CreateView):
	"""docstring for GroupCreateView"""
	model = Group
	template_name = 'students/groups_add.html'
	form_class = GroupCreateForm
	success_url = reverse_lazy("groups")
	success_message = u'Групу %(title)s успішно додано!'

	def get_context_data(self, **kwargs):
		context = super(GroupCreateView, self).get_context_data(**kwargs)
		context['page_title'] = u'Додати групу'
		return context

	def post(self, request, *args, **kwargs):
		if request.POST.get('cancel_button') is not None:
			messages.info(request, u'Додавання групи скасовано!')
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
	success_message = u'Групу %(title)s успішно змінено!'

	def get_context_data(self, **kwargs):
		context = super(GroupUpdateView, self).get_context_data(**kwargs)
		context['page_title'] = u'Редагувати групу'
		return context

	def post(self, request, *args, **kwargs):
		if request.POST.get('cancel_button'):
			messages.info(request, u'Редагування скасовано!')
			return HttpResponseRedirect(self.success_url)
		else:
			return super(GroupUpdateView, self).post(request, *args, **kwargs)


class GroupDeleteView(DeleteView):
	"""docstring for GroupDeleteView"""
	model = Group
	template_name = 'students/groups_confirm_delete.html'

	def get_success_url(self, message=u'Групу успішно видалено!'):
		messages.success(self.request, message)
		return reverse('groups')

	def post(self, request, *args, **kwargs):
		if 'cancel_button' in request.POST:
			return HttpResponseRedirect(self.get_success_url(u'Видалення скасовано!'))
		else:
			return super(GroupDeleteView, self).post(request, *args, **kwargs)
