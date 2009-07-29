from django.conf.urls.defaults import *

urlpatterns = patterns('crowdsource.views',
    url(r'^post_cs_entry/$',                              'post_csentry', name = 'post-cs-entry'),
)
