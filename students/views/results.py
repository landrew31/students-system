from django.shortcuts import render
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


from ..models.results import Result

#Views for Students

def results_list(request):
	results = Result.objects.all()

	#try to order students list
	order_by = request.GET.get('order_by', '')
	if order_by in ('id', 'student', 'exam', 'mark'):
		results = results.order_by(order_by)
		if request.GET.get('reverse', '') == '1':
			results = results.reverse()

	#paginate students
	paginator = Paginator(results, 3)
	page = request.GET.get('page')
	try:
		results = paginator.page(page)
	except PageNotAnInteger:
		results = paginator.page(1)
	except EmptyPage:
		results = paginator.page(paginator.num_pages)
	return render(request, 'students/results_list.html', {'results': results})


def results_add(request):
	return HttpResponse('<h1>Result Add Form</h1>')

def results_edit(request, sid):
	return HttpResponse('<h1>Edit Result %s</h1>' %sid)

def results_delete(request, sid):
	return HttpResponse('<h1>Delete Result %s</h1>' %sid)