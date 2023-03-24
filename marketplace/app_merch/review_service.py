from .models import Review, Offer
from app_users.models import Profile


def new_review(request):
    text_review = request.POST.get('review')
    offer_id = request.POST.get('offer_id')
    rating = request.POST.get('rating')
    Review.objects.create(profile=Profile.objects.get(user=request.user),
                          offer=Offer.objects.get(pk=offer_id),
                          text=text_review,
                          rating=rating)


def review_list(offer_id):
    reviews = Review.objects.filter(offer=offer_id, is_active=True).all()
    return reviews


def review_count(offer_id):
    count = Review.objects.filter(offer=offer_id, is_active=True).count()
    return count
