from django.conf.urls.defaults import patterns, include, url
from .views import DatasetsView
from .views import DatasetView
from .views import ImagesView
from .views import ImageView
from .views import ExtractedSourcesView
from .views import ExtractedSourceView
from .views import SourcesView
from .views import SourceView
from .views import TransientsView
from .views import TransientView


urlpatterns = patterns(
   'tkpweb.apps.dataset.views',

#   url(r'^(?P<dataset>\d+)/(?P<table>image|source|transient|extractedsource)/(?P<row>\d+)/$', view=AllView.as_view(), name='table-row'),
#   (?P<table>image|source|transient|extractedsource)/$', view=AllView.as_view(), name='table'),

   url(r'^(?P<dataset>\d+)/image/(?P<id>\d+)/$', view=ImageView.as_view(), name='image'),
   url(r'^(?P<dataset>\d+)/image/$', view=ImagesView.as_view(), name='images'),

   url(r'^(?P<dataset>\d+)/transient/(?P<id>\d+)/$', view=TransientView.as_view(), name='transient'),
   url(r'^(?P<dataset>\d+)/transient/$', view=TransientsView.as_view(), name='transients'),
   url(r'^(?P<dataset>\d+)/source/(?P<id>\d+)/$', view=SourceView.as_view(), name='source'),
   url(r'^(?P<dataset>\d+)/source/$', view=SourcesView.as_view(), name='sources'),
   url(r'^(?P<dataset>\d+)/extractedsource/(?P<id>\d+)/$', view=ExtractedSourceView.as_view(), name='extractedsource'),
   url(r'^(?P<dataset>\d+)/extractedsource/$', view=ExtractedSourcesView.as_view(), name='extractedsources'),

   url(r'^(?P<id>\d+)/$', view=DatasetView.as_view(), name='dataset'),
   url(r'^$', view=DatasetsView.as_view(), name='datasets'),
   )
