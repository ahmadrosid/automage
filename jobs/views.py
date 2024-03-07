from cron_descriptor import get_description

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .forms import CronJobForm
from .models import CronJob, CronJobLog
from .scheduler import add_to_scheduler, update_scheduler, delete_scheduler

def home(request):
    return render(request, 'home.html')

@login_required
def cronjob_list(request):
    cronjobs = CronJob.objects.filter(user=request.user).order_by('-id')
    return render(request, 'cronjob_list.html', {'cronjobs': cronjobs})

@login_required
def cronjob_create(request):
    if request.method == 'POST':
        form = CronJobForm(request.POST)
        if form.is_valid():
            cronjob = form.save(commit=False)
            cronjob.user = request.user
            cronjob.save()
            add_to_scheduler(cronjob)
            return redirect('cronjob_list')
        return redirect('/')
    else:
        return render(request=request, template_name='cronjob_create.html')

@login_required
def cronjob_edit(request, pk):
    cronjob = CronJob.objects.get(pk=pk)
    if request.method == 'POST':
        form = CronJobForm(request.POST, instance=cronjob, user=request.user)
        if form.is_valid():
            cronjob = form.save()
            update_scheduler(cronjob)
            return redirect('cronjob_list')
        return redirect('/')
    return render(request, 'cronjob_edit.html', {'cronjob': cronjob})

@login_required
def cronjob_delete(request, pk):
    cronjob = CronJob.objects.get(pk=pk)
    if request.method == 'POST':
        cronjob.delete()
        delete_scheduler(cronjob)
        return redirect('cronjob_list')
    return render(request, 'cronjob_confirm_delete.html', {'cronjob': cronjob})

@login_required
def log_list(request, pk):
    cronjob = CronJob.objects.get(pk=pk)
    cronjob_logs = CronJobLog.objects.filter(cronjob_id=pk).order_by('-id')
    if cronjob_logs.exists():
        last_log = cronjob_logs.first() 
        description = get_description(cronjob.schedule)

        return render(request, 'cronjob_logs.html', {
            'logs': cronjob_logs,
            'cronjob': cronjob,
            'total_run': len(cronjob_logs),
            'last_run': last_log,
            'cron_description': description,
        })
    return redirect('cronjob_list')
