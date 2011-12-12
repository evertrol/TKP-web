from django.conf.urls.defaults import patterns, include, url
from django.views.generic import RedirectView


urlpatterns = patterns(
   'tkpweb.apps.dataset.main',

   url(r'^$', view=RedirectView.as_view(url="/dataset/")),
   )
