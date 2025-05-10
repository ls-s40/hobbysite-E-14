"""URL config for commissions"""

from django.urls import path
from .views import commission_list, commission_detail, commission_create, commission_update


"""
urlpatterns = [
        path('list/', commission_list, name='index'),
        path('detail/<int:commission_id>/', commission_detail, name='commission_detail')
    ]

app_name = "commissions"
"""

app_name = "commissions"

urlpatterns = [
    path('list/', commission_list, name='index'),
    path('detail/<int:pk>/', commission_detail, name='commissions_detail'),
    path('add/', commission_create, name='commissions_create'),
    path('<int:pk>/edit/', commission_update, name='commissions_update'),
]