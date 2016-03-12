# -*- coding: utf-8 -*-

from django.contrib import admin
from django.core.urlresolvers import reverse
from django.forms import ModelForm, ValidationError

from .models import Student, Group, Exam, Result

class StudentFormAdmin(ModelForm):

	def clean_student_group(self):
		"""Check if student is leader in any group
		If yes, then ensure it's the same as selected group"""

		# get group where current student is a leader
		groups = Group.objects.filter(leader=self.instance)
		if len(groups) > 0 and self.cleaned_data['student_group'] != groups[0]:
			raise ValidationError(u'Студент є старостою іншої групи.', code='invalid')

		return self.cleaned_data['student_group']


class StudentAdmin(admin.ModelAdmin):
	list_display = ['last_name', 'first_name', 'ticket', 'student_group']
	list_display_links = ['last_name', 'first_name']
	list_editable = ['student_group']
	ordering = ['last_name']
	list_filter = ['student_group']
	list_per_page = 10
	search_fields = ['last_name', 'first_name', 'middle_name', 'ticket', 'notes']
	actions = ['copy']
	form = StudentFormAdmin

	def copy(self, request, queryset):
		for student in queryset.values():
			student.pop('id')
			Student(**student).save()
		self.message_user(request, u'Скопійовано студентів: %s' % len(queryset))

	copy.short_description = u'Копіювати вибраних студентів'

	def view_on_site(self, obj):
		return reverse('students_edit', kwargs={'pk': obj.id})


class GroupFormAdmin(ModelForm):

	def __init__(self, *args, **kwargs):
		super(GroupFormAdmin, self).__init__(*args, **kwargs)
		self.fields['leader'].queryset = self.instance.student_set.order_by['last_name']

	def clean_leader_group(self):
		"""Check if leader is student of chosen group"""


		new_leader = self.cleaned_data['leader']
		if hasattr(new_leader, 'student_group') and new_leader.student_group != self.instance:
			raise ValidationError(u'Студент не належить до даної групи', code='invalid')

		return self.cleaned_data['leader']

class GroupAdmin(admin.ModelAdmin):
	list_display = ['title', 'leader']
	list_display_links = ['title']
	list_editable = ['leader']
	ordering = ['title']
	list_per_page = 10
	list_filter = ['title', 'leader']
	search_fields = ['title', 'leader__first_name', 'leader__last_name']

	def view_on_site(self, obj):
		return reverse('groups_edit', kwargs={'pk': obj.id})
"""
	def get_search_results(self, request, queryset, search_term):
		queryset, use_distinct = super(GroupAdmin, self).get_search_results(request, queryset, search_term)
		try:
			search_term_list = search_term.split(' ')
		except Exception, e:
			raise e
		else:
			pass
"""


# Register your models here.
admin.site.register(Student, StudentAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(Exam)
admin.site.register(Result)
