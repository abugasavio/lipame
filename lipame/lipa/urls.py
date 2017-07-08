from django.conf.urls import url

from . import views

urlpatterns = [
    url(
        regex=r'^make-payment/$',
        view=views.make_payment,
        name='make_payment'
    )
]
