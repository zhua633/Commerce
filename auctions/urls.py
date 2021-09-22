from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("new_listing", views.new_listing, name="new_listing"),
    path("item/<int:listing_id>/", views.item, name="item"),
    path("watchlist/<int:listing_id>", views.watchlist, name="watchlist"),
    path("final/<int:listing_id>", views.final, name="final"),
    path("categories", views.categories, name="categories"),
    path("category/<str:name>", views.category, name="category")
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
