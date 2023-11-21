from villa.models import Basket


def basket(request):
    return {"baskets": Basket.objects.filter(user=request.user) if not request.user.is_anonymous else []}
