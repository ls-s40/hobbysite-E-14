"""Views for the commissions app"""

from django.shortcuts import render, get_object_or_404
from .models import Commission


def commissions_list(request):
    """List of all commissions"""
    commissions = Commission.objects.all()
    ctx = {"commissions": commissions}
    return render(request, "commissions_list.html", ctx)


def commissions_detail(request, commission_id):
    """Details of a specific commission"""
    commission = get_object_or_404(Commission, id=commission_id)
    ctx = {"commission": commission}
    return render(request, "commissions_detail.html", ctx)
