from django.conf.urls import url

from . import views

urlpatterns = [
    url(regex=r'^topup/$', view=views.topup, name='make_payment'
    )
]
