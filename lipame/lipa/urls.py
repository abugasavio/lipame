from django.conf.urls import url
from wkhtmltopdf.views import PDFTemplateView
from . import views

urlpatterns = [
    url(
        regex=r'^make-payment/$',
        view=views.make_payment,
        name='make_payment'
    ),
    url(r'^pdf/$', PDFTemplateView.as_view(template_name='test.html',
                                           filename='my_pdf.pdf'), name='pdf'),
]
