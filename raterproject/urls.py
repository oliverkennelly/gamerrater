from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import routers
from raterapi.views import GameView, CategoryView, ReviewView, UserViewSet, GamePictureViewSet

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'games', GameView, 'game')
router.register(r'categories', CategoryView, 'category')
router.register(r'reviews', ReviewView, 'review')
router.register(r'gamepictures', GamePictureViewSet, 'gamepicture')

urlpatterns = [
    path('', include(router.urls)),
    path('login', UserViewSet.as_view({'post': 'user_login'}), name='login'),
    path('register', UserViewSet.as_view({'post': 'register_account'}), name='register'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)