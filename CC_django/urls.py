"""CC_django URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import path, re_path
from django.views.generic import TemplateView
from django.conf.urls import url
from CC_django import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name='login.html'),name='login'),
    path('index/', TemplateView.as_view(template_name='index.html'),name='index'),
    url(r'^user_login/$', views.user_login, name='user_login'),
    url(r'^load_events/$', views.load_events, name='load_events'),
    url(r'^submit_add_event/$', views.submit_add_event, name='submit_add_event'),
    url(r'^submit_search_event/$', views.submit_search_event, name='submit_search_event'),
    url(r'^submit_edit_event/$', views.submit_edit_event, name='submit_edit_event'),
    url(r'^submit_remove_event/$', views.submit_remove_event, name='submit_remove_event'),
    url(r'^share_event/$', views.share_event, name='share_event'),
    url(r'^submit_share_event/$', views.submit_share_event, name='submit_share_event'),
    url(r'^signup/$', views.signup, name='signup'),

]
