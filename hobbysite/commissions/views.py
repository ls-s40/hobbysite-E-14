"""Views for the commissions app"""

from django.shortcuts import render, get_object_or_404
from .models import Commission


def commission_list(request):
    """List of all commissions"""
    commissions = Commission.objects.all()
    ctx = {"commissions": commissions}
    return render(request, "commission_list.html", ctx)


def commission_detail(request, commission_id):
    """Details of a specific commission"""
    commission = get_object_or_404(Commission, id=commission_id)
    ctx = {"commission": commission}
    return render(request, "commission_detail.html", ctx)
