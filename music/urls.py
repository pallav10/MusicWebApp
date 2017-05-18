from django.conf.urls import url
import views


urlpatterns = [
    url(r'^users/login/$', views.user_login),
    url(r'^users/$', views.user_registration),
    url(r'^users/(?P<pk>[0-9]+)/$', views.user_detail),
    url(r'^users/(?P<pk>[0-9]+)/genre/$', views.genre),
    url(r'^users/(?P<pk>[0-9]+)/genres/$', views.get_all_genres),
    url(r'^users/(?P<pk>[0-9]+)/genre/(?P<key>[0-9]+)/$', views.get_genre),
    url(r'^users/(?P<pk>[0-9]+)/song/$', views.song),
    url(r'^users/(?P<pk>[0-9]+)/tracks/$', views.get_all_tracks),
    url(r'^users/(?P<pk>[0-9]+)/tracks/(?P<key>[0-9]+)/$', views.get_track),
]



