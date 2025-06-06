"""
URL configuration for hobbysite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static
    
urlpatterns = [
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/', include(('accounts.urls', 'accounts'), namespace='accounts')),
    path('blog/', include(('blog.urls', 'blog'), namespace='blog')),
    path('admin/', admin.site.urls),
    path('wiki/', include(('wiki.urls', 'wiki'), namespace='wiki')),
    path('forum/', include(('forum.urls', 'forum'), namespace='forum')),
    path('merchstore/', include(('merchstore.urls', 'merchstore'), namespace='merchstore')),
    path('commissions/', include(('commissions.urls', 'commissions'), namespace='commissions')),
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path('profile/', include(('user_management.urls', 'user_management'), namespace='user_management'))
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
