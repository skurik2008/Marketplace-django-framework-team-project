from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import (CustomLoginView, CustomLogoutView,
                    CustomPasswordResetConfirmView,
                    CustomPasswordResetDoneView, CustomPasswordResetView,
                    CustomRegisterView, ProfileUpdateView, SellerView, AccountView)

app_name = 'app_users'

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('password_reset/', CustomPasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', CustomPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('register/', CustomRegisterView.as_view(), name='register'),
    path('profile_update/<int:pk>/', ProfileUpdateView.as_view(), name='profile-update'),
    path('seller/<int:pk>/', SellerView.as_view(), name='seller_detail'),
    path('profile/<slug:username>/', AccountView.as_view(), name='account'),
    # path('profile/<slug:username>/edit/',.as_view(), name = 'profile_edit'),
    # path('my/orders/',.as_view(), name = 'history_order'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
