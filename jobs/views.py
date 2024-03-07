from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from django_celery_beat.models import PeriodicTask, IntervalSchedule

from .forms import CronJobForm
from .models import CronJob

def home(request):
    return render(request, 'home.html')

@login_required
def cronjob_list(request):

    interval, _ = IntervalSchedule.objects.get_or_create(
        every=30,
        period=IntervalSchedule.SECONDS,
    )

    PeriodicTask.objects.create(
        interval=interval,
        name="my-schedule",
        task="jobs.tasks.execute_job",
        args=[1]
    )

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
            form.save()
            return redirect('cronjob_list')
        return redirect('/')
    return render(request, 'cronjob_edit.html', {'cronjob': cronjob})

@login_required
def cronjob_delete(request, pk):
    cronjob = CronJob.objects.get(pk=pk)
    if request.method == 'POST':
        cronjob.delete()
        return redirect('cronjob_list')
    return render(request, 'cronjob_confirm_delete.html', {'cronjob': cronjob})
