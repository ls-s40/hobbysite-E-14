"""Views for the commissions app"""

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Commission, Job, JobApplication
from .forms import CommissionForm, JobForm, JobApplicationForm
from django.forms import inlineformset_factory
from django.urls import reverse


def commission_list(request):
    """
    commissions = Commission.objects.all()
    for commission in commissions:
        jobs = Job.objects.filter(commission=commission)
        for job in jobs:
            job_accepted = JobApplication.objects.filter(job=job, status='Accepted').count()
            if job_accepted >= job.manpower_required and job.status != 'Full':
            job.status = 'Full'
            job.save()
    """

    
    status_order = ['Open', 'Full', 'Completed', 'Discontinued']
    commissions = sorted(
        Commission.objects.all(),
        key=lambda c: (status_order.index(c.status), -c.created_on.timestamp())
    )

    user_commissions = applied_commissions = None
    if request.user.is_authenticated:
        profile = request.user.profile
        user_commissions = Commission.objects.filter(author=profile)
        applied_commissions = Commission.objects.filter(job__jobapplication__applicant=profile).distinct()

    return render(request, 'commission_list.html', {
        'commissions': commissions,
        'user_commissions': user_commissions,
        'applied_commissions': applied_commissions,
    })


def commission_detail(request, pk):
    commission = get_object_or_404(Commission, pk=pk)
    jobs = Job.objects.filter(commission=commission)

    total_manpower = 0
    total_accepted = 0
    for job in jobs:
        total_manpower += job.manpower_required
        total_accepted += JobApplication.objects.filter(job=job, status='Accepted').count()
        job_accepted = JobApplication.objects.filter(job=job, status='Accepted').count()
        job.slots = job.manpower_required - job_accepted

        # checks the status of the job
        if job_accepted >= job.manpower_required and job.status != 'Full':
            job.status = 'Full'
            job.save()

        print(job)
        print(job.status)
        print()
    open_manpower = total_manpower - total_accepted

    """
    # sets the commission status to full. kaso yung problema is para magupdate yung status ng commission, dapat pumunta muna sa detail view
    if open_manpower == 0:
        commission.status = 'Full'
        commission.save()
    """

    if request.method == 'POST' and request.user.is_authenticated:
        job = get_object_or_404(Job, id=request.POST.get('job_id'))
        JobApplication.objects.get_or_create(
            job=job,
            applicant=request.user.profile,
            defaults={'status': 'Pending'}
        )
        return redirect('commissions:commissions_detail', pk=commission.pk)

    return render(request, 'commission_detail.html', {
        'commission': commission,
        'jobs': jobs,
        'total_manpower': total_manpower,
        'open_manpower': open_manpower
    })


@login_required
def commission_create(request):
    JobFormSet = inlineformset_factory(Commission, Job, form=JobForm, extra=1, can_delete=False)

    if request.method == 'POST':
        form = CommissionForm(request.POST)
        formset = JobFormSet(request.POST, queryset=Job.objects.none())

        if form.is_valid():
            commission = form.save(commit=False)
            commission.author = request.user.profile
            commission.save()

            if formset.is_valid():
                for job_form in formset:
                    if job_form.cleaned_data:
                        job = job_form.save(commit=False)
                        job.commission = commission
                        job.save()

            return redirect('commissions:commissions_detail', pk=commission.pk)
    else:
        form = CommissionForm()
        formset = JobFormSet(queryset=Job.objects.none())

    return render(request, 'commission_form.html', {
        'form': form,
        'formset': formset
    })


@login_required
def commission_update(request, pk):
    commission = get_object_or_404(Commission, pk=pk)
    JobFormSet = inlineformset_factory(Commission, Job, form=JobForm, extra=1, can_delete=False)

    print(commission.status)
    
    if commission.author != request.user.profile:
        return redirect('commissions:commissions_detail', pk=pk)

    if request.method == 'POST':
        form = CommissionForm(request.POST, instance=commission)
        formset = JobFormSet(request.POST, instance=commission)

        if form.is_valid() and formset.is_valid():
            form.save()
            jobs = formset.save(commit=False)
            for job in jobs:
                job.commission = commission
                job.save()
            return redirect('commissions:commissions_detail', pk=pk)
    else:
        form = CommissionForm(instance=commission)
        formset = JobFormSet(instance=commission)

    return render(request, 'commission_form.html', {
        'form': form,
        'formset': formset
    })

