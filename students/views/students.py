# -*- coding: utf-8 -*-


from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from datetime import datetime
from django.contrib import messages
from django.forms import ModelForm
from django.views.generic import UpdateView, DeleteView

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from crispy_forms.bootstrap import FormActions

from ..models import Student, Group

#Views for Students

def students_list(request):
	students = Student.objects.all()

	#try to order students list
	order_by = request.GET.get('order_by', '')
	if order_by in ('id', 'last_name', 'first_name', 'ticket'):
		students = students.order_by(order_by)
		if request.GET.get('reverse', '') == '1':
			students = students.reverse()

	#paginate students
	paginator = Paginator(students, 3)
	page = request.GET.get('page')
	try:
		students = paginator.page(page)
	except PageNotAnInteger:
		students = paginator.page(1)
	except EmptyPage:
		students = paginator.page(paginator.num_pages)

	return render(request, 'students/students_list.html', {'students': students})

def students_add(request):
	# was form posted?
	if request.method == "POST":
		# was form add button clicked?
		if request.POST.get('add_button') is not None:

			# errrs collection
			errors = {}
			# validate students data will go here
			data = {'middle_name': request.POST.get('middle_name'),
			        'notes': request.POST.get('notes')}

			# validate user input
			first_name = request.POST.get('first_name', '').strip()
			if not first_name:
				errors['first_name'] = u"Ім'я є обов'язковим"
			else:
				data['first_name'] = first_name

			last_name = request.POST.get('last_name', '').strip()
			if not last_name:
				errors['last_name'] = u"Прізвище є обов'язковим"
			else:
				data['last_name'] = last_name

			birthday = request.POST.get('birthday', '').strip()
			if not birthday:
				errors['birthday'] = u"Дата народження є обов'язковою"
			else:
				try:
					datetime.strptime(birthday, '%Y-%m-%d')
				except Exception:
					errors['birthday'] = u"Введіть коректний формат дати (напр. 1996-02-12)"
				else:
					data['birthday'] = birthday

			ticket = request.POST.get('ticket', '').strip()
			if not ticket:
				errors['ticket'] = u"Номер білета є обов'язковим"
			else:
				data['ticket'] = ticket

			student_group = request.POST.get('student_group', '').strip()
			if not student_group:
				errors['student_group'] = u"Оберіть групу студента"
			else:
				groups = Group.objects.filter(pk=student_group)
				if len(groups) != 1:
					errors['student_group'] = u"Оберіть коректну групу"
				else:
					data['student_group'] = groups[0]

			photo = request.FILES.get('photo')
			if photo:
				if photo.size > (2048*1024):
					errors['photo'] = u"Розмір фото не повинен перевищувати 2 МБ"
				elif not('image' in photo.content_type):
					errors['photo'] = u"Тип вибраного файлу не зображення"
				else:
					data['photo'] = photo



			if not errors:
				#create student object
				student = Student(**data)

				#save student to database
				student.save()

				#redirect user to students list
				messages.success(request, u'Студента %s %s успішно додано!' % (last_name, first_name) )
				return HttpResponseRedirect(reverse('home'))

			else:
				#render form with errors and previous user input
				for error_key in errors.keys():
					messages.error(request, errors[error_key])
				return render(request, 'students/students_add.html',
					{'groups': Group.objects.all().order_by('title'),
					 'errors': errors})

		elif request.POST.get('cancel_button') is not None:
			#redirect to home page on cancel button
			messages.info(request, u'Додавання студента скасовано!')
			return HttpResponseRedirect(reverse('home'))
	else:
		#initial form render
		return render(request, 'students/students_add.html',
			{'groups': Group.objects.all().order_by('title')})

class StudentUpdateForm(ModelForm):
	class Meta:
		model = Student
		fields = '__all__'

	def __init__(self, *args, **kwargs):
		super(StudentUpdateForm, self).__init__(*args, **kwargs)

		self.helper = FormHelper(self)

		# set form tag attributes

		self.helper.form_action = reverse('students_edit', kwargs={'pk': kwargs['instance'].id})
		self.helper.form_method = 'POST'
		self.helper.form_class = 'form-horizontal'

		# set form field properties
		self.helper.help_text_inline = True
		self.helper.html5_required = True
		self.helper.label_class = 'col-sm-2 control-label'
		self.helper.field_class = 'col-sm-10'

		# add buttons
		self.helper.layout[-1] = FormActions(
			Submit('add_button', u'Зберегти', css_class="btn btn-primary"),
			Submit('cancel_button', u'Скасувати', css_class="btn btn-link"),
		)

class StudentUpdateView(UpdateView):
	model = Student
	template_name = 'students/students_edit.html'
#	fields = '__all__'
	form_class = StudentUpdateForm

	def get_success_url(self):
		messages.success(self.request, u'status_message=Студента успішно збережено!')
		return reverse('home')


	def post(self, request, *args, **kwargs):
		if request.POST.get('cancel_button'):
			messages.info(self.request, u'Редагування студента відмінено!')
			return HttpResponseRedirect(reverse('home'))
		else:
			return super(StudentUpdateView, self).post(request, *args, **kwargs)

class StudentDeleteView(DeleteView):
	model = Student
	template_name = 'students/students_confirm_delete.html'

	def get_success_url(self):
		messages.success(self.request, u'Студента успішно видалено!')
		return reverse('home')