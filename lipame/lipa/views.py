import datetime
from django.views.generic import TemplateView, View
from django.http import JsonResponse
from lipa.models import Booking


class LipaView(TemplateView):
    template_name = 'lipa.html'


def make_payment(request):
    if request.method == 'POST':
        date_of_travel = request.POST.get('date_of_travel')
        travel_class = request.POST.get('travel_class')
        if date_of_travel:
            date_of_travel = datetime.datetime.strptime(date_of_travel, '%d/%m/%Y')

        booking = Booking.objects.create(date_of_travel=date_of_travel, travel_class=travel_class,
                                         user=request.user)

        response_data = {}
        response_data['result'] = 'Create Payment successful!'
        response_data['booking'] = booking.id

        return JsonResponse(response_data)
    else:
        return JsonResponse({"nothing to see": "this isn't happening"})
