import datetime
from django.views.generic import TemplateView, View
from django.conf import settings
from django.http import JsonResponse, HttpResponseBadRequest
from lipa.models import Booking
from wallet.models import Wallet, Transaction
from .utils import do_merchant_payment
from .utils import do_merchant_payment, send_sms
from wkhtmltopdf.views import PDFTemplateView


class PDFTicket(PDFTemplateView):
    pass



class LipaView(TemplateView):
    template_name = 'lipa.html'

    def get_context_data(self, **kwargs):
        context = super(LipaView, self).get_context_data(**kwargs)
        if self.request.user.id:
            context['bookings'] = Booking.objects.filter(user=self.request.user).order_by('-created')
            context['wallet_transactions'] = Transaction.objects.filter(wallet__owner=self.request.user).order_by('-created')
            context['balance'] = Wallet.user_balance(self.request.user)
        return context


def make_payment(request):
    if request.method == 'POST':
        date_of_travel = request.POST.get('date_of_travel')
        travel_class = request.POST.get('travel_class')
        trip = request.POST.get('trip')
        # validation
        if not date_of_travel:
            return HttpResponseBadRequest('Date of Travel is required')

        if not travel_class:
            return HttpResponseBadRequest('The class is required')

        if not trip:
            print(trip)
            return HttpResponseBadRequest('Trip is required')

        if date_of_travel:
            date_of_travel = datetime.datetime.strptime(date_of_travel, '%d/%m/%Y')

        booking = Booking.objects.create(date_of_travel=date_of_travel, travel_class=travel_class,
                                         user=request.user)

        if travel_class == Booking.TRAVEL_CLASSES.economy:
            amount = 100
        elif travel_class == Booking.TRAVEL_CLASSES.first_class:
            amount = 300

        response = do_merchant_payment(request.user.phone_number.as_e164.replace('+', ''), amount).json()

        if response['transactionStatus'] == '200':
            booking.payment_reference = response['transactionReference']
            booking.status = Booking.STATUS.paid
            # send_sms(request.user.phone_number.as_e164,
            #        "Thanks you for using LipaME. Your ticket number is TKT#{}".format(booking.id),
            #         None)
        else:
            booking.status = Booking.STATUS.failed
        booking.save()

        response_data = {}
        response_data['result'] = 'Create Payment successful!'
        response_data['booking'] = booking.id

        return JsonResponse(response_data)
    else:
        return JsonResponse({"nothing to see": "this isn't happening"})
