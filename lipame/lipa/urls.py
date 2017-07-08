from django.conf.urls import url

from . import views

urlpatterns = [
    url(
        regex=r'^make_payment/$',
        view=views.make_payment,
        name='make-payment'
    )
]
