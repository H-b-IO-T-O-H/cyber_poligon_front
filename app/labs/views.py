import json

from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect

from labs.models import Lab
from labs.forms import LabForm
from labs.task_pool import TaskManager, Task

task_manager = TaskManager()


def new_lab(request):
    if request.method == 'GET':
        form = LabForm()
        if request.user.is_authenticated:
            return render(request, 'labs/utils/new_lab.html', {'form': form})
        return redirect('accounts:login')
    else:
        if not request.user.is_authenticated:
            return HttpResponse(status=403)
        form = LabForm(request.POST)
        if not form.is_valid():
            return redirect(request.META['HTTP_REFERER'])
        lab_full = Lab.objects.create_lab(author=request.user,
                                          title=form.cleaned_data['title'],
                                          description=form.cleaned_data['description'],
                                          executable=form.cleaned_data['script'],
                                          linked_post_id=form.cleaned_data['linked_post'])
        if lab_full:
            lab_full.save()
            return redirect('../labs_catalog')
        else:
            return render(request, 'labs/utils/new_lab.html', {'error': 'Something went wrong. Please try again'})


def labs_catalog(request):
    context = {}
    labs = Lab.objects.all().order_by('-create_date')
    context.update({'labs': labs})
    return render(request, 'labs/utils/labs_catalog.html', context=context)


def display_lab(request, lab_id):
    context = {}
    user = request.user
    task = task_manager.get_user_task(user_id=user.id)
    if task is not None:
        context.update({'error': 'Для пользователя уже запущено виртуальное окружение', 'task': task})
        return render(request, 'labs/utils/lab.html', context=context)
    lab = get_object_or_404(Lab, id=lab_id)
    task = task_manager.push_task(Task(user_id=user.id, executable=lab.executable))
    context.update({'status': 'ok', 'task': task})
    return render(request, 'labs/utils/lab.html', context=context)


def task_status(request, user_id, task_id):
    resp = task_manager.task_status(user_id, task_id)
    if resp['status'] is None:
        return HttpResponse(resp, status=404)
    return HttpResponse(json.dumps(resp), status=200)
