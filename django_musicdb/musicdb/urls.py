from django.conf.urls import url

from . import views

urlpatterns = [
    url

    #(r'^$', views.index, name='index'),
    (r'^report', 'musicdb.views.report'),
    (r'^artist/(.*)', 'musicdb.views.artist')



]