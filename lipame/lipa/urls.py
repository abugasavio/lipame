from django.conf.urls import url

from . import views

urlpatterns = [
    url(
        regex=r'^',
        view=views.LipaView.as_view(),
        name='lipa'
    ),
]
