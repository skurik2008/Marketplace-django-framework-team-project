from app_users.models import Profile, Seller
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render

from .forms import ReviewForm
from .models import Offer, Review


def new_review(request, product):
    form = ReviewForm(request.POST)
    if form.is_valid():
        seller_id = request.POST.get('seller')
        offer = get_object_or_404(Offer, product=product, seller__id=seller_id)
        profile, created = Profile.objects.get_or_create(user=request.user)
        review = Review.objects.create(
            profile=profile,
            offer=offer,
            rating=form.cleaned_data['rating'],
            text=form.cleaned_data['text']
        )
        return HttpResponseRedirect(request.path_info)
    else:
        context = {
            'form': form,
            'product': product,
            'reviews': Review.objects.filter(offer__product=product, is_active=True),
            'sellers': Seller.objects.filter(
                profile__in=[offer.seller.profile for offer in Offer.objects.filter(product=product)]
            )
        }
        return render(request, 'products/product_detail.html', context)
    # text_review = request.POST.get('review')
    # offer_id = request.POST.get('offer_id')
    # rating = request.POST.get('rating')
    # Review.objects.create(profile=Profile.objects.get(user=request.user),
    #                       offer=Offer.objects.get(pk=offer_id),
    #                       text=text_review,
    #                       rating=rating)


def review_list(offer_id):
    reviews = Review.objects.filter(offer=offer_id, is_active=True).all()
    return reviews


def review_count(product):
    count = Review.objects.filter(offer__product=product, is_active=True).count()
    return count
