from rest_framework.routers import DefaultRouter
from .views import SessionViewSet
router=DefaultRouter()
from django.urls import path,include
router.register('sessions',SessionViewSet)
urlpatterns=[
    path('',include(router.urls)),
]