
from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('',
    url(r'^login/?', 'dreamsso.views.login', name='login'),
    url(r'^logout/?', 'dreamsso.views.logout', name='logout'),
)

