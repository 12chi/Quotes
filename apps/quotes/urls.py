from django.conf.urls import url
import views

urlpatterns = [
    url(r'^main$', views.index),
    url(r'^quotes$', views.quotes),
    url(r'^users/(?P<uid>\d+)$', views.show_user),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^add_fav/(?P<qid>\d+)$', views.add_fav),
    url(r'^del_fav/(?P<qid>\d+)$', views.del_fav),
    url(r'^show_user/(?P<uid>\d+)$', views.show_user),
    url(r'^add_quote$', views.add_quote),
    url(r'^reset$', views.reset),  
    url(r'^success$', views.success),
]