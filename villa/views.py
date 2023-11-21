from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.views.generic import DetailView, ListView, TemplateView

from mixins.views import TitleMixin

from .models import Apartment, ApartmentCategory, Basket


class IndexListView(ListView):
    template_name = 'villa/index.html'
    context_object_name = 'apartments'
    model = Apartment

    def get_context_data(self, **kwargs):
        context = super(IndexListView, self).get_context_data(**kwargs)
        context['title'] = 'Villa Agency - Real Estate HTML5 Template'
        context['categories'] = ApartmentCategory.objects.all()
        return context


class PropertiesListView(ListView):
    model = Apartment
    paginate_by = 3
    template_name = 'villa/properties.html'
    context_object_name = 'apartments'

    def get_context_data(self, **kwargs):
        context = super(PropertiesListView, self).get_context_data(**kwargs)
        context['title'] = 'Villa Agency - Property Listing by TemplateMo'
        context['categories'] = ApartmentCategory.objects.all()
        context['apartment_category_id'] = self.kwargs.get('apartment_category_id')
        return context

    def get_queryset(self):
        queryset = super(PropertiesListView, self).get_queryset()
        apartment_category_id = self.kwargs.get('apartment_category_id')
        return queryset.filter(category_id=apartment_category_id) if apartment_category_id else queryset


class PropertyDetailView(DetailView):
    model = Apartment
    template_name = 'villa/property-details.html'


class ContactView(TitleMixin, TemplateView):
    title = 'Contacts'
    template_name = 'villa/contact.html'


@login_required
def basket_add(request, apartment_id):
    apartment = Apartment.objects.get(id=apartment_id)
    baskets = Basket.objects.filter(user=request.user, apartment=apartment)

    if not baskets.exists():
        Basket.objects.create(user=request.user, apartment=apartment, quantity=1)
    else:
        basket = baskets.first()
        basket.quantity += 1
        basket.save()

    return HttpResponseRedirect(request.META['HTTP_REFERER'])


@login_required
def basket_remove(request, basket_id):
    basket = Basket.objects.get(id=basket_id)
    basket.delete()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])
