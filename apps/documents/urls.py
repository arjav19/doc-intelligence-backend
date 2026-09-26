from django.urls import path,include
from rest_framework.routers import DefaultRouter
from apps.documents.views import DocumesntViewSet

router = DefaultRouter
router.register(r'documets',DocumesntViewSet,basename='document')

urlpatterns = [
    path('',include(router.urls))
]