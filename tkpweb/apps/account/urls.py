from django.conf.urls.defaults import patterns, include, url
import django.contrib.auth.views
from django.views.generic import TemplateView
from .views import AccountView


urlpatterns = patterns(
    '',
    url(r'^login/$',
        view='django.contrib.auth.views.login',
        kwargs={'template_name': 'account/login.html'},
        name='login'),
    url(r'^logout/$',
        view='django.contrib.auth.views.logout',
        kwargs={'next_page': '/',
         'template_name': 'account/logout.html'},
        name='logout'),
    url(r'^$',
        view=AccountView.as_view(template_name='account/index.html'),
        name='index')
   )
