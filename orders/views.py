import stripe
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import CreateView, DetailView, ListView, TemplateView

from mixins.views import TitleMixin
from orders.forms import PreOrderForm
from orders.models import PreOrder
from villa.models import Basket

stripe.api_key = settings.STRIPE_SECRET_KEY
endpoint_secret = settings.STRIPE_WEBHOOK_SECRET


class OrderSuccessView(TitleMixin, TemplateView):
    template_name = 'orders/success.html'
    title = 'Success'


class OrderCancelView(TitleMixin, TemplateView):
    template_name = 'orders/cancel.html'
    title = 'Cancel'


class OrdersView(TitleMixin, ListView):
    model = PreOrder
    title = 'MyOrders'
    template_name = 'orders/orders.html'
    queryset = PreOrder.objects.all()

    def get_queryset(self):
        queryset = super(OrdersView, self).get_queryset()
        return queryset.filter(initiator=self.request.user)


class OrderDetailView(TitleMixin, DetailView):
    model = PreOrder
    title = 'OrderDetail'
    template_name = 'orders/order-detail.html'


class OrderCreateView(CreateView):
    form_class = PreOrderForm
    template_name = 'orders/order.html'
    success_url = reverse_lazy('orders:order')

    def form_valid(self, form):
        form.instance.initiator = self.request.user
        return super(OrderCreateView, self).form_valid(form)

    def post(self, request, *args, **kwargs):
        super(OrderCreateView, self).post(request, *args, **kwargs)
        baskets = Basket.objects.filter(user=self.request.user)
        checkout_session = stripe.checkout.Session.create(
            line_items=baskets.create_line_items(),
            metadata={
                'order_id': int(self.object.id),
            },
            mode='payment',
            success_url='{}{}'.format(settings.DOMAIN_NAME, reverse_lazy('orders:success')),
            cancel_url='{}{}'.format(settings.DOMAIN_NAME, reverse_lazy('orders:cancel')),
        )
        return HttpResponseRedirect(checkout_session.url, status=303)


@csrf_exempt
def my_webhook_view(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError:
        # Invalid signature
        return HttpResponse(status=400)

    # Handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        # Retrieve the session. If you require line items in the response, you may include them by expanding line_items.
        session = stripe.checkout.Session.retrieve(
            event['data']['object']['id'],
            expand=['line_items'],
        )

        # line_items = session.line_items
        # Fulfill the purchase...
        fulfill_order(session)

    # Passed signature verification
    return HttpResponse(status=200)


def fulfill_order(session):
    order_id = int(session.metadata.order_id)
    order = PreOrder.objects.get(id=order_id)
    order.update_after_payment()
