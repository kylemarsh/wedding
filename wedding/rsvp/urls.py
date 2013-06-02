from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('apps.rsvp.views',
    url(r'^$', 'rsvp', name='rsvp'),
    url(r'^stats/$', 'stats', name='stats'),
    url(r'^(?P<code>[\w]+)/$', 'rsvp_detail', name='rsvp_detail'),
    url(r'^(?P<code>[\w]+)/edit/$', 'rsvp_edit', name='rsvp_edit'),
)
