from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns(
    '',
    # Examples:
    url(r'^database/', include('tkpweb.apps.database.urls', namespace='database')),
    url(r'^dataset/', include('tkpweb.apps.dataset.urls', namespace='dataset')),
    url(r'^account/', include('tkpweb.apps.account.urls', namespace='account')),
    # url(r'^tkpweb/', include('tkpweb.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('tkpweb.apps.main.urls', namespace='main')),
)
