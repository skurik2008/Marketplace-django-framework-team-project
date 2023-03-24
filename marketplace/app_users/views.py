from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView, PasswordResetConfirmView, \
    PasswordResetDoneView
from django.core.cache import cache
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView
from app_merch.models import Offer
from app_settings.models import SiteSettings
from app_users.forms import UserRegisterForm, UserLoginForm, UserPasswordResetForm, UserSetPasswordForm
from app_users.models import Seller
from sql_util.utils import SubqueryCount


class CustomLoginView(LoginView):
    form_class = UserLoginForm
    template_name = 'users/login.html'
    redirect_authenticated_user = True
    success_url = reverse_lazy('pages:index')


class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('app_users:login')


class CustomPasswordResetView(PasswordResetView):
    form_class = UserPasswordResetForm
    template_name = 'users/password_reset.html'
    email_template_name = 'password_reset_email.html'
    success_url = reverse_lazy('app_users:password_reset_done')


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    form_class = UserSetPasswordForm
    template_name = 'users/password_reset_confirm.html'
    success_url = reverse_lazy('app_users:password_reset_complete')


class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'users/password_reset_done.html'


class CustomRegisterView(CreateView):
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('app_users:login')


# class PasswordResetCompleteView(TemplateView):
#     template_name = 'users/password_reset_complete.html'


class SellerView(DetailView):
    model = Seller
    template_name = 'seller.html'
    context_object_name = 'seller'

    def get_object(self, queryset=None):
        time_to_cache = SiteSettings.load().time_to_cache
        if not time_to_cache:
            time_to_cache = 1

        return cache.get_or_set(
            f"Seller {self.kwargs.get('pk')}",
            super(SellerView, self).get_object(queryset=None),
            time_to_cache * 60 * 60 * 24
        )

    def get_context_data(self, **kwargs):
        context = super(SellerView, self).get_context_data(**kwargs)
        top_seller_products_cache_time = SiteSettings.load().top_seller_products_cache_time

        if not top_seller_products_cache_time:
            top_seller_products_cache_time = 1

        context['offers'] = cache.get_or_set(
            f"Seller {kwargs.get('pk')} top products",
            Offer.objects.filter(seller=self.get_object()).annotate(
                sales=SubqueryCount('order_items')
            ).order_by('-sales')[:10],
            top_seller_products_cache_time * 60 * 60
        )
        return context
