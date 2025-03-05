from django.shortcuts import render
from django.http import HttpResponse

def commissions_list(request):
    commission = commission.objects.all()
    ctx = {
        'commission': commission
    }
    
    return render(request, 'commissions_list.html', ctx)

def commissions_detail(request, id):
    ctx = {
        'commission': Commission.objects.get(id=id)
    }
    
    return render(request, 'commissions_detail.html', ctx)