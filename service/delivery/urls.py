from django.urls import path
from .views import *

urlpatterns = [
    path('cargo-create/<str:location_pick_up>/<str:location_delivery>/', CargoCreateAPIView.as_view(),
         name='cargo-create'),

    path('cargo/<int:pk>/', CargoUpdateDeleteAPIView.as_view(), name='cargo-update-delete'),

    path('cargo-list/', CargoListAPIView.as_view(), name='cargo-list'),

    path('car/<int:pk>/', CarRetrieveUpdateAPIView.as_view(), name='car-update'),
]
