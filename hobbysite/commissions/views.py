"""Views for the commissions app"""

# idk about redirect
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Commission, Job, JobApplication
from .forms import CommissionForm, JobForm, JobApplicationForm
# not sure kung kasama to
from django.forms import modelformset_factory
from django.urls import reverse
from django.db.models import Sum


"""
def commission_list(request):
    ""List of all commissions""
    commissions = Commission.objects.all()
    ctx = {"commissions": commissions}
    return render(request, "commission_list.html", ctx)


def commission_detail(request, commission_id):
    ""Details of a specific commission""
    commission = get_object_or_404(Commission, id=commission_id)
    ctx = {"commission": commission}
    return render(request, "commission_detail.html", ctx)
"""

# --- Commission List View ---
def commission_list(request):
    status_order = ['Open', 'Full', 'Completed', 'Discontinued']
    commissions = sorted(
        Commission.objects.all(),
        key=lambda c: (status_order.index(c.status), -c.created_on.timestamp())
    )

    user_commissions = applied_commissions = None
    if request.user.is_authenticated:
        profile = request.user.profile
        user_commissions = Commission.objects.filter(author=profile)
        applied_commissions = Commission.objects.filter(
            job__jobapplication__applicant=profile
        ).distinct()

    return render(request, 'commission_list.html', {
        'commissions': commissions,
        'user_commissions': user_commissions,
        'applied_commissions': applied_commissions,
    })


# --- Commission Detail View ---
def commission_detail(request, pk):
    commission = get_object_or_404(Commission, pk=pk)
    jobs = Job.objects.filter(commission=commission)

    # Calculate manpower
    total_manpower = jobs.aggregate(Sum('manpower_required'))['manpower_required__sum'] or 0
    open_manpower = 0
    for job in jobs:
        accepted = JobApplication.objects.filter(job=job, status='Accepted').count()
        open_manpower += max(job.manpower_required - accepted, 0)

    # Handle job application if submitted
    if request.method == 'POST' and request.user.is_authenticated:
        job_id = request.POST.get('job_id')
        job = get_object_or_404(Job, id=job_id)
        accepted = JobApplication.objects.filter(job=job, status='Accepted').count()
        if accepted < job.manpower_required:
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
        'open_manpower': open_manpower,
        'job_application_form': JobApplicationForm(),
    })


# --- Commission Create View ---
@login_required
def commission_create(request):
    JobFormSet = modelformset_factory(Job, form=JobForm, extra=1)

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


# --- Commission Update View ---
@login_required
def commission_update(request, pk):
    commission = get_object_or_404(Commission, pk=pk)
    if commission.author != request.user.profile:
        return redirect('commissions:commissions_detail', pk=pk)

    JobFormSet = modelformset_factory(Job, form=JobForm, extra=1)

    if request.method == 'POST':
        form = CommissionForm(request.POST, instance=commission)
        formset = JobFormSet(request.POST, queryset=Job.objects.filter(commission=commission))

        if form.is_valid() and formset.is_valid():
            form.save()
            jobs = formset.save(commit=False)
            for job in jobs:
                job.commission = commission
                job.save()
            return redirect('commissions:commissions_detail', pk=pk)
    else:
        form = CommissionForm(instance=commission)
        formset = JobFormSet(queryset=Job.objects.filter(commission=commission))

    return render(request, 'commission_form.html', {
        'form': form,
        'formset': formset
    })